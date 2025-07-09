<script setup>
import Button from '../../components/Button.vue';
import Container from '../../components/Container.vue';
import TimepushLogo from '../../components/TimepushLogo.vue';

const onGetStarted = () => {
  // Replace with navigation or signup logic
  window.location.href = '/signup';
};
</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-main0 text-main4 px-4 gap-4">
    <!-- <Container class="w-full max-w-2xl flex flex-col items-center py-12 gap-8 "> -->
    <div class="flex flex-col items-center gap-4">
      <h1 class="text-3xl md:text-5xl font-bold text-center leading-tight">Effortless Data Tracking</h1>
      <p class="text-main3 text-lg md:text-xl text-center max-w-xl">
        Blah blah blah. blah blah blah.<br>
        blah blah blah.<br>
        Blah blah blah. blah blah blah
      </p>
    </div>
    <Button label="Get Started" class="w-full max-w-xs text-lg py-3" @click="onGetStarted" />

    <!-- </Container> -->
  </div>
</template>