<script setup>
import { ref, watch, nextTick, computed } from "vue";
import Popup from "@/components/Popup.vue";
import http from "@/lib/http";

const emit = defineEmits(["on-close", "on-added"]);

const props = defineProps({
  show: Boolean,
  typeOptions: { type: Array, default: () => [] },
  aggregationOptions: { type: Array, default: () => [] },
  componentOptions: { type: Array, default: () => [] },
  currentProvider: { type: Object, default: null }
});

const sourceName = ref("");
const sourceInputRef = ref(null);
const sourceType = ref("");
const sourceComponent = ref("");
const error = ref("");

// Use props.typeOptions, props.aggregationOptions, props.componentOptions
const selectedAggregations = ref([]);

const clearForm = () => {
  sourceName.value = "";
  sourceType.value = "";
  sourceComponent.value = "";
  selectedAggregations.value = [];
  error.value = "";
};

watch(
  () => props.show,
  async (val) => {
    if (val) {
      await nextTick();
      sourceInputRef.value?.focus();
    }
  }
);

const isCreateDisabled = computed(() => {
  return !sourceName.value.trim() || !sourceType.value || !sourceComponent.value;
});

const onCreate = async () => {
  error.value = "";
  const payload = {
    name: sourceName.value,
    provider_id: props.currentProvider?.id,
    type_id: sourceType.value,
    component_id: sourceComponent.value,
    aggregation_type_ids: selectedAggregations.value
  };
  const { data, error: apiError } = await http.post("/api/data_sources/create", payload);
  if (apiError || (data && data.success === false)) {
    error.value = apiError || "Failed to create data source.";
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
  <Popup :show="show" @on-close="onClose" title="Create a data source">
    <div class="flex flex-col gap-4 p-5 min-w-[300px]">
      <div>
        <label class="block font-semibold mb-1">Name</label>
        <input v-model="sourceName" ref="sourceInputRef" type="text" placeholder="Data source name" class="input w-full" />
      </div>
      <div>
        <label class="block font-semibold mb-1">Type</label>
        <select v-model="sourceType" class="input w-full">
          <option value="" disabled>Select type</option>
          <option v-for="opt in props.typeOptions" :key="opt.id" :value="opt.id">{{ opt.name }}</option>
        </select>
      </div>
      <div>
        <label class="block font-semibold mb-1">Component</label>
        <select v-model="sourceComponent" class="input w-full">
          <option value="" disabled>Select component</option>
          <option v-for="opt in props.componentOptions" :key="opt.id" :value="opt.id">{{ opt.name }}</option>
        </select>
      </div>
      <div>
        <label class="block font-semibold mb-1">Aggregation Types</label>
        <div class="flex flex-col gap-1">
          <label v-for="opt in props.aggregationOptions" :key="opt.id" class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" :value="opt.id" v-model="selectedAggregations" class="accent-nord3" />
            <span>{{ opt.name }}</span>
          </label>
        </div>
      </div>
      <div v-if="error" class="text-nord11 text-center mt-2">{{ error }}</div>
      <button class="button w-full mt-2" @click="onCreate" :disabled="isCreateDisabled">Create data source</button>
    </div>
  </Popup>
</template>
