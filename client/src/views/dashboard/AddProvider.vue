<script setup>
import { ref, watch, nextTick } from "vue";
import Popup from "@/components/Popup.vue";
import http from "@/lib/http";

const emit = defineEmits(["on-close", "on-added"]);

const props = defineProps({
  show: Boolean
});

const providerName = ref("");
const providerInputRef = ref(null);
const inviteCode = ref("");
const error = ref("");

const clearForm = () => {
  providerName.value = "";
  inviteCode.value = "";
  error.value = "";
};

watch(
  () => props.show,
  async (val) => {
    if (val) {
      await nextTick();
      providerInputRef.value?.focus();
    }
  }
);

const onCreate = async () => {
  error.value = "";
  const { data, error: apiError } = await http.post("/api/data_providers/create", { name: providerName.value });
  if (apiError) {
    error.value = apiError;
    return;
  }
  clearForm();
  emit("on-added");
};

const onClose = () => {
  clearForm();
  emit("on-close");
};
</script>

<template>
  <Popup :show="show" @on-close="onClose" title="Create a data provider">
    <div class="flex flex-col gap-4 p-5 min-w-[300px]">
      <div>
        <label class="block font-semibold mb-1">Name</label>
        <input v-model="providerName" ref="providerInputRef" type="text" placeholder="Provider name" class="input w-full" @keydown.enter="onCreate" />
      </div>
      <div v-if="error" class="text-nord11 text-center mt-2">{{ error }}</div>
      <button class="button w-full mt-2" @click="onCreate" :disabled="!providerName.trim()">Create provider</button>
    </div>
  </Popup>
</template>
