<script setup>
import { signout } from "@/lib/auth";
import { useRouter } from "vue-router";
import { ref, onMounted, watch } from "vue";
import http from "@/lib/http";
import NoProviders from "./NoProviders.vue";
import NoSources from "./NoSources.vue";
import AddProvider from "./AddProvider.vue";
import ProviderMenu from "./ProviderMenu.vue";

const router = useRouter();

const providers = ref(null);
const currentProvider = ref(null);

const showAddProvider = ref(false);
const dataSources = ref([]);

// 1. Fetch providers and set current provider
const fetchProviders = async () => {
  const { data, error: err } = await http.get("/api/data_providers");
  if (err) {
    providers.value = [];
    currentProvider.value = null;
    return;
  }
  const current = data.find((p) => p.current);
  currentProvider.value = current || null;
  providers.value = data;
};

// 2. Fetch data sources for a provider
const fetchDataSources = async (providerId) => {
  if (!providerId) {
    dataSources.value = [];
    return;
  }
  const { data, error } = await http.get(`/api/data_sources?provider_id=${providerId}`);
  dataSources.value = error ? [] : data;
};

// 3. Set current provider and update state
const setCurrentProvider = async (provider) => {
  if (provider.current) return;
  await http.post("/api/data_providers/set_current", { provider_id: provider.id });
  providers.value = providers.value.map((p) => ({ ...p, current: p.id === provider.id }));
  currentProvider.value = { ...provider, current: true };
};

// 4. Handler for when providers are added
const onProvidersAdded = () => {
  fetchProviders();
  showAddProvider.value = false;
};

// 5. Sign out
const onSignOut = async () => {
  await signout();
  router.push("/signin");
};

// 6. Lifecycle and watchers
onMounted(fetchProviders);
watch(
  currentProvider,
  (newVal) => {
    fetchDataSources(newVal?.id);
  },
  { immediate: true }
);
</script>

<template>
  <div class="flex h-full flex-col gap-4">
    <!-- <button class="button" @click="onSignOut">Sign out</button> -->
    <AddProvider :show="showAddProvider" @on-close="showAddProvider = false" @on-added="onProvidersAdded" />

    <NoProviders v-if="providers?.length === 0" @on-click="showAddProvider = true" />

    <div v-if="providers?.length > 0" class="flex flex-col p-4 h-full">
      <!-- Top bar -->
      <div class="flex justify-between">
        <div class="font-semibold text-2xl">{{ currentProvider.name }}</div>
        <ProviderMenu :providers="providers" :currentProvider="currentProvider" @set-current="setCurrentProvider" @add-provider="() => (showAddProvider = true)" />
      </div>
      <!-- Content -->
      <div class="flex-1 flex flex-col h-full">
        <NoSources v-if="dataSources?.length === 0" />
      </div>
    </div>
  </div>
</template>

<style></style>
