<script setup>
import { signout } from "@/lib/auth";
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import http from "@/lib/http";

const router = useRouter();
const providers = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchProviders = async () => {
  loading.value = true;
  error.value = null;
  const { data, error: err } = await http.get("/api/data_providers");
  if (err) {
    error.value = err;
    providers.value = [];
  } else {
    providers.value = data;
  }
  loading.value = false;
};

onMounted(fetchProviders);

const onSignOut = async () => {
  await signout();
  router.push("/signin");
};
</script>

<template>
  <div class="flex items-center justify-center h-full flex-col gap-4">
    <div>Hello, welcome to the home page!</div>
    <button class="button" @click="onSignOut">Sign out</button>
    <div v-if="loading">Loading providers...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else>
      <div v-if="providers.length === 0">No providers found.</div>
      <ul v-else class="mt-4 space-y-2">
        <li v-for="provider in providers" :key="provider.id" class="p-2 rounded bg-main2 text-main4">
          <div class="font-semibold">{{ provider.name }}</div>
          <div class="text-xs text-main3">Role: {{ provider.role }}</div>
        </li>
      </ul>
    </div>
  </div>
</template>

<style></style>
