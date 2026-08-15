'use client';

import { useMemo, useState } from 'react';

type ApiResult = {
  status: 'idle' | 'loading' | 'success' | 'error';
  request?: unknown;
  response?: unknown;
};

type EndpointConfig = {
  id: string;
  title: string;
  method: 'GET' | 'POST';
  path: string;
  description: string;
  body?: string;
};

type MediaPreview = {
  title: string;
  type: string;
  url: string;
  preview?: string;
  source?: string;
};

const pretty = (value: unknown) => JSON.stringify(value, null, 2);

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function mediaUrl(value: unknown): string | undefined {
  return typeof value === 'string' && value.startsWith('http') ? value : undefined;
}

function collectMedia(payload: unknown): MediaPreview[] {
  if (!isRecord(payload)) return [];
  const data = isRecord(payload.data) ? payload.data : payload;
  const items: MediaPreview[] = [];

  function pushItem(item: unknown, fallbackType = 'media') {
    if (!isRecord(item)) return;
    const url = mediaUrl(item.url) || mediaUrl(item.preview);
    if (!url) return;
    items.push({
      title: String(item.title || item.id || fallbackType),
      type: String(item.mediaType || fallbackType),
      url,
      preview: mediaUrl(item.preview),
      source: typeof item.source === 'string' ? item.source : undefined,
    });
  }

  pushItem(data.meme, 'meme');

  if (Array.isArray(data.topTrends)) {
    data.topTrends.slice(0, 8).forEach((item) => pushItem(item, 'trend'));
  }

  if (isRecord(data.mediaSuggestions)) {
    Object.values(data.mediaSuggestions).forEach((group) => {
      if (Array.isArray(group)) group.slice(0, 6).forEach((item) => pushItem(item));
    });
  }

  return items;
}

function isVideoMedia(item: MediaPreview) {
  const url = item.url.toLowerCase();
  return item.type === 'clip' || url.includes('.mp4') || url.includes('tinymp4') || url.includes('video');
}

function MediaGallery({ result }: { result: ApiResult }) {
  const media = collectMedia(result.response);
  if (!media.length) {
    if (result.status !== 'success') return null;
    return (
      <section className="media-gallery">
        <strong>Playable Media</strong>
        <div className="media-empty">No playable media URL was returned in this response.</div>
      </section>
    );
  }

  return (
    <section className="media-gallery">
      <strong>Playable Media</strong>
      <div className="media-grid">
        {media.map((item, index) => (
          <figure className="media-tile" key={`${item.url}-${index}`}>
            <div className="media-frame">
              {isVideoMedia(item) ? (
                <video src={item.url} controls muted loop playsInline preload="metadata" poster={item.preview} />
              ) : (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={item.preview || item.url} alt={item.title} loading="lazy" />
              )}
            </div>
            <figcaption>
              <span>{item.title}</span>
              <small>
                {item.type}
                {item.source ? ` · ${item.source}` : ''}
              </small>
              <a href={item.url} target="_blank" rel="noreferrer">
                Open media
              </a>
            </figcaption>
          </figure>
        ))}
      </div>
    </section>
  );
}

const defaultProduct = {
  name: 'AI Resume Builder',
  category: 'Education',
  description: 'AI platform for resume creation',
  features: 'ATS optimization, templates',
  problem: 'Students struggle to make ATS-friendly resumes',
  audience: 'College students',
  price_range: 'Free trial',
  competitors: 'Canva, Novoresume',
  platform: 'Instagram',
  tone: 'Funny',
  requirements: 'Make it relatable and meme style',
};

const defaultTrend = {
  brand: 'Frooti',
  industry: 'Food & Beverage',
  audience: 'Gen Z',
  limit: 10,
};

const defaultApiBase =
  process.env.NEXT_PUBLIC_API_BASE_URL || process.env.VITE_API_BASE_URL || 'http://127.0.0.1:8020';

