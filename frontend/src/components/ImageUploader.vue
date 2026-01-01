<script setup>
import { ref, computed } from "vue";
import { ImageIcon, X, CloudUpload } from "lucide-vue-next";

const props = defineProps({
    disabled: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["file-selected", "file-cleared"]);

const fileInput = ref(null);
const isDragging = ref(false);
const selectedFile = ref(null);
const previewUrl = ref(null);

const fileName = computed(() => selectedFile.value?.name || "");
const fileSizeFormatted = computed(() => {
    if (!selectedFile.value) return "";
    const bytes = selectedFile.value.size;
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / 1048576).toFixed(1) + " MB";
});

const uploadZoneClasses = computed(() => {
    const base = "relative flex min-h-80 items-center justify-center rounded-3xl border-2 border-dashed border-border transition-all duration-300";

    if (props.disabled) {
        return `${base} cursor-not-allowed opacity-50`;
    }
    if (isDragging.value) {
        return `${base} cursor-pointer scale-[1.02] border-primary bg-primary/10`;
    }
    if (previewUrl.value) {
        return `${base} cursor-pointer bg-muted p-6`;
    }
    return `${base} cursor-pointer hover:border-primary hover:bg-primary/5`;
});

function triggerFileInput() {
    if (!previewUrl.value && !props.disabled) {
        fileInput.value?.click();
    }
}

function handleDragOver() {
    if (!props.disabled) {
        isDragging.value = true;
    }
}

function handleDragLeave() {
    isDragging.value = false;
}

function handleDrop(event) {
    isDragging.value = false;
    if (props.disabled) return;
    const files = event.dataTransfer?.files;
    if (files?.length > 0) {
        processFile(files[0]);
    }
}

function handleFileSelect(event) {
    if (props.disabled) return;
    const files = event.target?.files;
    if (files?.length > 0) {
        processFile(files[0]);
    }
}

function processFile(file) {
    const validTypes = ["image/png", "image/jpeg", "image/jpg", "image/bmp", "image/tiff"];
    if (!validTypes.includes(file.type)) {
        alert("Tipe file tidak didukung. Gunakan PNG, JPG, JPEG, BMP, atau TIFF.");
        return;
    }

    if (file.size > 16 * 1024 * 1024) {
        alert("Ukuran file terlalu besar. Maksimal 16MB.");
        return;
    }

    selectedFile.value = file;

    const reader = new FileReader();
    reader.onload = (e) => {
        previewUrl.value = e.target.result;
    };
    reader.readAsDataURL(file);

    emit("file-selected", file);
}

function clearImage() {
    if (props.disabled) return;
    selectedFile.value = null;
    previewUrl.value = null;
    if (fileInput.value) {
        fileInput.value.value = "";
    }
    emit("file-cleared");
}

defineExpose({
    clearImage,
    selectedFile,
});
</script>

<template>
    <div :class="uploadZoneClasses" @dragover.prevent="handleDragOver" @dragleave.prevent="handleDragLeave" @drop.prevent="handleDrop" @click="triggerFileInput">
        <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="handleFileSelect" />

        <div v-if="!previewUrl" class="flex flex-col items-center gap-5">
            <div class="bg-primary/10 flex h-24 w-24 items-center justify-center rounded-full">
                <ImageIcon class="text-primary h-12 w-12" />
            </div>

            <div class="text-center">
                <p class="text-foreground text-lg font-medium"><span class="text-primary font-semibold">Klik untuk upload</span> atau drag & drop</p>
                <p class="text-muted-foreground mt-2 text-sm">PNG, JPG, JPEG, BMP, TIFF (Max 16MB)</p>
            </div>
        </div>

        <div v-else class="relative w-full">
            <img :src="previewUrl" :alt="fileName" class="mx-auto max-h-96 rounded-lg object-contain" />

            <div class="absolute right-0 bottom-0 left-0 rounded-b-lg bg-linear-to-t from-black/70 to-transparent p-4">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="max-w-xs truncate font-medium text-white">{{ fileName }}</p>
                        <p class="text-sm text-gray-300">{{ fileSizeFormatted }}</p>
                    </div>
                    <button @click.stop="clearImage" class="rounded-full bg-white/20 p-2 transition-colors hover:bg-white/30">
                        <X class="h-5 w-5 text-white" />
                    </button>
                </div>
            </div>
        </div>

        <div v-if="isDragging" class="bg-primary/20 border-primary absolute inset-0 flex items-center justify-center rounded-xl border-2">
            <div class="text-center">
                <CloudUpload class="text-primary mx-auto h-12 w-12 animate-bounce" />
                <p class="text-primary mt-2 font-semibold">Lepaskan untuk upload</p>
            </div>
        </div>
    </div>
</template>
