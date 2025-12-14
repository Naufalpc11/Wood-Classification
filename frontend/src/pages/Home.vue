<script setup>
import { ref } from "vue";
import { AlertCircle, LucideWand2, RotateCcw, X, Play } from "lucide-vue-next";
import AppHeader from "../components/AppHeader.vue";
import AppFooter from "../components/AppFooter.vue";
import Card from "../components/ui/Card.vue";
import Button from "../components/ui/Button.vue";
import ImageUploader from "../components/ImageUploader.vue";
import ProcessingSteps from "../components/ProcessingSteps.vue";
import ResultDisplay from "../components/ResultDisplay.vue";
import ComparativeAnalysis from "../components/ComparativeAnalysis.vue";
import { uploadImage, processImage as apiProcessImage } from "../api";

const uploaderRef = ref(null);
const selectedFile = ref(null);
const uploadedImageId = ref(null);
const isProcessing = ref(false);
const processingResults = ref(null);
const imageDimensions = ref({ width: 800, height: 600 });
const errorMessage = ref("");

const mockResults = {
    pipeline_steps: [
        {
            step: 1,
            name: "Grayscale Conversion",
            technique: "Color Space",
            description: "Mengkonversi gambar RGB menjadi grayscale untuk menyederhanakan analisis tekstur kayu.",
            image: "https://picsum.photos/seed/step1/400/300",
            parameters: { method: "Luminosity", channels: "RGB → Gray" },
        },
        {
            step: 2,
            name: "Gaussian Blur",
            technique: "Smoothing",
            description: "Menerapkan filter Gaussian untuk mengurangi noise dan memperhalus gambar.",
            image: "https://picsum.photos/seed/step2/400/300",
            parameters: { kernel_size: "5x5", sigma: "1.5" },
        },
        {
            step: 3,
            name: "CLAHE Enhancement",
            technique: "Contrast",
            description: "Meningkatkan kontras lokal menggunakan Contrast Limited Adaptive Histogram Equalization.",
            image: "https://picsum.photos/seed/step3/400/300",
            parameters: { clip_limit: "2.0", tile_size: "8x8" },
        },
        {
            step: 4,
            name: "Edge Detection",
            technique: "Canny",
            description: "Mendeteksi tepi untuk mengidentifikasi batas-batas mata kayu.",
            image: "https://picsum.photos/seed/step4/400/300",
            parameters: { threshold1: "50", threshold2: "150" },
        },
        {
            step: 5,
            name: "Morphological Operations",
            technique: "Closing",
            description: "Operasi morfologi untuk menutup gap dan menghubungkan area terdeteksi.",
            image: "https://picsum.photos/seed/step5/400/300",
            parameters: { operation: "Close", kernel: "Ellipse 5x5" },
        },
        {
            step: 6,
            name: "Contour Detection",
            technique: "findContours",
            description: "Menemukan dan menganalisis kontur untuk mengidentifikasi kandidat mata kayu.",
            image: "https://picsum.photos/seed/step6/400/300",
            parameters: { mode: "RETR_EXTERNAL", method: "CHAIN_APPROX_SIMPLE" },
        },
    ],
    detection_results: {
        result_image: "https://picsum.photos/seed/wood/800/600",
        knots_detected: 4,
        detections: [
            { id: 1, type: "Sound Knot", bbox: { x: 120, y: 80, width: 90, height: 95 }, area: 6750, confidence: 0.94 },
            { id: 2, type: "Encased Knot", bbox: { x: 350, y: 200, width: 75, height: 80 }, area: 4800, confidence: 0.87 },
            { id: 3, type: "Loose Knot", bbox: { x: 550, y: 120, width: 85, height: 90 }, area: 5950, confidence: 0.91 },
            { id: 4, type: "Dead Knot", bbox: { x: 200, y: 380, width: 70, height: 72 }, area: 3960, confidence: 0.82 },
        ],
    },
    features: {
        glcm: {
            contrast: 0.234,
            correlation: 0.891,
            energy: 0.156,
            homogeneity: 0.743,
        },
        texture: {
            mean: 127.45,
            std: 42.18,
            entropy: 5.67,
            kurtosis: 2.34,
            skewness: 0.15,
            uniformity: 0.089,
        },
    },
};

