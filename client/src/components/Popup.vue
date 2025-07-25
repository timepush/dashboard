<script setup>
import { onMounted, onUnmounted } from "vue";
import IconClose from "~icons/uil/times";

const emit = defineEmits(["on-close"]);

const props = defineProps({
  show: Boolean,
  title: String
});

const onClose = () => {
  emit("on-close");
};

const handleKeydown = (event) => {
  if (event.key === "Escape") {
    emit("on-close"); // Emit the event when ESC is pressed
  }
};

onMounted(() => {
  window.addEventListener("keydown", handleKeydown);
});

onUnmounted(() => {
  window.removeEventListener("keydown", handleKeydown);
});
</script>

<script>
export default {
  inheritAttrs: false
};
</script>

<template>
  <Transition name="popup-fade" appear>
    <div v-if="show" class="absolute top-0 bottom-0 left-0 right-0 z-[100]">
      <Transition name="popup-backdrop" appear>
        <div v-if="show" class="absolute inset-0 bg-black/30" @click.self="onClose"></div>
      </Transition>
      <Transition name="popup-modal" appear>
        <div v-if="show" class="absolute top-1/2 left-1/2 p-4 border border-nord4 rounded-lg flex flex-col gap-2 bg-gray-50 shadow z-[110] -translate-x-1/2 -translate-y-1/2 min-w-96 text-base" v-bind="$attrs">
          <div class="select-none font-bold flex justify-between">
            <div>{{ title }}</div>
            <div class="flex items-center gap-2">
              <icon-close class="self-center text-nord3 hover:cursor-pointer hover:text-nord0" @click="onClose" />
            </div>
          </div>
          <div class="border border-gray-300"></div>
          <div class="h-full"><slot></slot></div>
        </div>
      </Transition>
    </div>
  </Transition>
</template>

<style scoped>
.popup-fade-enter-active,
.popup-fade-leave-active {
  transition: opacity 0.2s;
}
.popup-fade-enter-from,
.popup-fade-leave-to {
  opacity: 0;
}
.popup-backdrop-enter-active,
.popup-backdrop-leave-active {
  transition: opacity 0.2s;
}
.popup-backdrop-enter-from,
.popup-backdrop-leave-to {
  opacity: 0;
}
.popup-modal-enter-active,
.popup-modal-leave-active {
  transition: opacity 0.2s;
}
.popup-modal-enter-from,
.popup-modal-leave-to {
  opacity: 0;
}
</style>
