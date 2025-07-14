<script setup>
const props = defineProps({
  label: { type: String, required: true },
  icon: { type: Object, default: null }
});
</script>

<template>
  <button class="button" :disabled="$attrs.disabled">
    <div class="flex gap-2">
      <div class="self-center">{{ props.label }}</div>
      <component class="self-center" v-if="props.icon" :is="props.icon" style="font-size: 1em" />
    </div>
  </button>
</template>
