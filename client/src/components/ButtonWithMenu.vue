<script setup>
import { ref } from "vue";
import { onClickOutside } from "@vueuse/core";
import ButtonWithIcon from "@/components/ButtonWithIcon.vue";

const props = defineProps({
  label: { type: String, required: true },
  icon: { type: Object, default: null }
});

const isOpen = ref(false);
const rootRef = ref(null);

const toggleMenu = () => {
  isOpen.value = !isOpen.value;
};
const closeMenu = () => {
  isOpen.value = false;
};

onClickOutside(rootRef, () => {
  isOpen.value = false;
});

defineExpose({ closeMenu });
</script>

<template>
  <div class="relative flex flex-col items-end" ref="rootRef">
    <div class="w-full">
      <ButtonWithIcon :label="props.label" :icon="props.icon" @click="toggleMenu" />
    </div>
    <Transition name="dropdown-fade">
      <div v-if="isOpen" class="absolute right-0 top-full mt-2 w-max border border-nord4 rounded shadow bg-white/50 z-50">
        <slot />
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.dropdown-fade-enter-active {
  transition: opacity 0.15s cubic-bezier(0.4, 0, 0.2, 1), transform 0.18s cubic-bezier(0.4, 0, 0.2, 1);
}
.dropdown-fade-leave-active {
  transition: opacity 0.12s cubic-bezier(0.4, 0, 0.2, 1), transform 0.16s cubic-bezier(0.4, 0, 0.2, 1);
}
.dropdown-fade-enter-from {
  opacity: 0;
  transform: translateY(-8px) scaleY(0.98);
}
.dropdown-fade-enter-to {
  opacity: 1;
  transform: translateY(0) scaleY(1);
}
.dropdown-fade-leave-from {
  opacity: 1;
  transform: translateY(0) scaleY(1);
}
.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px) scaleY(0.98);
}
</style>
