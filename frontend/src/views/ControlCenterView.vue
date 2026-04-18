<template>
  <section class="stack">
    <div class="panel">
      <p class="eyebrow">{{ t("settings.eyebrow") }}</p>
      <h2>{{ t("settings.title") }}</h2>
      <p class="muted">{{ t("settings.description") }}</p>
    </div>
    <div class="panel">
      <p class="eyebrow">{{ t("crawlLogs.eyebrow") }}</p>
      <h2>{{ t("crawlLogs.title") }}</h2>
      <p class="muted">{{ t("crawlLogs.description") }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from "../i18n";

const { t } = useI18n();
</script>
