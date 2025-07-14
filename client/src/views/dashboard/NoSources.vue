<script setup>
const emit = defineEmits(["on-click"]);
</script>

<template>
  <div class="flex flex-col items-center justify-center h-full gap-6 text-center">
    <div>
      <div class="text-2xl font-bold mb-2">No Data Sources Yet</div>
      <div class="text-main3 max-w-md mx-auto">Create a new data source to start tracking, sharing, and collaborating on your data.</div>
    </div>
    <button class="button !p-4 font-semibold text-lg" @click="emit('on-click')">Create a data source</button>
  </div>
</template>
