<script setup>
import Card from "@/components/Card.vue";
import { ref, computed } from "vue";
import { signup as authSignup } from "@/lib/auth";

const firstName = ref("");
const lastName = ref("");
const email = ref("");
const password = ref("");
const message = ref("");
const loading = ref(false);

const isDisabled = computed(() => loading.value || !firstName.value || !lastName.value || !email.value || !password.value);

const doSignup = async () => {
  message.value = "";
  loading.value = true;
  const { data, error } = await authSignup(firstName.value, lastName.value, email.value, password.value);
  loading.value = false;
  if (error) {
    message.value = error.message ? error.message : String(error);
    return;
  }

  message.value = "Account created successfully! Please verify your email to complete the signup process.";
};
</script>

<template>
  <div class="flex flex-col items-center justify-center mt-10 w-full p-4">
    <div class="flex flex-col w-full md:w-3/5">
      <div class="font-semibold text-2xl mb-4">Create an account</div>

      <Card class="m-auto !gap-0 !p-6">
        <div class="flex flex-col md:flex-row gap-4 mb-4">
          <input v-model="firstName" placeholder="First name" class="input w-full md:w-1/2" autocomplete="given-name" type="text" required autocapitalize="words" />
          <input v-model="lastName" placeholder="Last name" class="input w-full md:w-1/2" autocomplete="family-name" type="text" required autocapitalize="words" />
        </div>
        <div class="flex flex-col md:flex-row gap-4 mb-4">
          <input v-model="email" placeholder="Email" class="input w-full md:w-1/2" autocomplete="email" type="email" required autocorrect="off" />
          <input v-model="password" placeholder="Password" class="input w-full md:w-1/2" autocomplete="new-password" type="password" required minlength="8" autocorrect="off" />
        </div>
        <button class="button w-full mt-2" :disabled="isDisabled" @click="doSignup">Create account</button>
        <div class="text-nord11 text-center flex-wrap break-words mt-2">{{ message }}</div>
      </Card>

      <button class="button w-full mt-8 !text-sm" @click="() => $router.push('/signin')">Already have an account? Sign in</button>
    </div>
  </div>
</template>
