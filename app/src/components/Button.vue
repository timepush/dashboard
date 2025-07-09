<script setup>
const props = defineProps({
  label: { type: String, required: true },
  icon: { type: Object, default: null }
});
</script>

<template>
  <button class="cursor-pointer rounded-lg bg-main3 hover:bg-main4 transition-colors px-4 py-2 font-semibold text-main1 flex items-center justify-center min-w-fit text-nowrap gap-2">
    <span>{{ props.label }}</span>
    <div class="flex justify-center items-center flex-shrink-0">
      <component v-if="props.icon" :is="props.icon" class="ml-1" style="font-size: 1.5em" />
    </div>
  </button>
</template>