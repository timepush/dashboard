<script setup>
import { signout } from "@/lib/auth";
import { useRouter } from "vue-router";

const router = useRouter();

const onSignOut = async () => {
  await signout();
  router.push("/signin");
};
</script>

<template>
  <div class="flex items-center justify-center h-full flex-col gap-4">
    <div>Hello, welcome to the home page!</div>
    <button class="button" @click="onSignOut">Sign out</button>
  </div>
</template>

<style></style>
