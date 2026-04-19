import { apiClient } from "./client";
import type { Video, VideoListResponse } from "../types";

export const videosApi = {
  list(platform?: "bilibili" | "youtube", cursor?: string | null, limit?: number) {
    const params = {
      ...(platform ? { platform } : {}),
      ...(cursor ? { cursor } : {}),
      ...(limit ? { limit } : {}),
    };
    return apiClient.get<Video[] | VideoListResponse>("/videos", { params });
  },
};