export default function HomePage() {
  const [apiBase, setApiBase] = useState(defaultApiBase);
  const [productId, setProductId] = useState('');
  const [generationId, setGenerationId] = useState('');
  const [results, setResults] = useState<Record<string, ApiResult>>({});
  const [bodies, setBodies] = useState<Record<string, string>>({
    createProduct: pretty(defaultProduct),
    generateContent: pretty({ product_id: 1, tone: 'Sarcastic', requirements: 'Use Hinglish and short punchlines' }),
    createFeedback: pretty({ generation_id: 1, feedback: 'Make it funnier and less formal', sentiment: 'Positive' }),
    analyzeTrends: pretty(defaultTrend),
  });

  const endpoints = useMemo<EndpointConfig[]>(
    () => [
      {
        id: 'root',
        title: 'Root',
        method: 'GET',
        path: '/',
        description: 'Checks the backend landing response.',
      },
      {
        id: 'health',
        title: 'Health',
        method: 'GET',
        path: '/api/health',
        description: 'Confirms the API process is alive.',
      },
      {
        id: 'createProduct',
        title: 'Create Product',
        method: 'POST',
        path: '/api/product/create',
        description: 'Sends product context into the backend and returns a product id.',
        body: bodies.createProduct,
      },
      {
        id: 'getProduct',
        title: 'Get Product',
        method: 'GET',
        path: `/api/product/${productId || '1'}`,
        description: 'Reads the saved product back by id.',
      },
      {
        id: 'generateContent',
        title: 'Generate Content',
        method: 'POST',
        path: '/api/content/generate',
        description: 'Generates hook, script, caption, KLIPY query, and media suggestion.',
        body: bodies.generateContent,
      },
      {
        id: 'createFeedback',
        title: 'Create Feedback',
        method: 'POST',
        path: '/api/feedback/create',
        description: 'Saves feedback and updates personalization memory.',
        body: bodies.createFeedback,
      },
      {
        id: 'brand',
        title: 'Brand Context',
        method: 'GET',
        path: `/api/brand/${productId || '1'}`,
        description: 'Shows product context, memory, and recent generations.',
      },
      {
        id: 'recent',
        title: 'Recent Generations',
        method: 'GET',
        path: '/api/recent?limit=5',
        description: 'Lists recent generated content.',
      },
      {
        id: 'analyzeTrends',
        title: 'Trend Intelligence',
        method: 'POST',
        path: '/api/trends/analyze',
        description: 'Runs KLIPY trend discovery, ranking, prediction, and recommendations.',
        body: bodies.analyzeTrends,
      },
      {
        id: 'openapi',
        title: 'OpenAPI',
        method: 'GET',
        path: '/openapi.json',
        description: 'Loads the generated API schema.',
      },
    ],
    [bodies, productId],
  );

  function syncFlowIds(payload: unknown) {
    if (!payload || typeof payload !== 'object') return;
    const data = payload as Record<string, unknown>;
    if (typeof data.product_id === 'number') {
      const nextProductId = String(data.product_id);
      setProductId(nextProductId);
      setBodies((current) => ({
        ...current,
        generateContent: pretty({ ...JSON.parse(current.generateContent), product_id: data.product_id }),
      }));
    }
    if (typeof data.generation_id === 'number') {
      const nextGenerationId = String(data.generation_id);
      setGenerationId(nextGenerationId);
      setBodies((current) => ({
        ...current,
        createFeedback: pretty({ ...JSON.parse(current.createFeedback), generation_id: data.generation_id }),
      }));
    }
  }

  async function runEndpoint(endpoint: EndpointConfig) {
    const url = `${apiBase.replace(/\/$/, '')}${endpoint.path}`;
    let requestBody: unknown = undefined;

    try {
      if (endpoint.method === 'POST') {
        requestBody = JSON.parse(endpoint.body || '{}');
      }
    } catch (error) {
      setResults((current) => ({
        ...current,
        [endpoint.id]: {
          status: 'error',
          request: endpoint.body,
          response: { message: 'Invalid JSON body', detail: String(error) },
        },
      }));
      return;
    }

    setResults((current) => ({
      ...current,
      [endpoint.id]: { status: 'loading', request: requestBody || endpoint.path },
    }));

    try {
      const response = await fetch(url, {
        method: endpoint.method,
        headers: endpoint.method === 'POST' ? { 'Content-Type': 'application/json' } : undefined,
        body: endpoint.method === 'POST' ? JSON.stringify(requestBody) : undefined,
      });
      const contentType = response.headers.get('content-type') || '';
      const payload = contentType.includes('application/json') ? await response.json() : await response.text();
      const hint =
        response.status === 404 && endpoint.id === 'analyzeTrends'
          ? 'Trend endpoint was not found. Check that API base URL points to the latest backend, usually http://127.0.0.1:8020.'
          : undefined;
      const result = { ok: response.ok, status: response.status, data: payload, hint };
      if (response.ok) syncFlowIds(payload);
      setResults((current) => ({
        ...current,
        [endpoint.id]: {
          status: response.ok ? 'success' : 'error',
          request: requestBody || endpoint.path,
          response: result,
        },
      }));
    } catch (error) {
      setResults((current) => ({
        ...current,
        [endpoint.id]: {
          status: 'error',
          request: requestBody || endpoint.path,
          response: { message: 'Request failed', detail: String(error) },
        },
      }));
    }
  }

  async function runHappyPath() {
    const order = ['health', 'createProduct', 'getProduct', 'generateContent', 'createFeedback', 'brand', 'recent', 'analyzeTrends'];
    for (const id of order) {
      const endpoint = endpoints.find((item) => item.id === id);
      if (endpoint) await runEndpoint(endpoint);
    }
  }

  return (
    <main className="api-tester">
      <section className="tester-header">
        <div>
          <p className="eyebrow">TrendPilot AI</p>
          <h1>Backend API Test Console</h1>
        </div>
        <button className="primary-action" type="button" onClick={runHappyPath}>
          Run Happy Path
        </button>
      </section>

      <section className="control-strip">
        <label>
          API base URL
          <input value={apiBase} onChange={(event) => setApiBase(event.target.value)} />
        </label>
        <label>
          Product ID
          <input value={productId} onChange={(event) => setProductId(event.target.value)} placeholder="auto" />
        </label>
        <label>
          Generation ID
          <input value={generationId} onChange={(event) => setGenerationId(event.target.value)} placeholder="auto" />
        </label>
      </section>

      <section className="endpoint-grid">
        {endpoints.map((endpoint) => {
          const result = results[endpoint.id] || { status: 'idle' };
          return (
            <article className="endpoint-card" key={endpoint.id}>
              <header>
                <div>
                  <span className={`method ${endpoint.method.toLowerCase()}`}>{endpoint.method}</span>
                  <h2>{endpoint.title}</h2>
                </div>
                <button type="button" onClick={() => runEndpoint(endpoint)} disabled={result.status === 'loading'}>
                  {result.status === 'loading' ? 'Running...' : 'Run'}
                </button>
              </header>
              <p>{endpoint.description}</p>
              <code className="path">{endpoint.path}</code>

              {endpoint.body !== undefined ? (
                <label className="json-editor">
                  Request JSON
                  <textarea
                    value={endpoint.body}
                    onChange={(event) =>
                      setBodies((current) => ({
                        ...current,
                        [endpoint.id]: event.target.value,
                      }))
                    }
                  />
                </label>
              ) : null}

              <div className={`status ${result.status}`}>{result.status}</div>
              <MediaGallery result={result} />
              <div className="response-columns">
                <div>
                  <strong>Request</strong>
                  <pre>{pretty(result.request ?? null)}</pre>
                </div>
                <div>
                  <strong>Response</strong>
                  <pre>{pretty(result.response ?? null)}</pre>
                </div>
              </div>
            </article>
          );
        })}
      </section>
    </main>
  );
}
