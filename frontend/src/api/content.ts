import { apiClient } from './client';
import { Generation } from '../types';

type BackendScene = {
  scene: string;
  time: string;
};

type BackendGeneration = {
  generation_id: number;
  product_id: number;
  viral_score: number;
  trend?: Record<string, unknown> | null;
  hook: string;
  meme_format: string;
  dialogue: string[];
  script: BackendScene[];
  caption: string;
  hashtags: string[];
  klipy_query: string;
  meme?: {
    title?: string | null;
    url?: string | null;
    preview?: string | null;
    source?: string | null;
    mediaType?: string | null;
    providerStatus?: string | null;
  } | null;
};

export const normalizeGeneration = (data: BackendGeneration): Generation => {
  const trendName = String(data.trend?.name || data.trend?.title || data.klipy_query || 'Generated trend');
  const trendReason = String(data.trend?.reason || data.trend?.analysis || 'Selected from the generated brief and current content signals.');
  const mediaUrl = data.meme?.url || data.meme?.preview || '';

  return {
    generation_id: data.generation_id,
    viral_score: data.viral_score,
    trend: {
      format: trendName,
      reason: trendReason,
    },
    hook: data.hook,
    meme: {
      format: data.meme_format,
      search_query: data.klipy_query,
      gif: mediaUrl
        ? {
            id: data.meme?.title || data.klipy_query,
            title: data.meme?.title || data.meme_format,
            preview_url: data.meme?.preview || mediaUrl,
            gif_url: mediaUrl,
          }
        : null,
    },
    dialogue: (data.dialogue || []).map((line, index) => ({
      speaker: index % 2 === 0 ? 'Person A' : 'Person B',
      line,
    })),
    script: (data.script || []).map((scene) => ({
      time: scene.time,
      visual: scene.scene,
      voice: scene.scene,
      text_overlay: data.hook,
    })),
    caption: data.caption,
    hashtags: data.hashtags || [],
  };
};

export const generateContent = async (productId: number, tone?: string, requirements?: string): Promise<Generation> => {
  const response = await apiClient.post('/api/content/generate', {
    product_id: productId,
    tone,
    requirements,
  });
  return normalizeGeneration(response.data);
};
