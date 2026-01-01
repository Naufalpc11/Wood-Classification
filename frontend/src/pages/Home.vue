<script setup>
import { ref } from "vue";
import { AlertCircle, LucideWand2, X } from "lucide-vue-next";
import AppHeader from "../components/AppHeader.vue";
import AppFooter from "../components/AppFooter.vue";
import Card from "../components/ui/Card.vue";
import Button from "../components/ui/Button.vue";
import ImageUploader from "../components/ImageUploader.vue";
import ProcessingSteps from "../components/ProcessingSteps.vue";
import ResultDisplay from "../components/ResultDisplay.vue";
import { uploadImage, processImage as apiProcessImage } from "../api";

const uploaderRef = ref(null);
const selectedFile = ref(null);
const uploadedImageId = ref(null);
const isProcessing = ref(false);
const processingResults = ref(null);
const errorMessage = ref("");

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

        const results = await apiProcessImage(uploadResult.image_id);
        processingResults.value = results;
    } catch (error) {
        console.error("Processing error:", error);
        errorMessage.value = error.message || "Terjadi kesalahan saat memproses gambar";
    } finally {
        isProcessing.value = false;
    }
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
            <!-- Upload Section -->
            <section v-if="!processingResults" class="flex w-full justify-center">
                <Card class="flex w-full max-w-2xl flex-col gap-6">
                    <div class="flex flex-col items-center gap-2">
                        <h2 class="text-foreground text-4xl font-semibold tracking-tighter">Upload Gambar Kayu</h2>
                        <p class="text-muted-foreground text-center text-base">Upload gambar kayu untuk mendeteksi wood knots menggunakan teknik pengolahan citra digital.</p>
                    </div>

                    <ImageUploader ref="uploaderRef" :disabled="isProcessing" @file-selected="handleFileSelected" @file-cleared="handleFileCleared" />

                    <div class="flex justify-center">
                        <Button variant="primary" :loading="isProcessing" :disabled="!selectedFile" @click="processImage">
                            <LucideWand2 v-if="!isProcessing" class="h-5 w-5" />
                            {{ isProcessing ? "Processing..." : "Process Image" }}
                        </Button>
                    </div>
                </Card>
            </section>

            <!-- Results Section -->
            <div v-if="processingResults" class="flex w-full flex-col gap-12">
                <section class="w-full">
                    <ResultDisplay :classification="processingResults.classification" :features="processingResults.features" :results="processingResults.detection_results" @reset="resetAll" />
                </section>
                <section class="border-t-foreground/10 w-full border-t py-8">
                    <ProcessingSteps :steps="processingResults.pipeline_steps" />
                </section>
            </div>

            <!-- Error Toast -->
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
