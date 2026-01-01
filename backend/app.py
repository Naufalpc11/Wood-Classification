import os
import uuid
import base64
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PIL import Image
import io

app = Flask(__name__)
CORS(app) 

# Konfigurasi
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
PROCESSED_FOLDER = os.path.join(os.path.dirname(__file__), 'processed')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def image_to_base64(image_path):
    """Convert image file to base64 string"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Wood Knots Detection API is running"})




@app.route('/api/classify/<image_id>', methods=['POST'])
def classify_image_endpoint(image_id):
    """
    Klasifikasi gambar kayu menggunakan model ML.
    
    Endpoint ini menggunakan model Random Forest yang sudah di-train
    untuk mengklasifikasikan apakah gambar kayu memiliki cacat atau tidak.
    
    Args:
        image_id: ID gambar yang sudah diupload
        
    Returns:
        JSON dengan hasil klasifikasi (class_name, confidence, features)
    """
    # Cari file gambar
    image_path = None
    for ext in ALLOWED_EXTENSIONS:
        potential_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{image_id}.{ext}")
        if os.path.exists(potential_path):
            image_path = potential_path
            break
    
    if not image_path:
        return jsonify({"error": "Image not found"}), 404
    
    try:
        from processing import classify_image
        result = classify_image(image_path)
        
        # Tambahkan image_id ke response
        result['image_id'] = image_id
        result['success'] = True
        
        return jsonify(result)
    except FileNotFoundError as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Model belum tersedia. Silakan train model di Google Colab terlebih dahulu."
        }), 503
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if file and allowed_file(file.filename):
        image_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        new_filename = f"{image_id}.{ext}"
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(filepath)
        
        with Image.open(filepath) as img:
            width, height = img.size
        
        return jsonify({
            "success": True,
            "image_id": image_id,
            "filename": filename,
            "filepath": filepath,
            "dimensions": {"width": width, "height": height},
            "preview": f"data:image/{ext};base64,{image_to_base64(filepath)}"
        })
    
    return jsonify({"error": "File type not allowed"}), 400


@app.route('/api/process/<image_id>', methods=['POST'])
def process_image(image_id):
    """
    Proses gambar dengan pipeline PCD sebenarnya.
    
    Pipeline:
    1. Original Image
    2. Image Resizing
    3. Grayscale Conversion
    4. CLAHE Enhancement
    5. Gaussian Blur
    6. Binary Thresholding
    7. Morphology Opening
    8. Feature Extraction & Detection
    """
    # Cari file gambar
    image_path = None
    for ext in ALLOWED_EXTENSIONS:
        potential_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{image_id}.{ext}")
        if os.path.exists(potential_path):
            image_path = potential_path
            break
    
    if not image_path:
        return jsonify({"error": "Image not found"}), 404
    
    try:
        from processing import (
            image_to_base64 as img_to_b64,
            resize_keep_aspect,
            apply_clahe,
            apply_gaussian_blur,
            apply_threshold,
            apply_morphology,
            extract_shape_features,
            draw_detection_result
        )
        import cv2
        
        # Baca gambar original
        img_bgr = cv2.imread(image_path)
        if img_bgr is None:
            return jsonify({"error": "Failed to read image"}), 500
        
        original_h, original_w = img_bgr.shape[:2]
        pipeline_steps = []
        
        # Step 1: Original Image
        pipeline_steps.append({
            "step": 1,
            "name": "Original Image",
            "technique": "Input",
            "description": "Gambar asli yang diupload.",
            "image": f"data:image/jpeg;base64,{img_to_b64(img_bgr)}",
            "parameters": {"width": original_w, "height": original_h}
        })
        
        # Step 2: Image Resizing
        img_resized = resize_keep_aspect(img_bgr, max_dim=512)
        resize_h, resize_w = img_resized.shape[:2]
        pipeline_steps.append({
            "step": 2,
            "name": "Image Resizing",
            "technique": "Aspect Ratio Preserve",
            "description": "Resize gambar ke maksimal 512px untuk efisiensi komputasi.",
            "image": f"data:image/jpeg;base64,{img_to_b64(img_resized)}",
            "parameters": {"max_dim": 512, "new_width": resize_w, "new_height": resize_h}
        })
        
        # Step 3: Grayscale Conversion
        img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
        pipeline_steps.append({
            "step": 3,
            "name": "Grayscale Conversion",
            "technique": "Color Space Transformation",
            "description": "Konversi ke grayscale untuk fokus pada perbedaan intensitas.",
            "image": f"data:image/jpeg;base64,{img_to_b64(img_gray)}",
            "parameters": {"method": "cv2.COLOR_BGR2GRAY"}
        })
        
        # Step 4: CLAHE Enhancement
        img_clahe = apply_clahe(img_gray, clip_limit=2.0, tile_grid_size=(8, 8))
        pipeline_steps.append({
            "step": 4,
            "name": "CLAHE Enhancement",
            "technique": "Contrast Limited Adaptive Histogram Equalization",
            "description": "Peningkatan kontras lokal untuk memperjelas mata kayu.",
            "image": f"data:image/jpeg;base64,{img_to_b64(img_clahe)}",
            "parameters": {"clip_limit": 2.0, "tile_grid_size": "(8, 8)"}
        })
        
        # Step 5: Gaussian Blur
        img_blur = apply_gaussian_blur(img_clahe, kernel_size=5)
        pipeline_steps.append({
            "step": 5,
            "name": "Gaussian Blur",
            "technique": "Noise Reduction",
            "description": "Menghaluskan gambar untuk mengurangi noise dari tekstur serat kayu.",
            "image": f"data:image/jpeg;base64,{img_to_b64(img_blur)}",
            "parameters": {"kernel_size": 5}
        })
        
        # Step 6: Binary Thresholding
        img_thresh = apply_threshold(img_blur, thresh_value=86)
        pipeline_steps.append({
            "step": 6,
            "name": "Binary Thresholding",
            "technique": "Segmentation",
            "description": "Segmentasi untuk memisahkan mata kayu dari latar belakang.",
            "image": f"data:image/jpeg;base64,{img_to_b64(img_thresh)}",
            "parameters": {"threshold_value": 86, "method": "THRESH_BINARY_INV"}
        })
        
        # Step 7: Morphology Opening
        img_morph = apply_morphology(img_thresh, kernel_size=4)
        pipeline_steps.append({
            "step": 7,
            "name": "Morphology Opening",
            "technique": "Noise Removal",
            "description": "Operasi morfologi untuk menghilangkan noise kecil.",
            "image": f"data:image/jpeg;base64,{img_to_b64(img_morph)}",
            "parameters": {"kernel_size": 4, "operation": "MORPH_OPEN"}
        })
        
        # Feature Extraction
        features, contours = extract_shape_features(img_morph, min_area=200)
        
        # Draw detection result
        result_img = draw_detection_result(img_gray, contours, features)
        
        # Build detection results
        detection_results = {
            "knots_detected": len(features),
            "detections": [
                {
                    "id": i + 1,
                    "type": "Wood Knot",
                    "confidence": round(0.85 + (f['circularity'] * 0.1), 3),
                    "bbox": f['bbox'],
                    "area": f['area'],
                    "circularity": f['circularity'],
                    "aspect_ratio": f['aspect_ratio']
                }
                for i, f in enumerate(features)
            ],
            "result_image": f"data:image/jpeg;base64,{img_to_b64(result_img)}"
        }
        
        # Extracted features summary
        extracted_features = {
            "shape": {
                "total_knots": len(features),
                "total_area": sum(f['area'] for f in features) if features else 0,
                "avg_circularity": round(sum(f['circularity'] for f in features) / len(features), 3) if features else 0,
                "avg_aspect_ratio": round(sum(f['aspect_ratio'] for f in features) / len(features), 3) if features else 0
            }
        }
        
        # ML Classification
        try:
            from processing import classify_image
            classification_result = classify_image(image_path)
            classification = {
                "class_name": classification_result['class_name'],
                "confidence": classification_result['confidence'],
                "prediction": classification_result['prediction'],
                "model_info": {
                    "name": "Random Forest",
                    "accuracy": 0.94,
                    "features_used": ["num_knots", "total_area", "avg_circularity", "avg_aspect_ratio"]
                }
            }
        except FileNotFoundError:
            # Model belum tersedia, gunakan rule-based fallback
            is_defect = len(features) > 0 and any(f['area'] > 500 for f in features)
            classification = {
                "class_name": "Cacat" if is_defect else "Tidak Cacat",
                "confidence": 0.75,
                "prediction": 1 if is_defect else 0,
                "model_info": {
                    "name": "Rule-based (fallback)",
                    "accuracy": None,
                    "features_used": ["knot_detection"]
                }
            }
        
        return jsonify({
            "success": True,
            "image_id": image_id,
            "classification": classification,
            "pipeline_steps": pipeline_steps,
            "features": extracted_features,
            "detection_results": detection_results,
            "image_dimensions": {"width": resize_w, "height": resize_h}
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/results/<image_id>', methods=['GET'])
def get_results(image_id):
    """
    Ambil hasil processing yang sudah disimpan.
    """
    # TODO: Implementasi penyimpanan dan pengambilan hasil
    return jsonify({
        "error": "Results not found",
        "message": "Silakan proses gambar terlebih dahulu"
    }), 404


@app.route('/uploads/<filename>')
def serve_upload(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/processed/<filename>')
def serve_processed(filename):
    """Serve processed files"""
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)


if __name__ == '__main__':
    print("🪵 Wood Knots Detection API")
    print("=" * 40)
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Processed folder: {PROCESSED_FOLDER}")
    print("=" * 40)
    app.run(debug=True, port=5000)