function handleFileSelected(file) {
    selectedFile.value = file;
    processingResults.value = null;
    errorMessage.value = "";
}

function handleFileCleared() {
    selectedFile.value = null;
    uploadedImageId.value = null;
    processingResults.value = null;
}

async function processImage() {
    if (!selectedFile.value) return;

    isProcessing.value = true;
    errorMessage.value = "";

    try {
        const uploadResult = await uploadImage(selectedFile.value);
        uploadedImageId.value = uploadResult.image_id;
        imageDimensions.value = uploadResult.dimensions;

        const results = await apiProcessImage(uploadResult.image_id);
        processingResults.value = results;
    } catch (error) {
        console.error("Processing error:", error);
        errorMessage.value = error.message || "Terjadi kesalahan saat memproses gambar";
    } finally {
        isProcessing.value = false;
    }
}

function loadDemoResults() {
    isProcessing.value = true;
    setTimeout(() => {
        processingResults.value = mockResults;
        imageDimensions.value = { width: 800, height: 600 };
        isProcessing.value = false;
    }, 1500);
}

function resetAll() {
    uploaderRef.value?.clearImage();
    selectedFile.value = null;
    uploadedImageId.value = null;
    processingResults.value = null;
    errorMessage.value = "";
}
</script>

<template>
    <div class="bg-background relative flex min-h-screen flex-col items-center gap-3">
        <AppHeader />

        <main class="flex w-full max-w-6xl flex-1 flex-col gap-8 px-4 py-8">
            <section class="flex w-full justify-center">
                <Card class="flex w-full max-w-2xl flex-col gap-6">
                    <div class="flex flex-col items-center gap-2">
                        <h2 class="text-foreground text-4xl font-semibold tracking-tighter">Upload Gambar Kayu</h2>
                        <p class="text-muted-foreground text-center text-base">Upload gambar kayu untuk mendeteksi wood knots menggunakan teknik pengolahan citra digital.</p>
                    </div>

                    <ImageUploader ref="uploaderRef" @file-selected="handleFileSelected" @file-cleared="handleFileCleared" />

                    <div class="flex items-center justify-center gap-5">
                        <Button variant="primary" :loading="isProcessing" :disabled="!selectedFile" @click="processImage">
                            <LucideWand2 v-if="!isProcessing" class="h-5 w-5" />
                            {{ isProcessing ? "Processing..." : "Process Image" }}
                        </Button>

                        <Button v-if="!processingResults" variant="secondary" :loading="isProcessing" @click="loadDemoResults">
                            <Play v-if="!isProcessing" class="h-5 w-5" />
                            {{ isProcessing ? "Loading..." : "Demo Mode" }}
                        </Button>

                        <Button v-if="processingResults" variant="secondary" @click="resetAll">
                            <RotateCcw class="h-5 w-5" />
                            Reset
                        </Button>
                    </div>
                </Card>
            </section>

            <div v-if="processingResults" class="flex w-full flex-col gap-12 px-4 py-8">
                <section class="border-t-foreground/10 w-full border-t py-8">
                    <ProcessingSteps :steps="processingResults.pipeline_steps" />
                </section>

                <section class="border-t-foreground/10 w-full border-t py-8">
                    <ResultDisplay :results="processingResults.detection_results" :features="processingResults.features" :image-dimensions="imageDimensions" />
                </section>

                <section class="border-t-foreground/10 w-full border-t py-8">
                    <ComparativeAnalysis />
                </section>
            </div>

            <div v-if="errorMessage" class="bg-destructive fixed right-6 bottom-6 flex items-center gap-3 rounded-xl px-6 py-4 text-white shadow-lg">
                <AlertCircle class="h-6 w-6" />
                <span>{{ errorMessage }}</span>
                <button @click="errorMessage = ''" class="ml-2 hover:opacity-75">
                    <X class="h-5 w-5" />
                </button>
            </div>
        </main>

        <AppFooter />
    </div>
</template>
