<script setup>
import { computed } from "vue";
import { Crosshair, ClipboardCheck } from "lucide-vue-next";

const props = defineProps({
    results: {
        type: Object,
        default: null,
    },
    features: {
        type: Object,
        default: null,
    },
    imageDimensions: {
        type: Object,
        default: () => ({ width: 800, height: 600 }),
    },
});

const knotTypes = [
    { name: "Sound Knot", color: "#22c55e" },
    { name: "Encased Knot", color: "#f59e0b" },
    { name: "Loose Knot", color: "#ef4444" },
    { name: "Dead Knot", color: "#6b7280" },
];

const imageViewBox = computed(() => {
    return `0 0 ${props.imageDimensions.width} ${props.imageDimensions.height}`;
});

function getBoxColor(type) {
    const found = knotTypes.find((t) => t.name === type);
    return found ? found.color : "#3b82f6";
}
</script>

<template>
    <div class="flex flex-col gap-6">
        <div class="flex items-center gap-3">
            <div class="bg-primary/10 flex h-10 w-10 items-center justify-center rounded-xl">
                <Crosshair class="text-primary h-5 w-5" />
            </div>
            <h2 class="text-foreground text-2xl font-semibold">Detection Results</h2>
        </div>

        <div v-if="!results" class="bg-card rounded-2xl border p-8 py-16 text-center shadow-sm">
            <div class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-gray-100">
                <ClipboardCheck class="h-8 w-8 text-gray-400" />
            </div>
            <p class="text-muted-foreground">Hasil deteksi akan tampil di sini setelah processing</p>
        </div>

        <div v-else class="grid grid-cols-1 gap-6 lg:grid-cols-3">
            <div class="lg:col-span-2">
                <div class="bg-card overflow-hidden rounded-2xl border shadow-sm">
                    <div class="relative bg-gray-100">
                        <img :src="results.result_image" alt="Detection Result" class="h-auto w-full" />

                        <svg v-if="results.detections && results.detections.length > 0" class="pointer-events-none absolute inset-0 h-full w-full" :viewBox="imageViewBox" preserveAspectRatio="xMidYMid meet">
                            <g v-for="detection in results.detections" :key="detection.id">
                                <rect :x="detection.bbox.x" :y="detection.bbox.y" :width="detection.bbox.width" :height="detection.bbox.height" fill="none" :stroke="getBoxColor(detection.type)" stroke-width="3" rx="4" />
                                <rect :x="detection.bbox.x" :y="detection.bbox.y - 25" :width="detection.type.length * 10 + 20" height="24" :fill="getBoxColor(detection.type)" rx="4" />
                                <text :x="detection.bbox.x + 10" :y="detection.bbox.y - 8" fill="white" font-size="12" font-weight="600">
                                    {{ detection.type }}
                                </text>
                            </g>
                        </svg>
                    </div>

                    <div class="border-t border-gray-100 p-4">
                        <div class="flex flex-wrap gap-4">
                            <div v-for="type in knotTypes" :key="type.name" class="flex items-center gap-2">
                                <div class="h-4 w-4 rounded" :style="{ backgroundColor: type.color }"></div>
                                <span class="text-muted-foreground text-sm">{{ type.name }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="space-y-5">
                <div class="bg-card rounded-2xl border p-6 shadow-sm">
                    <h3 class="text-foreground mb-4 font-semibold">Summary</h3>

                    <div class="bg-primary/10 mb-5 rounded-xl p-4 text-center">
                        <div class="text-primary text-4xl font-bold">{{ results.knots_detected }}</div>
                        <div class="text-muted-foreground text-sm">Knots Detected</div>
                    </div>

                    <div class="space-y-3">
                        <div v-for="detection in results.detections" :key="detection.id" class="flex items-center justify-between rounded-lg bg-gray-50 p-3">
                            <div class="flex items-center gap-3">
                                <div class="h-3 w-3 rounded-full" :style="{ backgroundColor: getBoxColor(detection.type) }"></div>
                                <div>
                                    <p class="text-foreground text-sm font-medium">
                                        {{ detection.type }}
                                    </p>
                                    <p class="text-muted-foreground text-xs">Area: {{ detection.area }}px²</p>
                                </div>
                            </div>
                            <div class="text-right">
                                <p class="text-primary font-bold">{{ (detection.confidence * 100).toFixed(1) }}%</p>
                                <p class="text-muted-foreground text-xs">confidence</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="features" class="bg-card rounded-2xl border p-6 shadow-sm">
                    <h3 class="text-foreground mb-4 font-semibold">Extracted Features</h3>

                    <div v-if="features.glcm" class="mb-5">
                        <h4 class="text-muted-foreground mb-3 text-sm font-medium">GLCM</h4>
                        <div class="grid grid-cols-2 gap-3">
                            <div v-for="(value, key) in features.glcm" :key="key" class="rounded-lg bg-gray-50 p-3 text-center">
                                <p class="text-foreground text-lg font-bold">
                                    {{ typeof value === "number" ? value.toFixed(3) : value }}
                                </p>
                                <p class="text-muted-foreground text-xs capitalize">{{ key }}</p>
                            </div>
                        </div>
                    </div>

                    <div v-if="features.texture">
                        <h4 class="text-muted-foreground mb-3 text-sm font-medium">Texture</h4>
                        <div class="grid grid-cols-3 gap-3">
                            <div v-for="(value, key) in features.texture" :key="key" class="rounded-lg bg-gray-50 p-3 text-center">
                                <p class="text-foreground text-sm font-bold">
                                    {{ typeof value === "number" ? value.toFixed(2) : value }}
                                </p>
                                <p class="text-muted-foreground text-xs capitalize">{{ key }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
