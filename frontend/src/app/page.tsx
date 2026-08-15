"use client";

import React, { useState, useEffect } from 'react';
import { getHealth } from '../api/health';
import { createProduct, getProduct } from '../api/product';
import { generateContent } from '../api/content';
import { submitFeedback } from '../api/feedback';
import { getRecent, getTrends } from '../api/recent';
import { Product, Generation, FeedbackResponse, RecentGenerationItem } from '../types';

export default function Dashboard() {
  // Debug State
  const [debugLog, setDebugLog] = useState<{ req: string, res: string, err: string }>({ req: '', res: '', err: '' });

  // API Status State
  const [health, setHealth] = useState<{ status: string; service: string } | null>(null);
  const [healthLoading, setHealthLoading] = useState(true);

  // Form State
  const [form, setForm] = useState({
    name: '',
    category: 'SaaS',
    description: '',
    features: '',
    problem_solved: '',
    target_audience: '',
    price: '',
    platform: 'Both',
    tone: 'Funny',
    requirements: ''
  });
  
  // App State
  const [productId, setProductId] = useState<number | null>(null);
  const [currentProduct, setCurrentProduct] = useState<Product | null>(null);
  const [generation, setGeneration] = useState<Generation | null>(null);
  const [generating, setGenerating] = useState(false);
  const [feedbackResponse, setFeedbackResponse] = useState<FeedbackResponse | null>(null);
  const [customFeedback, setCustomFeedback] = useState('');
  const [recent, setRecent] = useState<RecentGenerationItem[]>([]);
  const [trends, setTrends] = useState<any[]>([]);

  // Debug helper
  const logApi = (req: any, res: any = '', err: any = '') => {
    setDebugLog({
      req: typeof req === 'object' ? JSON.stringify(req, null, 2) : req,
      res: typeof res === 'object' ? JSON.stringify(res, null, 2) : res,
      err: typeof err === 'object' ? JSON.stringify(err, null, 2) : err,
    });
  };

  // Initial Load
  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      setHealthLoading(true);
      logApi('GET /api/health');
      const data = await getHealth();
      setHealth(data);
      logApi('GET /api/health', data);
    } catch (e: any) {
      setHealth(null);
      logApi('GET /api/health', '', e.message);
    } finally {
      setHealthLoading(false);
    }
  };

  const handleCreateProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        name: form.name,
        category: form.category,
        description: form.description,
        features: form.features.split('\n').filter(f => f.trim() !== ''),
        problem_solved: form.problem_solved,
        target_audience: form.target_audience,
        price: form.price,
        platform: form.platform,
        tone: form.tone,
        requirements: form.requirements
      };
      
      logApi('POST /api/product/create', payload);
      const res = await createProduct(payload);
      setProductId(res.id);
      logApi('POST /api/product/create payload', res);
      
      // Auto-fetch product
      fetchProduct(res.id);
    } catch (e: any) {
      logApi('POST /api/product/create', form, e.message);
      alert('Error creating product');
    }
  };

  const fetchProduct = async (id: number) => {
    try {
      logApi(`GET /api/product/${id}`);
      const prod = await getProduct(id);
      setCurrentProduct(prod);
      logApi(`GET /api/product/${id}`, prod);
    } catch (e: any) {
      logApi(`GET /api/product/${id}`, '', e.message);
    }
  };

  const handleGenerate = async () => {
    if (!productId) return;
    try {
      setGenerating(true);
      setGeneration(null);
      setFeedbackResponse(null);
      logApi('POST /api/content/generate', { product_id: productId });
      
      const res = await generateContent(productId);
      setGeneration(res);
      logApi('POST /api/content/generate', res);
      fetchRecent();
    } catch (e: any) {
      logApi('POST /api/content/generate', { product_id: productId }, e.message);
      alert('Error generating content:\n' + e.message);
    } finally {
      setGenerating(false);
    }
  };

  const handleFeedback = async (type: string, comment = '') => {
    if (!generation) return;
    try {
      const payload = {
        generation_id: generation.generation_id,
        feedback_type: type,
        comment
      };
      logApi('POST /api/feedback', payload);
      const res = await submitFeedback(payload);
      setFeedbackResponse(res);
      logApi('POST /api/feedback', res);
    } catch (e: any) {
      logApi('POST /api/feedback', { type }, e.message);
      alert('Error submitting feedback');
    }
  };

  const fetchRecent = async () => {
    try {
      logApi('GET /api/recent');
      const res = await getRecent();
      setRecent(res.items);
      logApi('GET /api/recent', res);
    } catch (e: any) {
      logApi('GET /api/recent', '', e.message);
    }
  };

  const fetchTrends = async () => {
    try {
      logApi('GET /api/trends');
      const res = await getTrends();
      setTrends(res);
      logApi('GET /api/trends', res);
    } catch (e: any) {
      logApi('GET /api/trends', '', e.message);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  return (
    <div className="min-h-screen p-8 bg-white text-black font-sans max-w-5xl mx-auto space-y-12">
      <h1 className="text-3xl font-bold border-b pb-4">TrendPilot AI Dashboard</h1>

      {/* BACKEND STATUS */}
      <section className="border p-4 rounded bg-gray-50">
        <h2 className="text-xl font-semibold mb-2">1. Backend Status</h2>
        <div className="flex items-center space-x-2">
          <span>Status:</span>
          {healthLoading ? (
            <span className="text-gray-500">Checking...</span>
          ) : health ? (
            <span className="text-green-600 font-bold">● Connected (OK)</span>
          ) : (
            <span className="text-red-600 font-bold">● Offline</span>
          )}
        </div>
        <p className="text-sm mt-1 text-gray-600">
          API URL: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
        </p>
      </section>

      {/* PRODUCT FORM */}
      <section className="border p-4 rounded bg-gray-50">
        <h2 className="text-xl font-semibold mb-4">2. Product Form</h2>
        <form onSubmit={handleCreateProduct} className="grid grid-cols-2 gap-4">
          <div className="space-y-1">
            <label className="block text-sm font-bold">Product Name *</label>
            <input required className="border p-2 w-full" value={form.name} onChange={e => setForm({...form, name: e.target.value})} />
          </div>
          
          <div className="space-y-1">
            <label className="block text-sm font-bold">Category *</label>
            <select className="border p-2 w-full" value={form.category} onChange={e => setForm({...form, category: e.target.value})}>
              <option>Fashion</option><option>SaaS</option><option>Education</option><option>Food</option>
              <option>Fitness</option><option>Beauty</option><option>Finance</option><option>Other</option>
            </select>
          </div>

          <div className="space-y-1 col-span-2">
            <label className="block text-sm font-bold">Description *</label>
            <textarea required className="border p-2 w-full h-20" value={form.description} onChange={e => setForm({...form, description: e.target.value})}></textarea>
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-bold">Features (one per line)</label>
            <textarea className="border p-2 w-full h-24" placeholder="ATS optimization&#10;AI suggestions" value={form.features} onChange={e => setForm({...form, features: e.target.value})}></textarea>
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-bold">Problem Solved</label>
            <textarea className="border p-2 w-full h-24" value={form.problem_solved} onChange={e => setForm({...form, problem_solved: e.target.value})}></textarea>
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-bold">Target Audience *</label>
            <input required className="border p-2 w-full" value={form.target_audience} onChange={e => setForm({...form, target_audience: e.target.value})} />
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-bold">Price</label>
            <input className="border p-2 w-full" value={form.price} onChange={e => setForm({...form, price: e.target.value})} />
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-bold">Platform *</label>
            <select className="border p-2 w-full" value={form.platform} onChange={e => setForm({...form, platform: e.target.value})}>
              <option>Instagram</option><option>YouTube Shorts</option><option>Both</option>
            </select>
          </div>

          <div className="space-y-1">
            <label className="block text-sm font-bold">Tone *</label>
            <select className="border p-2 w-full" value={form.tone} onChange={e => setForm({...form, tone: e.target.value})}>
              <option>Funny</option><option>Sarcastic</option><option>Gen-Z</option><option>Professional</option>
              <option>Emotional</option><option>Educational</option><option>Luxury</option><option>Meme-heavy</option>
            </select>
          </div>

          <div className="space-y-1 col-span-2">
            <label className="block text-sm font-bold">Custom Requirements</label>
            <textarea className="border p-2 w-full h-24" placeholder="Make it Hinglish, funny, relatable to Indian college students and slightly savage." value={form.requirements} onChange={e => setForm({...form, requirements: e.target.value})}></textarea>
          </div>

          <div className="col-span-2 mt-4">
            <button type="submit" className="bg-blue-600 text-white px-4 py-2 font-bold rounded">Create Product</button>
            {productId && <span className="ml-4 text-green-700 font-bold">Product created successfully. Product ID: {productId}</span>}
          </div>
        </form>
      </section>

      {/* GET PRODUCT */}
      {currentProduct && (
        <section className="border p-4 rounded bg-gray-50">
          <h2 className="text-xl font-semibold mb-2">3. Current Product</h2>
          <pre className="bg-gray-200 p-2 text-xs overflow-x-auto">
            {JSON.stringify(currentProduct, null, 2)}
          </pre>
        </section>
      )}

      {/* GENERATE CONTENT */}
      <section className="border p-4 rounded bg-gray-50">
        <h2 className="text-xl font-semibold mb-4">4. Generate Content</h2>
        <button 
          onClick={handleGenerate} 
          disabled={!productId || generating}
          className="bg-purple-600 text-white px-4 py-2 font-bold rounded disabled:opacity-50"
        >
          {generating ? 'Generating...' : 'Generate Content'}
        </button>
      </section>

      {/* GENERATED CONTENT */}
      {generation && (
        <section className="border p-4 rounded bg-gray-50 space-y-6">
          <h2 className="text-xl font-semibold">5. Generated Result</h2>
          
          <div className="bg-white p-4 border rounded shadow-sm">
            <div className="font-bold text-lg mb-4 text-purple-700">Viral Score: {generation.viral_score}</div>
            
            <div className="mb-4">
              <h3 className="font-bold text-gray-700">Trend</h3>
              <p>Format: {generation.trend.format}</p>
              <p>Reason: {generation.trend.reason}</p>
            </div>

            <div className="mb-4 p-3 bg-blue-50 border border-blue-100 flex justify-between items-start">
              <div>
                <h3 className="font-bold text-gray-700">Hook</h3>
                <p className="text-xl">{generation.hook}</p>
              </div>
              <button onClick={() => copyToClipboard(generation.hook)} className="bg-gray-200 text-xs px-2 py-1 rounded">Copy</button>
            </div>

            <div className="mb-4">
              <h3 className="font-bold text-gray-700">Meme</h3>
              <p>Format: {generation.meme.format}</p>
              <p>Search Query: {generation.meme.search_query}</p>
              <div className="mt-2">
                {generation.meme.gif ? (
                  <img src={generation.meme.gif.preview_url} alt="Meme GIF" className="max-w-xs border rounded" />
                ) : (
                  <span className="text-gray-500 italic">No Tenor result available.</span>
                )}
              </div>
            </div>

            <div className="mb-4">
              <h3 className="font-bold text-gray-700 mb-2">Dialogue</h3>
              <div className="space-y-2 bg-gray-50 p-4 border rounded">
                {generation.dialogue.map((d, i) => (
                  <div key={i}>
                    <span className="font-bold">{d.speaker}:</span> {d.line}
                  </div>
                ))}
              </div>
            </div>

            <div className="mb-4 flex justify-between items-start">
              <div className="w-full mr-4">
                <h3 className="font-bold text-gray-700 mb-2">Script</h3>
                <div className="space-y-4">
                  {generation.script.map((s, i) => (
                    <div key={i} className="bg-yellow-50 p-3 border border-yellow-100 rounded text-sm">
                      <div className="font-bold mb-1">{s.time}</div>
                      <div><strong>Visual:</strong> {s.visual}</div>
                      <div><strong>Voice:</strong> {s.voice}</div>
                      {s.text_overlay && <div><strong>Text:</strong> {s.text_overlay}</div>}
                    </div>
                  ))}
                </div>
              </div>
              <button onClick={() => copyToClipboard(JSON.stringify(generation.script, null, 2))} className="bg-gray-200 text-xs px-2 py-1 rounded">Copy</button>
            </div>

            <div className="mb-4 flex justify-between items-start">
              <div>
                <h3 className="font-bold text-gray-700">Caption</h3>
                <p className="whitespace-pre-wrap">{generation.caption}</p>
                <p className="text-blue-600 mt-2">{generation.hashtags.join(' ')}</p>
              </div>
              <button onClick={() => copyToClipboard(`${generation.caption}\n\n${generation.hashtags.join(' ')}`)} className="bg-gray-200 text-xs px-2 py-1 rounded">Copy</button>
            </div>
          </div>

          {/* FEEDBACK & PERSONALIZATION */}
          <div className="border p-4 bg-white rounded space-y-6">
            <div>
              <h3 className="font-bold text-lg mb-2">6. Improve this content</h3>
              <div className="flex flex-wrap gap-2">
                <button onClick={() => handleFeedback('funnier')} className="bg-gray-200 px-3 py-1 rounded hover:bg-gray-300">Make it funnier</button>
                <button onClick={() => handleFeedback('more_trendy')} className="bg-gray-200 px-3 py-1 rounded hover:bg-gray-300">Make it more trendy</button>
                <button onClick={() => handleFeedback('more_relatable')} className="bg-gray-200 px-3 py-1 rounded hover:bg-gray-300">Make it more relatable</button>
                <button onClick={() => handleFeedback('more_professional')} className="bg-gray-200 px-3 py-1 rounded hover:bg-gray-300">Make it professional</button>
                <button onClick={() => handleFeedback('better_hook')} className="bg-gray-200 px-3 py-1 rounded hover:bg-gray-300">Improve the hook</button>
                <button onClick={() => handleFeedback('shorter')} className="bg-gray-200 px-3 py-1 rounded hover:bg-gray-300">Make it shorter</button>
                <button onClick={() => handleFeedback('like')} className="bg-green-100 text-green-800 px-3 py-1 rounded hover:bg-green-200">Like</button>
                <button onClick={() => handleFeedback('dislike')} className="bg-red-100 text-red-800 px-3 py-1 rounded hover:bg-red-200">Dislike</button>
              </div>
            </div>

            <div>
              <h4 className="font-bold mb-1">Other feedback</h4>
              <textarea 
                className="border p-2 w-full h-16" 
                value={customFeedback} 
                onChange={e => setCustomFeedback(e.target.value)} 
                placeholder="Make the dialogue more savage and shorter."
              ></textarea>
              <button onClick={() => handleFeedback('custom', customFeedback)} className="mt-2 bg-blue-600 text-white px-3 py-1 rounded text-sm">Submit Feedback</button>
            </div>

            {feedbackResponse && (
              <div className="bg-green-50 text-green-800 p-3 rounded text-sm">
                <div>✓ Feedback saved</div>
                <div>{feedbackResponse.preference_saved ? '✓ Preference updated' : 'Preference unchanged'}</div>
              </div>
            )}

            <div className="bg-purple-50 p-4 border border-purple-100 rounded text-sm">
              <h4 className="font-bold text-purple-800">Personalization Test</h4>
              <p className="mb-2">1. Generate content.<br/>2. Click "Make it funnier".<br/>3. Generate again.<br/>4. Compare whether the second generation reflects the preference.</p>
              <div className="font-mono mt-2">
                Last feedback: {feedbackResponse?.feedback_type || 'None'}
              </div>
              <div className="font-mono">
                Preference: Stored by backend
              </div>
            </div>
          </div>
        </section>
      )}

      {/* RECENT GENERATIONS */}
      <section className="border p-4 rounded bg-gray-50">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">7. Recent Generations</h2>
          <button onClick={fetchRecent} className="bg-blue-100 text-blue-800 px-3 py-1 rounded text-sm font-bold">Refresh</button>
        </div>
        
        {recent.length === 0 ? (
          <p className="text-gray-500 text-sm">No recent generations.</p>
        ) : (
          <div className="space-y-4">
            {recent.map((r, i) => (
              <div key={r.id} className="border p-3 bg-white rounded flex flex-col space-y-1">
                <span className="font-bold">{i + 1}. Product {r.product_id}</span>
                <span className="text-gray-700 italic">"{r.hook}"</span>
                <span className="text-sm text-gray-500">{r.tone} • {r.platform}</span>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* TRENDS */}
      <section className="border p-4 rounded bg-gray-50">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">8. Trends</h2>
          <button onClick={fetchTrends} className="bg-blue-100 text-blue-800 px-3 py-1 rounded text-sm font-bold">Load Trends</button>
        </div>
        
        {trends.length === 0 ? (
          <p className="text-gray-500 text-sm">Click "Load Trends" to fetch.</p>
        ) : (
          <div className="space-y-4">
            {trends.map((t, i) => (
              <div key={i} className="border p-3 bg-white rounded">
                <div className="font-bold text-lg">{t.name}</div>
                <div className="text-gray-700">{t.description}</div>
                {t.best_for && <div className="text-sm mt-1 text-gray-500">Best for: {t.best_for}</div>}
              </div>
            ))}
          </div>
        )}
      </section>

      {/* API DEBUG */}
      <section className="border-t-4 border-black pt-4 pb-12 mt-12">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold bg-black text-white px-2 py-1 inline-block">API Debug</h2>
          <button onClick={() => setDebugLog({ req: '', res: '', err: '' })} className="bg-red-100 text-red-800 px-3 py-1 text-sm font-bold rounded">Clear Debug</button>
        </div>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <h3 className="font-bold text-sm mb-1 text-blue-800">Last Request</h3>
            <pre className="bg-blue-50 p-2 text-xs h-64 overflow-auto border">{debugLog.req}</pre>
          </div>
          <div>
            <h3 className="font-bold text-sm mb-1 text-green-800">Last Response</h3>
            <pre className="bg-green-50 p-2 text-xs h-64 overflow-auto border">{debugLog.res}</pre>
          </div>
          <div>
            <h3 className="font-bold text-sm mb-1 text-red-800">Last Error</h3>
            <pre className="bg-red-50 p-2 text-xs h-64 overflow-auto border">{debugLog.err}</pre>
          </div>
        </div>
      </section>

    </div>
  );
}
