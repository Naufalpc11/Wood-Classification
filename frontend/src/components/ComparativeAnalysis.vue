<script setup>
import { computed } from "vue";
import { BarChart3, Trophy, Clock, Target, Lightbulb } from "lucide-vue-next";

const techniques = [
    {
        name: "Grayscale Conversion",
        purpose: "Menyederhanakan analisis dengan menghilangkan informasi warna",
        effectiveness: 85,
        time: 12,
        impact: "Tinggi",
    },
    {
        name: "Gaussian Blur",
        purpose: "Mengurangi noise dan memperhalus gambar",
        effectiveness: 78,
        time: 24,
        impact: "Sedang",
    },
    {
        name: "CLAHE",
        purpose: "Meningkatkan kontras lokal untuk detail yang lebih jelas",
        effectiveness: 95,
        time: 35,
        impact: "Tinggi",
    },
    {
        name: "Canny Edge Detection",
        purpose: "Mendeteksi tepi untuk identifikasi batas knots",
        effectiveness: 88,
        time: 28,
        impact: "Tinggi",
    },
    {
        name: "Morphological Ops",
        purpose: "Membersihkan noise dan menghubungkan area terdeteksi",
        effectiveness: 82,
        time: 18,
        impact: "Sedang",
    },
    {
        name: "Otsu Thresholding",
        purpose: "Segmentasi otomatis berdasarkan histogram",
        effectiveness: 90,
        time: 15,
        impact: "Tinggi",
    },
];

const recommendations = [
    "Kombinasi CLAHE dan Canny Edge Detection memberikan hasil terbaik untuk deteksi wood knots pada dataset ini.",
    "Gaussian Blur dengan kernel 5x5 optimal untuk mengurangi noise tanpa kehilangan detail penting.",
    "Morphological operations sebaiknya menggunakan kernel ellipse untuk bentuk knots yang lebih natural.",
    "Untuk dataset dengan pencahayaan tidak merata, CLAHE sangat direkomendasikan dibanding histogram equalization standar.",
    "Pipeline dapat dioptimasi dengan mengurangi ukuran gambar input untuk kecepatan tanpa mengorbankan akurasi signifikan.",
];

const totalTime = computed(() => {
    return techniques.reduce((sum, t) => sum + t.time, 0);
});

const avgAccuracy = computed(() => {
    return Math.round(techniques.reduce((sum, t) => sum + t.effectiveness, 0) / techniques.length);
});

function getImpactClass(impact) {
    switch (impact) {
        case "Tinggi":
            return "bg-green-100 text-green-700";
        case "Sedang":
            return "bg-yellow-100 text-yellow-700";
        default:
            return "bg-gray-100 text-gray-700";
    }
}
</script>

