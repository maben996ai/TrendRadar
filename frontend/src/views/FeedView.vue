<template>
  <section class="stack">
    <div class="hero">
      <div>
        <p class="eyebrow">{{ t("feed.eyebrow") }}</p>
        <h2>{{ t("feed.title") }}</h2>
      </div>
      <div class="feed-filters">
        <button
          class="filter-btn"
          :class="{ active: sortMode === 'time' }"
          @click="setSortMode('time')"
        >{{ t("feed.sortByTime") }}</button>
        <button
          class="filter-btn"
          :class="{ active: sortMode === 'author' }"
          @click="setSortMode('author')"
        >{{ t("feed.sortByAuthor") }}</button>
      </div>
    </div>

    <p v-if="feedStore.loading" class="muted feed-state">{{ t("feed.loading") }}</p>
    <p v-else-if="feedStore.error" class="error-msg feed-state">{{ t("feed.fetchError") }}</p>
    <p v-else-if="feedStore.videos.length === 0" class="muted feed-state">{{ t("feed.empty") }}</p>

    <template v-else>
      <!-- 按时间排序：分页平铺 -->
      <template v-if="sortMode === 'time'">
        <div class="video-grid-sm">
          <a
            v-for="video in pagedVideos"
            :key="video.id"
            :href="video.video_url"
            target="_blank"
            rel="noopener noreferrer"
            class="video-card-sm"
          >
            <div class="video-thumb-sm">
              <img v-if="video.thumbnail_url" :src="video.thumbnail_url" :alt="video.title" loading="lazy" />
              <div v-else class="video-thumb-placeholder" />
              <span class="platform-badge" :class="video.platform">{{ video.platform }}</span>
            </div>
            <div class="video-info-sm">
              <p class="video-title-sm">{{ video.title }}</p>
              <div class="video-meta-sm">
                <span class="muted">{{ video.creator_name }}</span>
                <span class="muted">{{ formatDate(video.published_at) }}</span>
              </div>
            </div>
          </a>
        </div>

        <div v-if="totalPages > 1" class="pagination">
          <button class="filter-btn" :disabled="page === 1" @click="page--">
            {{ t("feed.prevPage") }}
          </button>
          <span class="muted page-indicator">{{ page }} / {{ totalPages }}</span>
          <button class="filter-btn" :disabled="page === totalPages" @click="page++">
            {{ t("feed.nextPage") }}
          </button>
        </div>
      </template>

      <!-- 按作者分组：各组内时间倒排 -->
      <template v-else>
        <div v-for="group in authorGroups" :key="group.creatorName" class="author-group">
          <div class="author-group-header">
            <img v-if="group.avatarUrl" :src="group.avatarUrl" class="creator-avatar" :alt="group.creatorName" />
            <div v-else class="creator-avatar creator-avatar-placeholder" />
            <span class="author-group-name">{{ group.creatorName }}</span>
            <span class="platform-badge" :class="group.platform">{{ group.platform }}</span>
            <span class="muted author-group-count">{{ group.videos.length }} 个视频</span>
          </div>
          <div class="video-grid-sm">
            <a
              v-for="video in group.videos"
              :key="video.id"
              :href="video.video_url"
              target="_blank"
              rel="noopener noreferrer"
              class="video-card-sm"
            >
              <div class="video-thumb-sm">
                <img v-if="video.thumbnail_url" :src="video.thumbnail_url" :alt="video.title" loading="lazy" />
                <div v-else class="video-thumb-placeholder" />
              </div>
              <div class="video-info-sm">
                <p class="video-title-sm">{{ video.title }}</p>
                <span class="muted video-meta-sm">{{ formatDate(video.published_at) }}</span>
              </div>
            </a>
          </div>
        </div>
      </template>
    </template>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";

import { useI18n } from "../i18n";
import { useFeedStore } from "../stores/feed";
import type { Video } from "../types";

const { t } = useI18n();
const feedStore = useFeedStore();

const PAGE_SIZE = 20;
const sortMode = ref<"time" | "author">("time");
const page = ref(1);

const sortedByTime = computed(() =>
  [...feedStore.videos].sort(
    (a, b) => new Date(b.published_at).getTime() - new Date(a.published_at).getTime()
  )
);

const totalPages = computed(() => Math.max(1, Math.ceil(sortedByTime.value.length / PAGE_SIZE)));

const pagedVideos = computed(() => {
  const start = (page.value - 1) * PAGE_SIZE;
  return sortedByTime.value.slice(start, start + PAGE_SIZE);
});

interface AuthorGroup {
  creatorName: string;
  avatarUrl: string | null | undefined;
  platform: "bilibili" | "youtube";
  videos: Video[];
}

const authorGroups = computed((): AuthorGroup[] => {
  const map = new Map<string, AuthorGroup>();
  for (const video of feedStore.videos) {
    if (!map.has(video.creator_name)) {
      map.set(video.creator_name, {
        creatorName: video.creator_name,
        avatarUrl: video.creator_avatar_url,
        platform: video.platform,
        videos: [],
      });
    }
    map.get(video.creator_name)!.videos.push(video);
  }
  for (const group of map.values()) {
    group.videos.sort(
      (a, b) => new Date(b.published_at).getTime() - new Date(a.published_at).getTime()
    );
  }
  return [...map.values()].sort(
    (a, b) =>
      new Date(b.videos[0].published_at).getTime() -
      new Date(a.videos[0].published_at).getTime()
  );
});

function setSortMode(mode: "time" | "author") {
  sortMode.value = mode;
  page.value = 1;
}

watch(sortMode, () => { page.value = 1; });

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

onMounted(() => feedStore.fetchVideos());
</script>
