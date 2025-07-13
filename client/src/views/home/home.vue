<script setup>
import { useRouter } from "vue-router";
import Button from "@/components/Button.vue";
import IconBell from "~icons/bx/bxs-chevrons-right";

const router = useRouter();
const goToSignin = () => {
  router.push({ name: "signin" });
};
</script>

<template>
  <div class="flex items-center justify-center h-full">
    <Button label="Get Started" :icon="IconBell" @click="goToSignin" />
  </div>
</template>

<style></style>
