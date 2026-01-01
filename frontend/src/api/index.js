// Base URL backend Flask, ganti kalau beda port
const API_BASE_URL = "http://localhost:5000/api";

// Upload gambar ke server
export async function uploadImage(file) {
    const formData = new FormData();
    formData.append("image", file);

    const response = await fetch(`${API_BASE_URL}/upload`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || "Upload failed");
    }

    return response.json();
}

// Proses gambar pakai pipeline PCD
export async function processImage(imageId) {
    const response = await fetch(`${API_BASE_URL}/process/${imageId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || "Processing failed");
    }

    return response.json();
}

// Ambil hasil processing yang udah disimpan
export async function getResults(imageId) {
    const response = await fetch(`${API_BASE_URL}/results/${imageId}`);

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || "Failed to get results");
    }

    return response.json();
}

// Cek backend jalan atau ngga
export async function healthCheck() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        return response.json();
    } catch (error) {
        return { status: "error", message: "Backend not reachable" };
    }
}

// Demo mode - proses gambar sample dengan pipeline PCD
export async function getDemoResults() {
    const response = await fetch(`${API_BASE_URL}/demo`);

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || "Demo processing failed");
    }

    return response.json();
}

export default {
    uploadImage,
    processImage,
    getResults,
    healthCheck,
    getDemoResults,
};
