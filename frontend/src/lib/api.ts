export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8020'

export type ProductPayload = {
  name: string
  category: string
  description: string
  features?: string
  problem?: string
  audience: string
  price_range?: string
  competitors?: string
  platform: 'Instagram' | 'YouTube Shorts' | 'Both'
  tone: 'Funny' | 'Sarcastic' | 'Professional' | 'Emotional' | 'Luxury' | 'Gen-Z' | 'Educational' | 'Meme Style'
  requirements?: string
}

export type GeneratedContent = {
  generation_id: number
  product_id: number
  hook: string
  meme_format: string
  dialogue: string[]
  script: { scene: string; time: string }[]
  caption: string
  klipy_query: string
  selected_media_type?: string | null
  media_feeling?: string | null
  media_reason?: string | null
  hashtags: string[]
  viral_score: number
  meme?: {
    title?: string | null
    url?: string | null
    preview?: string | null
    source?: string
    mediaType?: string | null
    providerStatus?: string | null
  } | null
}

async function requestJson<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers || {}),
    },
  })
  const payload = await response.json().catch(() => null)
  if (!response.ok) {
    throw new Error(payload?.detail || `API request failed: ${response.status}`)
  }
  return payload as T
}

export async function healthCheck() {
  return requestJson<{ ok: boolean; service: string }>('/api/health')
}

export async function createProduct(payload: ProductPayload) {
  return requestJson<{ product_id: number; message: string }>('/api/product/create', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function generateContent(productId: number, tone?: string, requirements?: string) {
  return requestJson<GeneratedContent>('/api/content/generate', {
    method: 'POST',
    body: JSON.stringify({ product_id: productId, tone, requirements }),
  })
}

export async function createFeedback(generationId: number, feedback: string, sentiment = 'Positive') {
  return requestJson<{ feedback_id: number; preference: string; message: string }>('/api/feedback/create', {
    method: 'POST',
    body: JSON.stringify({ generation_id: generationId, feedback, sentiment }),
  })
}
