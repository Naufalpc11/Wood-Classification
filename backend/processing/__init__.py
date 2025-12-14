"""
Wood Knots Detection - Image Processing Module

Modul ini berisi fungsi-fungsi untuk pengolahan citra digital.
Silakan isi dengan implementasi teknik PCD yang diperlukan.

Teknik yang bisa diimplementasikan:
1. Preprocessing:
   - Grayscale conversion
   - Noise reduction (Gaussian blur, Median filter)
   - Histogram equalization
   
2. Processing & Transformation:
   - Edge detection (Canny, Sobel)
   - Morphological operations
   - Thresholding (Otsu, Adaptive)
   
3. Feature Extraction:
   - GLCM (Gray Level Co-occurrence Matrix)
   - HOG (Histogram of Oriented Gradients)
   - LBP (Local Binary Patterns)
   
4. Classification (Bonus):
   - SVM, KNN, Random Forest, etc.
"""

import cv2
import numpy as np
from PIL import Image


def preprocess_image(image_path: str) -> dict:
    """
    Melakukan preprocessing pada gambar.
    
    Args:
        image_path: Path ke file gambar
        
    Returns:
        dict dengan hasil preprocessing setiap tahap
    """
    # TODO: Implementasi oleh teammate
    # Contoh struktur return:
    # return {
    #     "original": original_image,
    #     "grayscale": grayscale_image,
    #     "denoised": denoised_image,
    #     "enhanced": enhanced_image,
    # }
    pass


def extract_features(image) -> dict:
    """
    Ekstraksi fitur dari gambar yang sudah dipreprocess.
    
    Args:
        image: Gambar hasil preprocessing
        
    Returns:
        dict berisi fitur-fitur yang diekstrak
    """
    # TODO: Implementasi oleh teammate
    pass


def detect_knots(image) -> dict:
    """
    Deteksi wood knots pada gambar.
    
    Args:
        image: Gambar yang akan dideteksi
        
    Returns:
        dict berisi hasil deteksi (bounding boxes, classifications, etc.)
    """
    # TODO: Implementasi oleh teammate
    pass


def classify_knot(features) -> dict:
    """
    Klasifikasi tipe wood knot berdasarkan fitur.
    
    Args:
        features: Fitur hasil ekstraksi
        
    Returns:
        dict berisi hasil klasifikasi dan confidence
    """
    # TODO: Implementasi oleh teammate (BONUS)
    pass
