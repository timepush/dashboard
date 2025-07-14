<script setup>
import { ref } from "vue";
import Popup from "@/components/Popup.vue";
import http from "@/lib/http";

const emit = defineEmits(["on-close", "on-added"]);

const props = defineProps({
  show: Boolean
});

const providerName = ref("");
const inviteCode = ref("");
const error = ref("");

const onCreate = async () => {
  error.value = "";
  const { data, error: apiError } = await http.post("/api/data_providers/create", { name: providerName.value });
  if (apiError) {
    error.value = apiError;
    return;
  }
  emit("on-added");
};

const onJoin = () => {
  error.value = "Invitation is not implemented yet.";
  // TODO: Call API to join provider
  // emit("on-close");
};
</script>

<template>
  <Popup :show="show" @on-close="emit('on-close')" title="Create or join a data provider">
    <div class="flex flex-col md:flex-row gap-6 items-stretch p-5">
      <div class="flex-1 flex flex-col items-stretch">
        <div class="font-semibold mb-2">Create a new provider</div>
        <input v-model="providerName" type="text" placeholder="Provider name" class="input w-full mb-2" @keydown.enter="onCreate" />
        <button class="button w-full" @click="onCreate" :disabled="!providerName.trim()">Create provider</button>
      </div>
      <div class="hidden md:flex flex-col items-center justify-center">
        <div class="w-px h-full bg-nord3/30" style="min-height: 80px"></div>
      </div>
      <div class="flex md:hidden flex-row items-center justify-center my-4">
        <div class="h-px w-12 bg-nord3/30"></div>
      </div>
      <div class="flex-1 flex flex-col items-stretch">
        <div class="font-semibold mb-2 flex-nowrap">Join with invitation code</div>
        <input v-model="inviteCode" type="text" placeholder="Invitation code" class="input w-full mb-2" @keydown.enter="onJoin" />
        <button class="button w-full" @click="onJoin" :disabled="!inviteCode.trim()">Join provider</button>
      </div>
    </div>
    <div v-if="error" class="text-nord11 mt-2 text-center">{{ error }}</div>
  </Popup>
</template>
