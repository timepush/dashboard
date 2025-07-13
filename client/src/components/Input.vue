<template>
  <input :value="modelValue" @input="$emit('update:modelValue', $event.target.value)" v-bind="$attrs" class="px-2 py-1 rounded inline-block border border-nord4 bg-white focus:outline-none" />
</template>

<script setup>
defineProps(["modelValue"]);
</script>
