"use client";

import React, { useState } from 'react';
import { createProduct } from '@/api/product';
import { generateContent } from '@/api/content';
import { submitFeedback } from '@/api/feedback';
import type { Generation } from '@/types';

interface ProductBrief {
  name: string;
  category: string;
  description: string;
  features: string[];
  problem_solved: string;
  target_audience: string;
  platform: string;
  tone: string;
  requirements: string;
}

interface FormErrors {
  name?: string;
  description?: string;
  problem_solved?: string;
  target_audience?: string;
  platform?: string;
  tone?: string;
  requirements?: string;
}

type AppState = 'idle' | 'generating' | 'complete';
type FeedbackState = 'idle' | 'saving' | 'saved';

export default function CreateScreen() {
  const [brief, setBrief] = useState<ProductBrief>({
    name: '',
    category: '',
    description: '',
    features: [],
    problem_solved: '',
    target_audience: '',
    platform: '',
    tone: '',
    requirements: ''
  });

  const [featureInput, setFeatureInput] = useState('');
  const [errors, setErrors] = useState<FormErrors>({});
  
  const [appState, setAppState] = useState<AppState>('idle');
  const [productId, setProductId] = useState<number | null>(null);
  const [generation, setGeneration] = useState<Generation | null>(null);
  
  const [feedbackState, setFeedbackState] = useState<FeedbackState>('idle');
  const [feedbackType, setFeedbackType] = useState<string>('');
  const [feedbackComment, setFeedbackComment] = useState<string>('');

  const addFeature = () => {
    const trimmed = featureInput.trim();
    if (trimmed && !brief.features.includes(trimmed)) {
      setBrief({ ...brief, features: [...brief.features, trimmed] });
      setFeatureInput('');
    }
  };

  const removeFeature = (idx: number) => {
    setBrief({ ...brief, features: brief.features.filter((_, i) => i !== idx) });
  };

  const validate = (): boolean => {
    const newErrors: FormErrors = {};
    if (!brief.name.trim()) newErrors.name = 'Product name is required.';
    if (!brief.description.trim()) newErrors.description = 'Please describe the product.';
    if (!brief.problem_solved.trim()) newErrors.problem_solved = 'Please explain the problem it solves.';
    if (!brief.target_audience.trim()) newErrors.target_audience = 'Target audience is required.';
    if (!brief.platform) newErrors.platform = 'Please select a platform.';
    if (!brief.tone) newErrors.tone = 'Please select a tone.';
    if (!brief.requirements.trim()) newErrors.requirements = 'Creative direction is required.';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) {
      setAppState('generating');
      try {
        const prod = await createProduct({
          name: brief.name,
          category: brief.category,
          description: brief.description,
          features: brief.features,
          problem_solved: brief.problem_solved,
          target_audience: brief.target_audience,
          platform: brief.platform,
          tone: brief.tone,
          requirements: brief.requirements
        });
        setProductId(prod.id);
        const gen = await generateContent(prod.id, brief.tone, brief.requirements);
        setGeneration(gen);
        setAppState('complete');
      } catch (err) {
        console.error("Failed to generate content", err);
        setAppState('idle');
      }
    }
  };

  const handleStartOver = () => {
    setAppState('idle');
    setProductId(null);
    setGeneration(null);
    setFeedbackState('idle');
    setFeedbackType('');
    setFeedbackComment('');
    setBrief({
      name: '', category: '', description: '', features: [],
      problem_solved: '', target_audience: '', platform: '',
      tone: '', requirements: ''
    });
  };

  const autoFillTest = () => {
    setBrief({
      name: 'Aura Drops',
      category: 'Wellness',
      description: 'A premium liquid supplement infused with adaptogens and L-theanine designed to reduce anxiety and promote a calm focus.',
      features: ['Zero sugar', 'Fast acting', 'Pocket sized'],
      problem_solved: 'Feeling stressed but needing to stay productive without the caffeine jitters.',
      target_audience: 'Stressed-out Gen-Z students and young professionals.',
      platform: 'Instagram',
      tone: 'Gen-Z',
      requirements: 'Make it sound highly aesthetic, slightly sarcastic about hustle culture, and relatable.'
    });
  };

  const handleFeedbackSubmit = async () => {
    if (!generation || !feedbackType) return;
    setFeedbackState('saving');
    try {
      await submitFeedback({
        generation_id: generation.generation_id,
        feedback_type: feedbackType,
        comment: feedbackComment || undefined
      });
      setFeedbackState('saved');
    } catch (err) {
      console.error("Failed to submit feedback", err);
      setFeedbackState('idle');
    }
  };

  const handleGenerateAnother = async () => {
    if (!productId) return;
    setAppState('generating');
    setFeedbackState('idle');
    setFeedbackType('');
    setFeedbackComment('');
    try {
      const gen = await generateContent(productId, brief.tone, `${brief.requirements}\nCreate a fresh alternate angle.`);
      setGeneration(gen);
      setAppState('complete');
    } catch (err) {
      console.error("Failed to generate content", err);
      setAppState('idle');
    }
  };

  if (appState === 'generating') {
    return (
      <div className="mx-auto max-w-3xl px-6 min-h-[60vh] flex flex-col items-center justify-center animate-in fade-in duration-1000 ease-out text-center">
        <div className="text-[11px] uppercase tracking-[0.25em] font-semibold text-[var(--color-muted)] mb-8">
          Kairos
        </div>
        <h1 className="font-display text-5xl md:text-6xl tracking-tight text-[var(--color-ink)] mb-12">
          Finding your angle.
        </h1>
        <p className="text-lg text-[var(--color-muted)] leading-relaxed max-w-[32ch] mx-auto mb-20">
          Your brief is in.<br/>
          Now we're turning it into something people might actually share.
        </p>

        {/* Subtle geometric progress indicator */}
        <div className="flex flex-col items-center justify-center gap-2">
          <div className="w-1.5 h-1.5 rounded-full bg-[var(--color-ink)] animate-[pulse_2s_ease-in-out_infinite]" />
          <div className="flex gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-[var(--color-ink)] animate-[pulse_2s_ease-in-out_0.5s_infinite]" />
            <div className="w-1.5 h-1.5 rounded-full bg-[var(--color-ink)] animate-[pulse_2s_ease-in-out_1s_infinite]" />
          </div>
          <div className="w-1.5 h-1.5 rounded-full bg-[var(--color-ink)] animate-[pulse_2s_ease-in-out_1.5s_infinite]" />
        </div>
      </div>
    );
  }

  if (appState === 'complete' && generation) {
    const feedbackOptions = [
      { label: 'Funnier', value: 'funnier' },
      { label: 'More Gen-Z', value: 'more_trendy' },
      { label: 'More relatable', value: 'more_relatable' },
      { label: 'Stronger hook', value: 'better_hook' },
      { label: 'More trendy', value: 'more_trendy' },
      { label: 'Shorter', value: 'shorter' },
      { label: 'More professional', value: 'more_professional' }
    ];

    return (
      <div className="mx-auto max-w-4xl px-6 py-24 sm:px-12 pb-48 animate-in fade-in duration-700 ease-out">
        
        {/* START OVER */}
        <div className="mb-16">
          <button 
            onClick={handleStartOver}
            className="text-[13px] font-medium text-[var(--color-muted)] hover:text-[var(--color-ink)] transition-colors"
          >
            ← Start over
          </button>
        </div>

        {/* RESULTS TOP-LEVEL */}
        <div className="space-y-6 mb-16">
          <h2 className="text-[11px] uppercase tracking-[0.18em] font-semibold text-[var(--color-muted)]">Your Angle</h2>
          
          <div className="flex flex-wrap items-center gap-2 text-[13px] text-[var(--color-muted)] font-medium">
            <span>{brief.platform}</span>
            <span>·</span>
            <span>{brief.tone}</span>
            {generation.trend?.format && (
              <>
                <span>·</span>
                <span>{generation.trend.format}</span>
              </>
            )}
          </div>

          <h1 className="font-display text-5xl md:text-7xl leading-[1.05] tracking-tight text-[var(--color-ink)] pb-4">
            {generation.hook}
          </h1>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-12 gap-12 mb-24">
          
          {/* LEFT COL: VIRAL & TREND */}
          <div className="md:col-span-4 space-y-12">
            <div>
              <h2 className="text-[11px] uppercase tracking-[0.18em] font-semibold text-[var(--color-muted)] mb-3">Viral Potential</h2>
              <div className="flex items-baseline gap-2 mb-2">
                <span className="font-display text-4xl text-[var(--color-ink)]">{generation.viral_score}</span>
                <span className="text-[13px] font-medium text-[var(--color-muted)]">/ 100</span>
              </div>
              <p className="text-[14px] text-[var(--color-muted)] leading-relaxed">
                {generation.viral_score >= 80 ? 'Strong potential for reach based on current formats.' : 'Solid engagement expected.'}
              </p>
            </div>

            {generation.trend?.reason && (
              <div>
                <h2 className="text-[11px] uppercase tracking-[0.18em] font-semibold text-[var(--color-muted)] mb-3">Why this works</h2>
                <p className="text-[15px] text-[var(--color-ink)] leading-relaxed">
                  {generation.trend.reason}
                </p>
              </div>
            )}
          </div>

          {/* RIGHT COL: CONTENT ASSETS */}
          <div className="md:col-span-8 space-y-16">
            
            {/* MEME */}
            {generation.meme?.gif?.gif_url && (
              <div>
                <h2 className="text-[11px] uppercase tracking-[0.18em] font-semibold text-[var(--color-muted)] mb-4">Meme Asset</h2>
                <div className="overflow-hidden rounded-[var(--radius-lg)] border border-[var(--color-border)]">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={generation.meme.gif.gif_url} alt={generation.meme.search_query || "Meme"} className="w-full object-cover" />
                </div>
                <p className="mt-3 text-[13px] text-[var(--color-muted)]">{generation.meme.format} (Query: {generation.meme.search_query})</p>
              </div>
            )}

            {/* DIALOGUE */}
            {generation.dialogue && generation.dialogue.length > 0 && (
              <div>
                <h2 className="text-[11px] uppercase tracking-[0.18em] font-semibold text-[var(--color-muted)] mb-6">Dialogue</h2>
                <div className="space-y-4">
                  {generation.dialogue.map((d, i) => (
                    <div key={i} className="flex flex-col">
                      <span className="text-[11px] uppercase tracking-wider font-semibold text-[var(--color-muted)] mb-1">{d.speaker}</span>
                      <span className="text-[16px] text-[var(--color-ink)] leading-relaxed">{d.line}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* REEL BLUEPRINT */}
            {generation.script && generation.script.length > 0 && (
              <div>
                <h2 className="text-[11px] uppercase tracking-[0.18em] font-semibold text-[var(--color-muted)] mb-6">Reel Blueprint</h2>
                <div className="space-y-6">
                  {generation.script.map((scene, i) => (
                    <div key={i} className="pl-4 border-l border-[var(--color-border)]">
                      <div className="text-[12px] font-medium text-[var(--color-muted)] mb-2">{scene.time}</div>
                      <div className="text-[14px] text-[var(--color-ink)] mb-1"><span className="font-semibold text-[var(--color-muted)]">Visual:</span> {scene.visual}</div>
                      <div className="text-[14px] text-[var(--color-ink)] mb-1"><span className="font-semibold text-[var(--color-muted)]">Voice:</span> {scene.voice}</div>
                      {scene.text_overlay && (
                        <div className="text-[14px] text-[var(--color-ink)]"><span className="font-semibold text-[var(--color-muted)]">Overlay:</span> "{scene.text_overlay}"</div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* CAPTION & HASHTAGS */}
            {(generation.caption || (generation.hashtags && generation.hashtags.length > 0)) && (
              <div>
                <h2 className="text-[11px] uppercase tracking-[0.18em] font-semibold text-[var(--color-muted)] mb-4">Caption</h2>
                <div className="bg-[var(--color-surface)] p-6 rounded-[var(--radius-md)] border border-[var(--color-border)]">
                  {generation.caption && (
                    <p className="text-[15px] text-[var(--color-ink)] leading-relaxed mb-4 whitespace-pre-wrap">{generation.caption}</p>
                  )}
                  {generation.hashtags && generation.hashtags.length > 0 && (
                    <p className="text-[14px] text-[var(--color-accent)] font-medium">
                      {generation.hashtags.join(' ')}
                    </p>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* FEEDBACK SECTION */}
        <hr className="border-[var(--color-border)] mb-16" />
        
        <div className="max-w-2xl">
          {feedbackState === 'saved' ? (
            <div className="animate-in fade-in slide-in-from-bottom-2 duration-500">
              <h2 className="font-display text-3xl text-[var(--color-ink)] mb-6">Preference saved.</h2>
              <button 
                onClick={handleGenerateAnother}
                className="rounded-[var(--radius-md)] bg-[var(--color-ink)] text-[var(--color-bg)] px-8 py-3 text-[14px] font-medium hover:bg-black active:scale-[0.98] transition-all"
              >
                Find another angle →
              </button>
            </div>
          ) : (
            <div>
              <h2 className="font-display text-3xl text-[var(--color-ink)] mb-8">Refine this angle.</h2>
              
              <div className="flex flex-wrap gap-2 mb-8">
                {feedbackOptions.map(opt => (
                  <button
                    key={opt.value}
                    type="button"
                    onClick={() => setFeedbackType(opt.value)}
                    className={`px-4 py-2 rounded-full text-[13px] font-medium transition-colors border ${
                      feedbackType === opt.value 
                        ? 'bg-[var(--color-ink)] text-[var(--color-bg)] border-[var(--color-ink)]' 
                        : 'bg-transparent text-[var(--color-ink)] border-[var(--color-border)] hover:border-[var(--color-ink)]'
                    }`}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>

              <div className="mb-6">
                <label htmlFor="feedbackComment" className="block text-[14px] font-medium text-[var(--color-ink)] mb-3">
                  Tell KAIROS how to adjust this.
                </label>
                <textarea
                  id="feedbackComment"
                  value={feedbackComment}
                  onChange={(e) => setFeedbackComment(e.target.value)}
                  placeholder="e.g. Needs more energy in the hook..."
                  className="w-full bg-[var(--color-surface)] border border-[var(--color-border)] px-4 py-3 text-[15px] text-[var(--color-ink)] placeholder-[var(--color-muted)] focus:outline-none focus:border-[var(--color-ink)] transition-colors rounded-[var(--radius-sm)] min-h-[100px] resize-y"
                />
              </div>

              <button 
                onClick={handleFeedbackSubmit}
                disabled={!feedbackType || feedbackState === 'saving'}
                className="rounded-[var(--radius-md)] bg-[var(--color-ink)] text-[var(--color-bg)] px-8 py-3 text-[14px] font-medium hover:bg-black active:scale-[0.98] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {feedbackState === 'saving' ? 'Saving...' : 'Improve →'}
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Common input styling class for high-end editorial feel
  const inputClass = "w-full bg-[var(--color-surface)] border border-[var(--color-border)] px-4 py-3 text-[15px] text-[var(--color-ink)] placeholder-[var(--color-muted)] focus:outline-none focus:border-[var(--color-ink)] transition-colors rounded-[var(--radius-sm)]";
  const labelClass = "block text-[13px] font-medium text-[var(--color-ink)] mb-2";
  const sectionHeaderClass = "text-[11px] uppercase tracking-[0.18em] font-semibold text-[var(--color-muted)] mb-8";
  
  return (
    <div className="w-full h-[calc(100vh-64px)] overflow-hidden flex flex-col md:flex-row animate-in fade-in duration-500 bg-[var(--color-bg)]">
      
      {/* LEFT COL: CREATIVE BRIEF FORM (50%) */}
      <div className="w-full md:w-1/2 h-full flex flex-col overflow-y-auto custom-scrollbar px-6 py-6 md:px-10 md:py-6 lg:px-12 lg:py-6">
        <form onSubmit={handleSubmit} className="flex flex-col gap-5 w-full max-w-[600px] ml-auto mr-0 xl:mr-4" noValidate>
          
          {/* 01 THE PRODUCT */}
          <section>
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-baseline gap-2">
                <span className="font-mono text-[var(--color-muted)] text-[10px]">01</span>
                <h2 className="text-[11px] uppercase tracking-[0.18em] font-semibold text-[var(--color-ink)]">The Product</h2>
              </div>
              <button 
                type="button" 
                onClick={autoFillTest}
                className="text-[11px] font-medium text-[var(--color-muted)] hover:text-[var(--color-ink)] transition-colors underline underline-offset-2"
              >
                Auto-fill test data
              </button>
            </div>
            
            <div className="space-y-2.5">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
                <div>
                  <label htmlFor="name" className="block text-[12px] font-medium text-[var(--color-ink)] mb-1">Product name</label>
                  <input 
                    id="name"
                    type="text" 
                    value={brief.name}
                    onChange={e => setBrief({...brief, name: e.target.value})}
                    className={`${inputClass} py-1.5 text-[13px] h-[38px]`}
                    placeholder="e.g. Aura Drops"
                  />
                </div>
                <div>
                  <label htmlFor="category" className="block text-[12px] font-medium text-[var(--color-ink)] mb-1">Category (Optional)</label>
                  <input 
                    id="category"
                    type="text" 
                    value={brief.category}
                    onChange={e => setBrief({...brief, category: e.target.value})}
                    className={`${inputClass} py-1.5 text-[13px] h-[38px]`}
                    placeholder="e.g. Fashion"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="description" className="block text-[12px] font-medium text-[var(--color-ink)] mb-1">Description</label>
                <textarea 
                  id="description"
                  value={brief.description}
                  onChange={e => setBrief({...brief, description: e.target.value})}
                  className={`${inputClass} h-[60px] resize-none py-2 text-[13px]`}
                  placeholder="What exactly is this product?"
                />
              </div>

              <div>
                <label htmlFor="featureInput" className="block text-[12px] font-medium text-[var(--color-ink)] mb-1">Features</label>
                <div className="flex gap-2">
                  <input 
                    id="featureInput"
                    type="text" 
                    value={featureInput}
                    onChange={e => setFeatureInput(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && (e.preventDefault(), addFeature())}
                    className={`${inputClass} py-1.5 text-[13px] h-[38px]`}
                    placeholder="Add a key feature"
                  />
                  <button 
                    type="button" 
                    onClick={addFeature}
                    className="px-4 h-[38px] border border-[var(--color-border)] rounded-[var(--radius-sm)] text-[12px] font-medium text-[var(--color-ink)] hover:border-[var(--color-ink)] transition-colors shrink-0 bg-transparent"
                  >
                    Add
                  </button>
                </div>
                {brief.features.length > 0 && (
                  <ul className="space-y-1 mt-1.5">
                    {brief.features.map((feature, idx) => (
                      <li key={idx} className="flex items-center justify-between py-1 px-2.5 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-[var(--radius-sm)] text-[12px]">
                        <span>{feature}</span>
                        <button 
                          type="button" 
                          onClick={() => removeFeature(idx)}
                          className="text-[var(--color-muted)] hover:text-[var(--color-error)] transition-colors"
                        >
                          ✕
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </section>

          {/* 02 WHO + WHERE */}
          <section>
            <div className="flex items-baseline gap-2 mb-2">
              <span className="font-mono text-[var(--color-muted)] text-[10px]">02</span>
              <h2 className="text-[11px] uppercase tracking-[0.18em] font-semibold text-[var(--color-ink)]">Who + Where</h2>
            </div>

            <div className="space-y-2.5">
              <div>
                <label htmlFor="problem_solved" className="block text-[12px] font-medium text-[var(--color-ink)] mb-1">Problem</label>
                <textarea 
                  id="problem_solved"
                  value={brief.problem_solved}
                  onChange={e => setBrief({...brief, problem_solved: e.target.value})}
                  className={`${inputClass} h-[60px] resize-none py-2 text-[13px]`}
                  placeholder="e.g. Looking stylish but feeling like you're wearing a blanket."
                />
              </div>

              <div>
                <label htmlFor="target_audience" className="block text-[12px] font-medium text-[var(--color-ink)] mb-1">Audience</label>
                <input 
                  id="target_audience"
                  type="text" 
                  value={brief.target_audience}
                  onChange={e => setBrief({...brief, target_audience: e.target.value})}
                  className={`${inputClass} py-1.5 text-[13px] h-[38px]`}
                  placeholder="e.g. Streetwear enthusiasts."
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
                <div>
                  <label htmlFor="platform" className="block text-[12px] font-medium text-[var(--color-ink)] mb-1">Platform</label>
                  <div className="relative">
                    <select 
                      id="platform"
                      value={brief.platform}
                      onChange={e => setBrief({...brief, platform: e.target.value})}
                      className={`${inputClass} py-1.5 h-[38px] text-[13px] appearance-none cursor-pointer`}
                    >
                      <option value="" disabled>Select platform...</option>
                      <option value="Instagram">Instagram</option>
                      <option value="YouTube Shorts">YouTube Shorts</option>
                      <option value="Both">Both</option>
                    </select>
                    <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-[var(--color-muted)]">▼</div>
                  </div>
                </div>
                
                <div>
                  <label htmlFor="tone" className="block text-[12px] font-medium text-[var(--color-ink)] mb-1">Tone</label>
                  <div className="relative">
                    <select 
                      id="tone"
                      value={brief.tone}
                      onChange={e => setBrief({...brief, tone: e.target.value})}
                      className={`${inputClass} py-1.5 h-[38px] text-[13px] appearance-none cursor-pointer`}
                    >
                      <option value="" disabled>Select tone...</option>
                      <option value="Funny">Funny</option>
                      <option value="Sarcastic">Sarcastic</option>
                      <option value="Gen-Z">Gen-Z</option>
                      <option value="Professional">Professional</option>
                      <option value="Educational">Educational</option>
                    </select>
                    <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-[var(--color-muted)]">▼</div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* 03 THE ANGLE */}
          <section>
            <div className="flex items-baseline gap-2 mb-2">
              <span className="font-mono text-[var(--color-muted)] text-[10px]">03</span>
              <h2 className="text-[11px] uppercase tracking-[0.18em] font-semibold text-[var(--color-ink)]">The Angle</h2>
            </div>
            <div className="flex flex-col">
              <label htmlFor="requirements" className="block text-[12px] font-medium text-[var(--color-ink)] mb-1">
                Creative Direction
              </label>
              <textarea 
                id="requirements"
                value={brief.requirements}
                onChange={e => setBrief({...brief, requirements: e.target.value})}
                className={`${inputClass} resize-none text-[13px] leading-relaxed py-2 h-[70px]`}
                placeholder="Make it Hinglish, slightly savage, relatable..."
              />
            </div>
          </section>

          {/* SUBMIT */}
          <div className="pt-2 pb-6">
            <button 
              type="submit"
              className="w-full sm:w-auto rounded-[var(--radius-sm)] bg-[var(--color-ink)] text-[var(--color-bg)] px-8 h-[44px] text-[13px] font-medium hover:bg-black active:scale-[0.98] transition-all shadow-sm"
            >
              Find my angle →
            </button>
          </div>
        </form>
      </div>

      {/* RIGHT COL: OUTPUT PREVIEW (50%) */}
      <div className="w-full md:w-1/2 h-full overflow-y-auto custom-scrollbar border-t md:border-t-0 md:border-l border-[var(--color-border)] px-6 py-8 md:px-12 md:py-8 lg:px-16 lg:py-10 bg-[var(--color-bg)]">
        <div className="w-full max-w-[600px] mr-auto ml-0 xl:ml-8">
          <h2 className="text-[12px] uppercase tracking-[0.2em] font-semibold text-[var(--color-muted)] mb-8">
            Your Creative Brief
          </h2>
          
          <div className="space-y-6">
            <div>
              <div className="text-[10px] uppercase tracking-widest text-[var(--color-muted)] mb-1.5">Product</div>
              <div className={`text-[16px] leading-tight ${brief.name ? 'text-[var(--color-ink)]' : 'text-[var(--color-muted)] italic'}`}>
                {brief.name || "Waiting for your product..."}
              </div>
            </div>

            <div>
              <div className="text-[10px] uppercase tracking-widest text-[var(--color-muted)] mb-1.5">Audience</div>
              <div className={`text-[16px] leading-tight ${brief.target_audience ? 'text-[var(--color-ink)]' : 'text-[var(--color-muted)] italic'}`}>
                {brief.target_audience || "Who you're speaking to..."}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <div className="text-[10px] uppercase tracking-widest text-[var(--color-muted)] mb-1.5">Platform</div>
                <div className={`text-[15px] font-medium ${brief.platform ? 'text-[var(--color-ink)]' : 'text-[var(--color-muted)]'}`}>
                  {brief.platform || "—"}
                </div>
              </div>
              <div>
                <div className="text-[10px] uppercase tracking-widest text-[var(--color-muted)] mb-1.5">Tone</div>
                <div className={`text-[15px] font-medium ${brief.tone ? 'text-[var(--color-ink)]' : 'text-[var(--color-muted)]'}`}>
                  {brief.tone || "—"}
                </div>
              </div>
            </div>
          </div>

          <hr className="my-10 border-[var(--color-border)]" />

          <h2 className="text-[12px] uppercase tracking-[0.2em] font-semibold text-[var(--color-muted)] mb-6">
            KAIROS will find:
          </h2>
          <div className="space-y-4">
            <div className="pl-5 border-l-2 border-[var(--color-border)] font-display text-[18px] text-[var(--color-muted)]">HOOK</div>
            <div className="pl-5 border-l-2 border-[var(--color-border)] font-display text-[18px] text-[var(--color-muted)]">MEME</div>
            <div className="pl-5 border-l-2 border-[var(--color-border)] font-display text-[18px] text-[var(--color-muted)]">DIALOGUE</div>
            <div className="pl-5 border-l-2 border-[var(--color-border)] font-display text-[18px] text-[var(--color-muted)]">REEL</div>
          </div>
        </div>
      </div>
    </div>
  );
}
