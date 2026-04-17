<template>
  <section class="panel">
    <p class="eyebrow">{{ t("crawlLogs.eyebrow") }}</p>
    <h2>{{ t("crawlLogs.title") }}</h2>
    <p class="muted">{{ t("crawlLogs.description") }}</p>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from "../i18n";

const { t } = useI18n();
</script>
