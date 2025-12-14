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
    Proses gambar dengan pipeline PCD.
    
    Endpoint ini akan memanggil fungsi-fungsi dari modul processing.
    Saat ini menggunakan mock data untuk testing UI.
    
    Args:
        image_id: ID gambar yang akan diproses
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
    
    # ============================================================
    # TODO: Ganti mock data ini dengan implementasi PCD sebenarnya
    # dari modul processing/__init__.py
    # ============================================================
    
    # Mock data untuk testing UI
    # Dalam implementasi sebenarnya, panggil:
    # from processing import preprocess_image, extract_features, detect_knots
    # results = preprocess_image(image_path)
    
    original_base64 = image_to_base64(image_path)
    ext = image_path.rsplit('.', 1)[1].lower()
    
    mock_response = {
        "success": True,
        "image_id": image_id,
        "pipeline_steps": [
            {
                "step": 1,
                "name": "Original Image",
                "technique": "Input",
                "description": "Gambar asli yang diupload",
                "image": f"data:image/{ext};base64,{original_base64}",
                "parameters": {}
            },
            {
                "step": 2,
                "name": "Grayscale Conversion",
                "technique": "Color Space Transformation",
                "description": "Konversi ke grayscale untuk mempermudah analisis tekstur",
                "image": f"data:image/{ext};base64,{original_base64}",  # Placeholder
                "parameters": {"method": "cv2.COLOR_BGR2GRAY"}
            },
            {
                "step": 3,
                "name": "Noise Reduction",
                "technique": "Gaussian Blur",
                "description": "Mengurangi noise untuk hasil segmentasi yang lebih baik",
                "image": f"data:image/{ext};base64,{original_base64}",  # Placeholder
                "parameters": {"kernel_size": 5, "sigma": 1.0}
            },
            {
                "step": 4,
                "name": "Histogram Equalization",
                "technique": "CLAHE",
                "description": "Meningkatkan kontras untuk membedakan knots dari kayu normal",
                "image": f"data:image/{ext};base64,{original_base64}",  # Placeholder
                "parameters": {"clip_limit": 2.0, "tile_grid_size": (8, 8)}
            },
            {
                "step": 5,
                "name": "Edge Detection",
                "technique": "Canny Edge Detector",
                "description": "Mendeteksi tepi untuk identifikasi batas knots",
                "image": f"data:image/{ext};base64,{original_base64}",  # Placeholder
                "parameters": {"threshold1": 50, "threshold2": 150}
            },
            {
                "step": 6,
                "name": "Segmentation",
                "technique": "Otsu Thresholding",
                "description": "Segmentasi untuk memisahkan knots dari background",
                "image": f"data:image/{ext};base64,{original_base64}",  # Placeholder
                "parameters": {"threshold_type": "THRESH_BINARY + THRESH_OTSU"}
            }
        ],
        "features": {
            "glcm": {
                "contrast": 0.847,
                "correlation": 0.923,
                "energy": 0.156,
                "homogeneity": 0.789
            },
            "texture": {
                "mean": 127.45,
                "std": 45.23,
                "entropy": 7.234
            }
        },
        "detection_results": {
            "knots_detected": 3,
            "detections": [
                {
                    "id": 1,
                    "type": "Sound Knot",
                    "confidence": 0.945,
                    "bbox": {"x": 120, "y": 80, "width": 50, "height": 45},
                    "area": 2250
                },
                {
                    "id": 2,
                    "type": "Encased Knot",
                    "confidence": 0.872,
                    "bbox": {"x": 280, "y": 150, "width": 65, "height": 60},
                    "area": 3900
                },
                {
                    "id": 3,
                    "type": "Loose Knot",
                    "confidence": 0.798,
                    "bbox": {"x": 400, "y": 200, "width": 40, "height": 38},
                    "area": 1520
                }
            ],
            "result_image": f"data:image/{ext};base64,{original_base64}"  # Placeholder
        }
    }
    
    return jsonify(mock_response)


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
