import { api } from "./api";

import type { UpdateProgression } from "@/schemas/progress";

export async function getProgress(challengeId: number) {
  const response = await api.get(`/challenge/progress/get/${challengeId}`);
  return response.data;
}

export async function updateProgress(data: UpdateProgression) {
  const response = await api.patch("/challenge/progress/update",data);
  return response.data;
}