<script setup>
import { ref } from "vue";

const props = defineProps({
    class: {
        type: String,
        default: "",
    },
});

const emit = defineEmits(["click", "drop"]);

const isDragover = ref(false);

function handleDrop(event) {
    isDragover.value = false;
    emit("drop", event);
}
</script>

<template>
    <div
        :class="[
            'border-border bg-muted/50 cursor-pointer rounded-3xl border-2 border-dashed px-16 py-20 text-center transition-all duration-300',
            'hover:border-primary hover:bg-primary/5',
            isDragover && 'border-primary bg-primary/10 scale-[1.02]',
            props.class,
        ]"
        @dragover.prevent="isDragover = true"
        @dragleave="isDragover = false"
        @drop.prevent="handleDrop"
        @click="$emit('click')"
    >
        <slot />
    </div>
</template>

