<script setup>
const props = defineProps({
    variant: {
        type: String,
        default: "info",
        validator: (value) => ["success", "warning", "error", "info"].includes(value),
    },
    class: {
        type: String,
        default: "",
    },
});

const variantClasses = {
    success: "bg-green-500/10 text-green-500",
    warning: "bg-amber-500/10 text-amber-500",
    error: "bg-red-500/10 text-red-500",
    info: "bg-blue-500/10 text-blue-500",
}[props.variant];
</script>

<template>
    <span :class="['inline-flex items-center rounded-full px-2 py-1 text-xs font-medium', variantClasses, props.class]">
        <slot />
    </span>
</template>
