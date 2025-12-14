<script setup>
const props = defineProps({
    class: {
        type: String,
        default: "",
    },
});
</script>

<template>
    <div :class="['border-border bg-card rounded-2xl border p-8 shadow-md transition-all duration-300 hover:shadow-lg', props.class]">
        <slot />
    </div>
</template>
