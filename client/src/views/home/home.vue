<script setup>
import { useRouter } from "vue-router";
import ButtonWithIcon from "@/components/ButtonWithIcon.vue";
import IconBell from "~icons/bx/bxs-chevrons-right";

const router = useRouter();
const goToDashboard = () => {
  router.push({ name: "dashboard" });
};
</script>

<template>
  <div class="flex items-center justify-center h-full">
    <ButtonWithIcon label="Get Started" :icon="IconBell" @click="goToDashboard" />
  </div>
</template>

<style></style>
