<script setup>
import { computed } from "vue";
import { CheckCircle, XCircle, Info, Cpu, RotateCcw } from "lucide-vue-next";
import Button from "./ui/Button.vue";

const props = defineProps({
    classification: { type: Object, default: null },
    features: { type: Object, default: null },
    results: { type: Object, default: null },
});

const emit = defineEmits(["reset"]);

const isDefect = computed(() => props.classification?.prediction === 1);
const confidencePercent = computed(() => (props.classification?.confidence ? Math.round(props.classification.confidence * 100) : 0));
</script>

<template>
    <div class="flex flex-col gap-6">
        <!-- Header -->
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="bg-primary/10 flex h-10 w-10 items-center justify-center rounded-xl">
                    <Cpu class="text-primary h-5 w-5" />
                </div>
                <h2 class="text-foreground text-2xl font-bold tracking-tight">Hasil Klasifikasi</h2>
            </div>
            <Button v-if="classification" variant="secondary" @click="emit('reset')">
                <RotateCcw class="h-4 w-4" />
                Upload Ulang
            </Button>
        </div>

        <!-- Empty State -->
        <div v-if="!classification" class="flex flex-col items-center justify-center gap-4 rounded-2xl bg-gray-50 p-12">
            <div class="flex h-16 w-16 items-center justify-center rounded-full bg-gray-100">
                <Info class="h-8 w-8 text-gray-400" />
            </div>
            <p class="text-muted-foreground text-center">Hasil klasifikasi akan tampil di sini setelah processing</p>
        </div>

        <!-- Classification Result -->
        <div v-else class="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <!-- Main Result Card -->
            <div class="bg-card overflow-hidden rounded-2xl border shadow-sm">
                <div class="flex flex-col items-center justify-center gap-4 p-8" :class="isDefect ? 'bg-red-50' : 'bg-green-50'">
                    <!-- Icon -->
                    <div class="flex h-24 w-24 items-center justify-center rounded-full" :class="isDefect ? 'bg-red-100' : 'bg-green-100'">
                        <XCircle v-if="isDefect" class="h-14 w-14 text-red-600" />
                        <CheckCircle v-else class="h-14 w-14 text-green-600" />
                    </div>

                    <!-- Result Text -->
                    <div class="text-center">
                        <h3 class="text-3xl font-bold tracking-wide uppercase" :class="isDefect ? 'text-red-600' : 'text-green-600'">
                            {{ classification.class_name }}
                        </h3>
                        <p class="text-muted-foreground mt-1">
                            {{ isDefect ? "Terdeteksi cacat pada kayu" : "Kayu dalam kondisi baik" }}
                        </p>
                    </div>

                    <!-- Confidence Bar -->
                    <div class="w-full max-w-xs">
                        <div class="mb-1 flex justify-between text-sm">
                            <span class="text-muted-foreground">Confidence</span>
                            <span class="font-semibold" :class="isDefect ? 'text-red-600' : 'text-green-600'"> {{ confidencePercent }}% </span>
                        </div>
                        <div class="h-3 w-full overflow-hidden rounded-full bg-gray-200">
                            <div class="h-full rounded-full transition-all duration-500" :class="isDefect ? 'bg-red-500' : 'bg-green-500'" :style="{ width: `${confidencePercent}%` }" />
                        </div>
                    </div>
                </div>

                <!-- Model Info -->
                <div class="border-t p-4 text-sm">
                    <div class="flex items-center justify-between">
                        <span class="text-muted-foreground">Model</span>
                        <span class="font-medium">{{ classification.model_info?.name || "Random Forest" }}</span>
                    </div>
                    <div v-if="classification.model_info?.accuracy" class="mt-1 flex items-center justify-between">
                        <span class="text-muted-foreground">Training Accuracy</span>
                        <span class="font-medium">{{ Math.round(classification.model_info.accuracy * 100) }}%</span>
                    </div>
                </div>
            </div>

            <!-- Features Card -->
            <div class="bg-card rounded-2xl border p-6 shadow-sm">
                <h3 class="text-foreground mb-4 font-semibold">Fitur yang Diekstrak</h3>

                <div v-if="features?.shape" class="grid grid-cols-2 gap-3">
                    <div class="rounded-lg bg-gray-50 p-4 text-center">
                        <p class="text-foreground text-2xl font-bold">{{ features.shape.total_knots }}</p>
                        <p class="text-muted-foreground text-xs">Jumlah Knots</p>
                    </div>
                    <div class="rounded-lg bg-gray-50 p-4 text-center">
                        <p class="text-foreground text-2xl font-bold">{{ features.shape.total_area.toLocaleString() }}</p>
                        <p class="text-muted-foreground text-xs">Total Area (px²)</p>
                    </div>
                    <div class="rounded-lg bg-gray-50 p-4 text-center">
                        <p class="text-foreground text-2xl font-bold">{{ features.shape.avg_circularity }}</p>
                        <p class="text-muted-foreground text-xs">Avg Circularity</p>
                    </div>
                    <div class="rounded-lg bg-gray-50 p-4 text-center">
                        <p class="text-foreground text-2xl font-bold">{{ features.shape.avg_aspect_ratio }}</p>
                        <p class="text-muted-foreground text-xs">Avg Aspect Ratio</p>
                    </div>
                </div>

                <!-- Detection Image Preview -->
                <div v-if="results?.result_image" class="mt-4">
                    <p class="text-muted-foreground mb-2 text-sm font-medium">Hasil Deteksi</p>
                    <img :src="results.result_image" alt="Detection Result" class="w-full rounded-lg border" />
                </div>
            </div>
        </div>
    </div>
</template>
