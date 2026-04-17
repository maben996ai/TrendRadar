<template>
  <div class="app-frame">
    <div class="locale-switcher" :aria-label="t('app.localeLabel')">
      <button
        class="locale-option"
        :class="{ active: locale === 'zh-CN' }"
        :aria-pressed="locale === 'zh-CN'"
        @click="setLocale('zh-CN')"
      >
        中文
      </button>
      <button
        class="locale-option"
        :class="{ active: locale === 'en' }"
        :aria-pressed="locale === 'en'"
        @click="setLocale('en')"
      >
        EN
      </button>
    </div>
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { useI18n } from "./i18n";

const { locale, setLocale, t } = useI18n();
</script>