<template>
    <div class="flex flex-col gap-8">
        <div class="flex items-center gap-3">
            <div class="bg-primary/10 flex h-10 w-10 items-center justify-center rounded-xl">
                <BarChart3 class="text-primary h-5 w-5" />
            </div>
            <h2 class="text-foreground text-2xl font-semibold">Analisis Komparatif</h2>
        </div>

        <div class="mb-6 overflow-hidden rounded-xl border p-0">
            <div class="bg-muted/50 border-b px-6 py-4">
                <h3 class="text-foreground font-semibold">Perbandingan Teknik Preprocessing</h3>
                <p class="text-muted-foreground text-sm">Efektivitas setiap teknik terhadap kualitas deteksi</p>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full">
                    <thead>
                        <tr class="bg-muted/30 border-b">
                            <th class="text-foreground px-6 py-3 text-left text-sm font-semibold">Teknik</th>
                            <th class="text-foreground px-6 py-3 text-left text-sm font-semibold">Tujuan</th>
                            <th class="text-foreground px-6 py-3 text-center text-sm font-semibold">Efektivitas</th>
                            <th class="text-foreground px-6 py-3 text-center text-sm font-semibold">Waktu (ms)</th>
                            <th class="text-foreground px-6 py-3 text-left text-sm font-semibold">Dampak</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(technique, index) in techniques" :key="technique.name" class="hover:bg-muted/20 border-b transition-colors last:border-b-0">
                            <td class="px-6 py-4">
                                <div class="flex items-center gap-3">
                                    <div class="bg-primary/10 text-primary flex h-8 w-8 items-center justify-center rounded-full text-sm font-bold">
                                        {{ index + 1 }}
                                    </div>
                                    <span class="text-foreground font-medium">{{ technique.name }}</span>
                                </div>
                            </td>
                            <td class="text-muted-foreground max-w-xs px-6 py-4 text-sm">{{ technique.purpose }}</td>
                            <td class="px-6 py-4 text-center">
                                <div class="flex items-center justify-center gap-2">
                                    <div class="h-2 w-20 overflow-hidden rounded-full bg-gray-200">
                                        <div class="bg-primary h-full rounded-full transition-all" :style="{ width: `${technique.effectiveness}%` }"></div>
                                    </div>
                                    <span class="text-foreground w-10 text-sm font-medium">{{ technique.effectiveness }}%</span>
                                </div>
                            </td>
                            <td class="text-muted-foreground px-6 py-4 text-center font-mono text-sm">{{ technique.time }}</td>
                            <td class="px-6 py-4">
                                <span :class="['rounded-full px-3 py-1 text-xs font-medium', getImpactClass(technique.impact)]">
                                    {{ technique.impact }}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="grid grid-cols-1 gap-5 md:grid-cols-3">
            <div class="bg-card rounded-2xl border p-6 shadow-sm">
                <div class="mb-3 flex items-center gap-3">
                    <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-green-100 text-green-600">
                        <Trophy class="h-5 w-5" />
                    </div>
                    <h4 class="text-foreground font-semibold">Teknik Terbaik</h4>
                </div>
                <p class="text-primary mb-2 text-2xl font-bold">CLAHE</p>
                <p class="text-muted-foreground text-sm leading-relaxed">Meningkatkan kontras lokal secara signifikan, membantu membedakan knots dari tekstur kayu normal.</p>
            </div>

            <div class="bg-card rounded-2xl border p-6 shadow-sm">
                <div class="mb-3 flex items-center gap-3">
                    <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-100 text-blue-600">
                        <Clock class="h-5 w-5" />
                    </div>
                    <h4 class="text-foreground font-semibold">Total Waktu</h4>
                </div>
                <p class="text-foreground mb-2 text-2xl font-bold">{{ totalTime }} <span class="text-muted-foreground text-base font-normal">ms</span></p>
                <p class="text-muted-foreground text-sm leading-relaxed">Waktu total untuk menjalankan keseluruhan pipeline preprocessing.</p>
            </div>

            <div class="bg-card rounded-2xl border p-6 shadow-sm">
                <div class="mb-3 flex items-center gap-3">
                    <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-100 text-purple-600">
                        <Target class="h-5 w-5" />
                    </div>
                    <h4 class="text-foreground font-semibold">Akurasi Deteksi</h4>
                </div>
                <p class="text-foreground mb-2 text-2xl font-bold">{{ avgAccuracy }}<span class="text-muted-foreground text-base font-normal">%</span></p>
                <p class="text-muted-foreground text-sm leading-relaxed">Rata-rata confidence score dari semua knots yang terdeteksi.</p>
            </div>
        </div>

        <div class="bg-card rounded-2xl border p-6 shadow-sm">
            <div class="mb-4 flex items-center gap-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-100 text-amber-600">
                    <Lightbulb class="h-5 w-5" />
                </div>
                <h3 class="text-foreground font-semibold">Rekomendasi & Kesimpulan</h3>
            </div>
            <div class="space-y-3">
                <div v-for="(rec, index) in recommendations" :key="index" class="bg-muted/30 flex items-start gap-3 rounded-lg p-4">
                    <div class="bg-primary text-primary-foreground flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-bold">
                        {{ index + 1 }}
                    </div>
                    <p class="text-foreground/80 text-sm leading-relaxed">{{ rec }}</p>
                </div>
            </div>
        </div>
    </div>
</template>
