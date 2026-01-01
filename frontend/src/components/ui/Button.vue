<script setup>
import { LoaderCircle } from "lucide-vue-next";

const props = defineProps({
    variant: {
        type: String,
        default: "primary",
        validator: (value) => ["primary", "secondary", "outline", "ghost"].includes(value),
    },
    disabled: {
        type: Boolean,
        default: false,
    },
    loading: {
        type: Boolean,
        default: false,
    },
    class: {
        type: String,
        default: "",
    },
});

const variantClasses = {
    primary:
        "bg-primary text-primary-foreground shadow-md hover:bg-primary/90 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-primary/30 active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0",
    secondary: "bg-secondary text-secondary-foreground border border-border hover:bg-secondary/80 disabled:opacity-50 disabled:cursor-not-allowed",
    outline: "bg-transparent text-primary border-2 border-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-50 disabled:cursor-not-allowed",
    ghost: "bg-transparent text-muted-foreground hover:bg-accent disabled:opacity-50 disabled:cursor-not-allowed",
}[props.variant];
</script>

<template>
    <button :class="['inline-flex cursor-pointer items-center justify-center gap-2 rounded-full border-none px-3.5 py-3 text-sm font-medium transition-all duration-150', variantClasses, props.class]" :disabled="disabled || loading">
        <LoaderCircle v-if="loading" class="h-5 w-5 animate-spin" />
        <slot />
    </button>
</template>
