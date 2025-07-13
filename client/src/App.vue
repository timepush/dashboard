<script setup>
import TopBar from "@/components/TopBar.vue";
</script>

<template>
  <div class="h-full flex flex-col overflow-hidden">
    <TopBar />
    <router-view />
  </div>
</template>

<style></style>
