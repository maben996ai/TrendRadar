<template>
  <section class="panel">
    <p class="eyebrow">{{ t("creators.eyebrow") }}</p>
    <h2>{{ t("creators.title") }}</h2>
    <p class="muted">{{ t("creators.description") }}</p>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from "../i18n";

const { t } = useI18n();
</script>
