<script setup>
import Container from "../../components/Container.vue";
import Button from "../../components/Button.vue";
import GoogleIcon from "~icons/cbi/google-logo-circle";
import FacebookIcon from "~icons/mdi/facebook";
import { ref } from "vue";

const email = ref("");
const password = ref("");

const onClick = () => {
  console.log("Button Clicked!");
};
</script>

<template>
  <div class="flex flex-col items-center justify-center h-screen w-full">
    <div class="flex flex-col w-8/12">
      <div class="flex flex-col md:flex-row font-semibold gap-4">
        <Button @click="onClick" class="w-full md:w-1/2" label="Sign in with Facebook" :icon="FacebookIcon" />
        <Button @click="onClick" class="w-full md:w-1/2" label="Sign in with Google" :icon="GoogleIcon" />
      </div>
      <div class="flex items-center w-full my-8 gap-2">
        <hr class="flex-1 border-main1 border-t-2" />
        <span class="text-main2 font-semibold text-sm">OR</span>
        <hr class="flex-1 border-main1 border-t-2" />
      </div>

      <Container>
        <div class="font-semibold mb-4">Sign in with email</div>
        <div class="flex flex-col md:flex-row gap-4 mb-4">
          <input v-model="email" placeholder="Email" class="w-full md:w-1/2" autocomplete="email" type="email" />
          <input v-model="password" placeholder="Password" class="w-full md:w-1/2" autocomplete="new-password" type="password" />
        </div>
        <Button label="Sign in" class="w-full mt-2" @click="onClick" />
        <div class="w-full text-center mt-4 ">
          <a href="" class="text-main2 text-sm hover:underline  ">Forgot password?</a>
        </div>
      </Container>

      <Button label="No account? Sign up" class="w-full mt-8 !text-sm !bg-main1 !text-main3 hover:!bg-main2" @click="() => $router.push('/signup')" />
    </div>
  </div>
</template>