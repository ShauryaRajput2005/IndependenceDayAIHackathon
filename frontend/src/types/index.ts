export interface Product {
  id?: number;
  name: string;
  category: string;
  description: string;
  features: string[];
  problem_solved?: string;
  target_audience: string;
  price?: string;
  platform: string;
  tone: string;
  requirements?: string;
  created_at?: string;
}

export interface GifResult {
  id: string;
  title: string;
  preview_url: string;
  gif_url: string;
  width?: number;
  height?: number;
}

export interface Meme {
  format: string;
  search_query: string;
  gif?: GifResult | null;
}

export interface Dialogue {
  speaker: string;
  line: string;
}

export interface ScriptScene {
  time: string;
  visual: string;
  voice: string;
  text_overlay?: string;
}

export interface Generation {
  generation_id: number;
  viral_score: number;
  trend: {
    format: string;
    reason: string;
  };
  hook: string;
  meme: Meme;
  dialogue: Dialogue[];
  script: ScriptScene[];
  caption: string;
  hashtags: string[];
}

export interface Feedback {
  generation_id: number;
  feedback_type: string;
  comment?: string;
}

export interface FeedbackResponse {
  id: number;
  generation_id: number;
  feedback_type: string;
  comment?: string;
  created_at: string;
  preference_saved: boolean;
}

export interface RecentGenerationItem {
  id: number;
  product_id: number;
  hook: string;
  tone: string;
  platform: string;
  created_at: string;
}

export interface RecentGenerationsResponse {
  items: RecentGenerationItem[];
  total: number;
}

export interface Trend {
  name: string;
  description: string;
  platforms: string[];
  tones: string[];
  audience: string[];
  best_for: string;
  example: string;
}
