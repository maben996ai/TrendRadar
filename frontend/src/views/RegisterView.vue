<template>
  <section class="panel auth-panel">
    <p class="eyebrow">{{ t("auth.registerEyebrow") }}</p>
    <h2>{{ t("auth.registerTitle") }}</h2>

    <form class="form" @submit.prevent="handleRegister">
      <div class="field">
        <label for="display_name">{{ t("auth.displayName") }}</label>
        <input
          id="display_name"
          v-model="displayName"
          type="text"
          :placeholder="t('auth.displayNamePlaceholder')"
          autocomplete="name"
        />
      </div>

      <div class="field">
        <label for="email">{{ t("auth.email") }}</label>
        <input
          id="email"
          v-model="email"
          type="email"
          :placeholder="t('auth.emailPlaceholder')"
          autocomplete="email"
          required
        />
      </div>

      <div class="field">
        <label for="password">{{ t("auth.password") }}</label>
        <input
          id="password"
          v-model="password"
          type="password"
          :placeholder="t('auth.registerPasswordPlaceholder')"
          autocomplete="new-password"
          minlength="8"
          required
        />
      </div>

      <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

      <button class="btn" type="submit" :disabled="loading">
        {{ loading ? t("auth.creatingAccount") : t("auth.createAccount") }}
      </button>
    </form>

    <p class="auth-footer">
      {{ t("auth.haveAccount") }}
      <RouterLink to="/login">{{ t("auth.signInLink") }}</RouterLink>
    </p>
  </section>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

import { authApi } from "../api/auth";
import { useI18n } from "../i18n";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const authStore = useAuthStore();
const { t } = useI18n();

const displayName = ref("");
const email = ref("");
const password = ref("");
const loading = ref(false);
const errorMsg = ref("");

async function handleRegister() {
  errorMsg.value = "";
  loading.value = true;
  try {
    await authApi.register({
      email: email.value,
      password: password.value,
      display_name: displayName.value || undefined,
    });
    const loginResp = await authApi.login({ email: email.value, password: password.value });
    authStore.setToken(loginResp.data.access_token);
    await authStore.fetchUser();
    router.push("/");
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail ?? t("auth.registerFailed");
  } finally {
    loading.value = false;
  }
}
</script>
