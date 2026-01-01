<script setup>
const props = defineProps({
    progress: {
        type: Number,
        default: 0,
        validator: (value) => value >= 0 && value <= 100,
    },
    class: {
        type: String,
        default: "",
    },
});
</script>

<template>
    <div :class="['bg-muted h-1 overflow-hidden rounded-full', props.class]">
        <div class="bg-primary h-full rounded-full transition-all duration-300" :style="{ width: `${progress}%` }"></div>
    </div>
</template>
