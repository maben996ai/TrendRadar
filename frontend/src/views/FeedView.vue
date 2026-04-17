<template>
  <section class="stack">
    <div class="hero">
      <div>
        <p class="eyebrow">{{ t("feed.eyebrow") }}</p>
        <h2>{{ t("feed.title") }}</h2>
      </div>
      <span class="status-pill">{{ t("feed.status") }}</span>
    </div>

    <div class="grid">
      <article class="panel card" v-for="item in cards" :key="item.title">
        <p class="card-platform">{{ item.platform }}</p>
        <h3>{{ item.title }}</h3>
        <p class="muted">{{ item.description }}</p>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from "vue";

import { useI18n } from "../i18n";

const { t } = useI18n();

const cards = computed(() => [
  {
    platform: t("feed.cards.bilibiliPlatform"),
    title: t("feed.cards.bilibiliTitle"),
    description: t("feed.cards.bilibiliDescription"),
  },
  {
    platform: t("feed.cards.youtubePlatform"),
    title: t("feed.cards.youtubeTitle"),
    description: t("feed.cards.youtubeDescription"),
  },
  {
    platform: t("feed.cards.systemPlatform"),
    title: t("feed.cards.systemTitle"),
    description: t("feed.cards.systemDescription"),
  },
]);
</script>
