<template>
  <section class="panel auth-panel">
    <p class="eyebrow">{{ t("auth.loginEyebrow") }}</p>
    <h2>{{ t("auth.loginTitle") }}</h2>

    <form class="form" @submit.prevent="handleLogin">
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
          :placeholder="t('auth.passwordPlaceholder')"
          autocomplete="current-password"
          required
        />
      </div>

      <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

      <button class="btn" type="submit" :disabled="loading">
        {{ loading ? t("auth.signingIn") : t("auth.signIn") }}
      </button>
    </form>

    <p class="auth-footer">
      {{ t("auth.noAccount") }}
      <RouterLink to="/register">{{ t("auth.createOne") }}</RouterLink>
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

const email = ref("");
const password = ref("");
const loading = ref(false);
const errorMsg = ref("");

async function handleLogin() {
  errorMsg.value = "";
  loading.value = true;
  try {
    const resp = await authApi.login({ email: email.value, password: password.value });
    authStore.setToken(resp.data.access_token);
    await authStore.fetchUser();
    router.push("/");
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail ?? t("auth.loginFailed");
  } finally {
    loading.value = false;
  }
}
</script>
