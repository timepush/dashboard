<script setup>
import { signout } from "@/lib/auth";
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import http from "@/lib/http";
import NoProviders from "./NoProviders.vue";
import IconMenu from "~icons/material-symbols/menu-rounded";
import IconCheck from "~icons/material-symbols/check-rounded";
import ButtonWithMenu from "@/components/ButtonWithMenu.vue";
import AddProvider from "./AddProvider.vue";

const router = useRouter();

const providers = ref(null);
const currentProvider = ref(null);
const showAddProvider = ref(false);

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

onMounted(fetchProviders);

const onSignOut = async () => {
  await signout();
  router.push("/signin");
};

const onProvidersAdded = () => {
  fetchProviders();
  showAddProvider.value = false;
};

const setCurrentProvider = async (provider) => {
  if (provider.current) return;
  await http.post("/api/data_providers/set_current", { provider_id: provider.id });
  providers.value = providers.value.map((p) => ({ ...p, current: p.id === provider.id }));
  currentProvider.value = { ...provider, current: true };
};
</script>

<template>
  <div class="flex h-full flex-col gap-4">
    <!-- <button class="button" @click="onSignOut">Sign out</button> -->
    <AddProvider :show="showAddProvider" @on-close="showAddProvider = false" @on-added="onProvidersAdded" />

    <NoProviders v-if="providers?.length === 0" @on-click="showAddProvider = true" />

    <div v-if="providers?.length > 0" class="flex flex-col p-4">
      <div class="flex justify-between">
        <div class="font-semibold text-2xl">{{ currentProvider.name }}</div>
        <ButtonWithMenu :label="'Data Providers'" :icon="IconMenu">
          <div class="flex flex-col gap-1">
            <table class="w-full">
              <tr v-for="provider in providers" :key="provider.id" class="hover:bg-gray-200/50 cursor-pointer" @click="setCurrentProvider(provider)">
                <td class="pl-2 w-10">
                  <IconCheck v-if="provider.current" class="text-nord14 text-xl" />
                </td>
                <td class="py-1">{{ provider.name }}</td>
                <td class="pl-2 pr-2 py-1 text-sm">{{ provider.role }}</td>
              </tr>
            </table>
            <!-- BORDER -->
            <div class="border-t border-nord4 px-4 py-2">
              <button class="button text-sm w-full" @click="showAddProvider = true">Add data provider</button>
            </div>
          </div>
        </ButtonWithMenu>
      </div>
    </div>
  </div>
</template>

<style></style>
