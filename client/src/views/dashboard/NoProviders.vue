<script setup>
import { ref } from "vue";

const emit = defineEmits(["on-click"]);
</script>

<template>
  <div class="flex flex-col items-center justify-center h-full gap-6 text-center">
    <div>
      <div class="text-2xl font-bold mb-2">No Data Providers Yet</div>
      <div class="text-main3 max-w-md mx-auto">Create a new provider to start tracking, sharing, and collaborating on your data—or join an existing one if you’ve been invited.</div>
    </div>
    <button class="button !p-4 font-semibold text-lg" @click="emit('on-click')">Create or join a data provider</button>
  </div>
</template>
