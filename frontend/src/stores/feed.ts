import { defineStore } from "pinia";
import { ref } from "vue";

import { videosApi } from "../api/videos";
import type { Video } from "../types";

export const useFeedStore = defineStore("feed", () => {
  const videos = ref<Video[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchVideos() {
    loading.value = true;
    error.value = null;
    try {
      const resp = await videosApi.list();
      videos.value = resp.data;
    } catch {
      error.value = "fetch_failed";
    } finally {
      loading.value = false;
    }
  }

  return { videos, loading, error, fetchVideos };
});
