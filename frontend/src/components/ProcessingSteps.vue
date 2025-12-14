<script setup>
import { ref } from "vue";
import { Layers, LayoutGrid, ChevronsRight, Package, ArrowRight, X } from "lucide-vue-next";

defineProps({
    steps: {
        type: Array,
        default: () => [],
    },
});

const viewMode = ref("grid");
const selectedStep = ref(null);
</script>

<template>
    <div class="flex flex-col gap-6">
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="bg-primary/10 flex h-10 w-10 items-center justify-center rounded-xl">
                    <Layers class="text-primary h-5 w-5" />
                </div>
                <h2 class="text-foreground text-2xl font-semibold">Processing Pipeline</h2>
            </div>
            <div class="flex items-center gap-2">
                <button @click="viewMode = 'grid'" :class="['rounded-lg p-2 transition-colors', viewMode === 'grid' ? 'bg-primary/10 text-primary' : 'text-muted-foreground hover:bg-muted']">
                    <LayoutGrid class="h-5 w-5" />
                </button>
                <button @click="viewMode = 'flow'" :class="['rounded-lg p-2 transition-colors', viewMode === 'flow' ? 'bg-primary/10 text-primary' : 'text-muted-foreground hover:bg-muted']">
                    <ChevronsRight class="h-5 w-5" />
                </button>
            </div>
        </div>

        <div v-if="!steps || steps.length === 0" class="bg-card rounded-2xl border p-8 py-16 text-center shadow-sm">
            <div class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-gray-100">
                <Package class="h-8 w-8 text-gray-400" />
            </div>
            <p class="text-muted-foreground">Upload gambar untuk melihat pipeline processing</p>
        </div>

        <div v-else-if="viewMode === 'grid'" class="grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
            <div
                v-for="(step, index) in steps"
                :key="step.step"
                class="animate-slide-up bg-card hover:border-primary-500 cursor-pointer rounded-2xl border p-5 shadow-sm transition-all hover:shadow-md"
                :style="{ animationDelay: `${index * 100}ms` }"
                @click="selectedStep = step"
            >
                <div class="mb-4 flex items-center gap-3">
                    <div class="bg-primary/10 text-primary flex h-9 w-9 items-center justify-center rounded-full text-sm font-semibold">
                        {{ step.step }}
                    </div>
                    <div>
                        <h4 class="text-foreground text-sm font-semibold">{{ step.name }}</h4>
                        <p class="text-muted-foreground text-xs">{{ step.technique }}</p>
                    </div>
                </div>

                <div class="relative mb-4 aspect-video overflow-hidden rounded-lg bg-gray-100">
                    <img :src="step.image" :alt="step.name" class="h-full w-full object-cover" />
                </div>

                <p class="text-muted-foreground line-clamp-2 text-sm">
                    {{ step.description }}
                </p>
            </div>
        </div>

        <div v-else class="overflow-x-auto pb-4">
            <div class="flex min-w-max items-start gap-3">
                <template v-for="(step, index) in steps" :key="step.step">
                    <div class="bg-card hover:border-primary-500 w-52 shrink-0 cursor-pointer rounded-2xl border p-4 shadow-sm transition-all hover:shadow-md" @click="selectedStep = step">
                        <div class="mb-3 flex items-center gap-2">
                            <div class="bg-primary text-primary-foreground flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold">
                                {{ step.step }}
                            </div>
                            <span class="text-primary text-xs font-medium">{{ step.technique }}</span>
                        </div>

                        <div class="mb-3 aspect-square overflow-hidden rounded-lg bg-gray-100">
                            <img :src="step.image" :alt="step.name" class="h-full w-full object-cover" />
                        </div>

                        <h4 class="text-foreground text-center text-sm font-medium">
                            {{ step.name }}
                        </h4>
                    </div>

                    <div v-if="index < steps.length - 1" class="text-primary flex shrink-0 items-center self-center">
                        <ArrowRight class="h-8 w-8" />
                    </div>
                </template>
            </div>
        </div>

        <Teleport to="body">
            <div v-if="selectedStep" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="selectedStep = null">
                <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="selectedStep = null"></div>

                <div class="animate-slide-up relative max-h-[90vh] w-full max-w-3xl overflow-hidden rounded-2xl bg-white shadow-2xl">
                    <button @click="selectedStep = null" class="absolute top-4 right-4 z-10 rounded-full bg-gray-100 p-2 transition-colors hover:bg-gray-200">
                        <X class="h-5 w-5 text-gray-600" />
                    </button>

                    <div class="aspect-video bg-gray-100">
                        <img :src="selectedStep.image" :alt="selectedStep.name" class="h-full w-full object-contain" />
                    </div>

                    <div class="p-6">
                        <div class="mb-4 flex items-center gap-3">
                            <div class="bg-primary/10 text-primary flex h-10 w-10 items-center justify-center rounded-full font-bold">
                                {{ selectedStep.step }}
                            </div>
                            <div>
                                <h3 class="text-foreground text-xl font-bold">{{ selectedStep.name }}</h3>
                                <p class="text-primary text-sm">{{ selectedStep.technique }}</p>
                            </div>
                        </div>

                        <p class="text-muted-foreground mb-4">{{ selectedStep.description }}</p>

                        <div v-if="selectedStep.parameters && Object.keys(selectedStep.parameters).length > 0">
                            <h4 class="text-foreground mb-2 font-semibold">Parameters:</h4>
                            <div class="rounded-lg bg-gray-50 p-4">
                                <div v-for="(value, key) in selectedStep.parameters" :key="key" class="flex justify-between border-b border-gray-100 py-1.5 text-sm last:border-0">
                                    <span class="text-muted-foreground">{{ key }}:</span>
                                    <span class="text-foreground font-mono">{{ value }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Teleport>
    </div>
</template>
