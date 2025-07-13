<script setup>
const props = defineProps({
  label: { type: String, required: true },
  icon: { type: Object, default: null }
});
</script>

<template>
  <button class="button" :disabled="$attrs.disabled">
    <span>{{ props.label }}</span>
    <div class="flex justify-center items-center flex-shrink-0">
      <component v-if="props.icon" :is="props.icon" style="font-size: 1em" />
    </div>
  </button>
</template>
