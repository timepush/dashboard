<script setup>
import Button from "@/components/Button.vue";
import Card from "@/components/Card.vue";
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { signin } from "@/lib/auth";

const email = ref("");
const password = ref("");
const message = ref("");
const loading = ref(false);
const router = useRouter();

const isDisabled = computed(() => loading.value || !email.value || !password.value);

const doSignin = async () => {
  message.value = "";
  loading.value = true;
  const { data, error } = await signin(email.value, password.value);
  loading.value = false;
  if (error) {
    message.value = error.message ? error.message : String(error);
    return;
  }
  router.push("/dashboard");
};
</script>

<template>
  <div class="flex flex-col items-center justify-center mt-10 w-full p-4">
    <div class="flex flex-col w-full md:w-3/5">
      <div class="font-semibold text-2xl mb-4">Sign in to your account</div>

      <Card class="m-auto !gap-0 !p-6">
        <div class="flex flex-col md:flex-row gap-4 mb-4">
          <input v-model="email" placeholder="Email" class="input w-full md:w-1/2" autocomplete="email" type="email" autocorrect="off" />
          <input v-model="password" placeholder="Password" class="input w-full md:w-1/2" autocomplete="current-password" type="password" autocorrect="off" />
        </div>
        <button class="button w-full mt-2" @click="doSignin" :disabled="isDisabled">Sign in</button>
        <div class="text-nord11 text-center flex-wrap break-words mt-2">{{ message }}</div>
      </Card>

      <button class="button w-full mt-8 !text-sm" @click="() => $router.push('/signup')">Don't have an account? Sign up</button>
    </div>
  </div>
</template>
