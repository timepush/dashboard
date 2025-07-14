<script setup>
import ButtonWithMenu from "@/components/ButtonWithMenu.vue";
import IconMenu from "~icons/material-symbols/menu-rounded";
import IconCheck from "~icons/material-symbols/check-rounded";
const props = defineProps({
  providers: Array,
  currentProvider: Object
});
const emit = defineEmits(["set-current", "add-provider"]);
import { ref } from "vue";
const menuRef = ref(null);
const handleSetCurrent = (provider) => {
  emit("set-current", provider);
  menuRef.value?.closeMenu();
};
const handleAddProvider = () => {
  emit("add-provider");
  menuRef.value?.closeMenu();
};
</script>

<template>
  <ButtonWithMenu ref="menuRef" :label="'Data Providers'" :icon="IconMenu">
    <div class="flex flex-col gap-1">
      <table class="w-full">
        <tr v-for="provider in providers" :key="provider.id" class="hover:bg-gray-200/50 cursor-pointer" @click="handleSetCurrent(provider)">
          <td class="pl-2 w-10">
            <IconCheck v-if="provider.current" class="text-nord14 text-xl" />
          </td>
          <td class="py-1">{{ provider.name }}</td>
          <td class="pl-2 pr-2 py-1 text-sm">{{ provider.role }}</td>
        </tr>
      </table>
      <div class="border-t border-nord4 px-4 py-2">
        <button class="button text-sm w-full" @click.stop="handleAddProvider">Add data provider</button>
      </div>
    </div>
  </ButtonWithMenu>
</template>
