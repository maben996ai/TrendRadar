<template>
  <section class="panel">
    <p class="eyebrow">{{ t("contentAnalysis.eyebrow") }}</p>
    <h2>{{ t("contentAnalysis.title") }}</h2>
    <p class="muted">{{ t("contentAnalysis.description") }}</p>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from "../i18n";

const { t } = useI18n();
</script>
