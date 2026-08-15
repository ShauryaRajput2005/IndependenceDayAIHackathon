import { useEffect, useState } from 'react'
import { createFileRoute } from '@tanstack/react-router'
import { AnimatePresence, motion } from 'framer-motion'
import { ArrowRight, Check, Copy, Flame, Heart, MessageCircle, Play, RefreshCw, Sparkles, WandSparkles } from 'lucide-react'
import { toast } from 'sonner'
import { API_BASE_URL, createFeedback, createProduct, generateContent, healthCheck } from '@/lib/api'

export const Route = createFileRoute('/')({
  head: () => ({
    meta: [
      { title: 'KAIROS' },
      { name: 'description', content: 'Turn one product idea into a complete, trend-aware content system.' },
    ],
  }),
  component: Home,
})

type FormState = {
  brand: string
  audience: string
  product: string
  tone: string
  platform: string
  requirements: string
}

type Output = {
  generationId?: number
  productId?: number
  trend: string
  hook: string
  meme: string
  dialogue: string[]
  script: { label: string; detail: string }[]
  caption: string
  mediaUrl?: string | null
  mediaTitle?: string | null
  mediaSource?: string | null
  mediaType?: string | null
  mediaStatus?: string | null
  mediaReason?: string | null
}

const initialForm: FormState = {
  brand: '',
  audience: '',
  product: '',
  tone: 'Meme-first',
  platform: 'Instagram + Shorts',
  requirements: '',
}

const tones = ['Meme-first', 'Dry & witty', 'Soft & relatable', 'Founder mode', 'Luxury casual']
const platforms = ['Instagram', 'YouTube Shorts', 'Instagram + Shorts']
const angleDirections = [
  'Switch to a contrarian POV with a sharper punchline.',
  'Use an unexpected everyday situation and a fresh meme setup.',
  'Make the angle more visual, with a different opening scene.',
  'Use a creator-style confession angle with a new hook.',
  'Make the joke more specific to the audience pain point.',
]

function isVideoMedia(url?: string | null) {
  if (!url) return false
  const cleanUrl = url.split('?')[0].toLowerCase()
  return ['.mp4', '.webm', '.mov', '.m4v'].some((extension) => cleanUrl.endsWith(extension)) || url.toLowerCase().includes('format=mp4')
}

function buildDraftOutput(form: FormState): Output {
  const brand = form.brand.trim() || 'Your brand'
  const audience = form.audience.trim() || 'your audience'
  const product = form.product.trim() || 'your product'

  return {
    trend: `${audience} insight`,
    hook: `${brand} is ready to turn ${product} into a scroll-stopping angle.`,
    meme: `${audience} Relatable POV`,
    dialogue: ['Add your brief', 'Generate to get backend-written dialogue.'],
    script: [
      { label: '0-3 sec', detail: 'Your backend-generated opening scene appears here.' },
      { label: '3-8 sec', detail: 'The product moment updates after generation.' },
    ],
    caption: 'Generate content to create a platform-ready caption.',
  }
}

function Home() {
  const [intro, setIntro] = useState(true)
  const [form, setForm] = useState(initialForm)
  const [step, setStep] = useState<'home' | 'form' | 'results'>('home')
  const [output, setOutput] = useState<Output | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [apiOnline, setApiOnline] = useState<boolean | null>(null)
  const [feedback, setFeedback] = useState<string | null>(null)
  const [angleIndex, setAngleIndex] = useState(0)
  const previewOutput = output ?? buildDraftOutput(form)
  const canGenerate = Boolean(form.brand.trim() && form.audience.trim() && form.product.trim())

  useEffect(() => {
    const timer = window.setTimeout(() => setIntro(false), 900)
    return () => window.clearTimeout(timer)
  }, [])

  useEffect(() => {
    healthCheck().then(() => setApiOnline(true)).catch(() => setApiOnline(false))
  }, [])

  const update = (key: keyof FormState, value: string) => setForm((current) => ({ ...current, [key]: value }))
  const backendPlatform = (platform: string) => platform.includes('Instagram') && platform.includes('Shorts') ? 'Both' : platform.includes('Shorts') ? 'YouTube Shorts' : 'Instagram'
  const backendTone = (tone: string) => tone === 'Meme-first' ? 'Meme Style' : tone === 'Dry & witty' ? 'Sarcastic' : tone === 'Soft & relatable' ? 'Emotional' : tone === 'Founder mode' ? 'Professional' : tone === 'Luxury casual' ? 'Luxury' : 'Funny'

  async function generate(variation = false) {
    if (!canGenerate) {
      toast.error('Add brand, audience, and product first')
      setStep('form')
      return
    }
    setIsGenerating(true)
    setFeedback(null)
    try {
      const nextAngleIndex = variation ? angleIndex + 1 : angleIndex
      const angleDirection = angleDirections[nextAngleIndex % angleDirections.length]
      const requirements = variation
        ? `${form.requirements}\nCreate a fresh alternate angle. Variation #${nextAngleIndex}: ${angleDirection}`
        : form.requirements
      const tone = backendTone(variation ? tones[nextAngleIndex % tones.length] : form.tone)
      if (variation) setAngleIndex(nextAngleIndex)
      const product = await createProduct({
        name: form.brand,
        category: 'Consumer Brand',
        description: form.product,
        features: form.product,
        problem: 'Audience needs scroll-stopping content that feels native to the platform',
        audience: form.audience,
        platform: backendPlatform(form.platform),
        tone,
        requirements,
      })
      const content = await generateContent(product.product_id, tone, requirements)
      const selectedMediaType = content.selected_media_type || content.meme?.mediaType || null
      const mediaUrl = selectedMediaType === 'clip'
        ? content.meme?.url || content.meme?.preview || null
        : content.meme?.preview || content.meme?.url || null
      setOutput({
        generationId: content.generation_id,
        productId: content.product_id,
        trend: content.klipy_query,
        hook: content.hook,
        meme: content.meme_format,
        dialogue: content.dialogue,
        script: content.script.map((scene) => ({ label: scene.time, detail: scene.scene })),
        caption: content.caption,
        mediaUrl,
        mediaTitle: content.meme?.title || null,
        mediaSource: content.meme?.source || null,
        mediaType: selectedMediaType,
        mediaStatus: content.meme?.providerStatus || null,
        mediaReason: content.media_reason || null,
      })
      setApiOnline(true)
      setStep('results')
      toast.success('Generated from backend', { description: API_BASE_URL })
    } catch (error) {
      setApiOnline(false)
      toast.error('Backend generation failed', { description: error instanceof Error ? error.message : 'Check FastAPI is running.' })
    } finally {
      setIsGenerating(false)
    }
  }

  async function submitFeedback(value: string) {
    setFeedback(value)
    if (!output?.generationId) {
      toast.success('Preference saved locally')
      return
    }
    try {
      await createFeedback(output.generationId, value)
      toast.success('Feedback saved to backend')
    } catch (error) {
      toast.error('Could not save feedback', { description: error instanceof Error ? error.message : 'Check backend connection.' })
    }
  }

  async function copy(text: string) {
    await navigator.clipboard?.writeText(text)
    toast.success('Copied to clipboard')
  }

  if (intro) {
    return (
      <div className="fixed inset-0 z-50 grid place-items-center bg-primary text-primary-foreground">
        <div className="text-center">
          <div className="mx-auto grid size-16 place-items-center rounded-2xl bg-primary-foreground/10">
            <Sparkles className="size-7 text-accent" />
          </div>
          <p className="mt-5 font-serif text-4xl tracking-tight">KAIROS</p>
        </div>
      </div>
    )
  }

  return (
    <main className="min-h-dvh bg-background text-foreground">
      <nav className="sticky top-0 z-40 flex items-center justify-between border-b border-border/70 bg-background/90 px-5 py-4 backdrop-blur-xl md:px-10">
        <button onClick={() => setStep('home')} className="flex items-center gap-2.5" aria-label="Back to home">
          <span className="grid size-8 place-items-center rounded-lg bg-primary text-primary-foreground"><Sparkles className="size-4" /></span>
          <span className="font-semibold tracking-tight">KAIROS</span>
        </button>
        <div className="flex items-center gap-3">
          <span className={`rounded-full px-3 py-1 text-xs font-semibold ${apiOnline ? 'bg-green-100 text-green-700' : apiOnline === false ? 'bg-red-100 text-red-700' : 'bg-secondary text-muted-foreground'}`}>
            {apiOnline ? 'Backend connected' : apiOnline === false ? 'Backend offline' : 'Checking backend'}
          </span>
          <button onClick={() => setStep('form')} className="inline-flex items-center gap-2 rounded-full bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground">
            Open studio <ArrowRight className="size-4" />
          </button>
        </div>
      </nav>

      <AnimatePresence mode="wait">
        {step === 'home' && (
          <motion.section key="home" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="mx-auto grid min-h-[calc(100dvh-73px)] max-w-7xl items-center gap-12 px-5 py-16 md:grid-cols-[1.05fr_.95fr] md:px-10 lg:px-20">
            <div>
              <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-3 py-1.5 text-xs font-semibold uppercase tracking-[.16em] text-primary">
                <span className="size-1.5 rounded-full bg-accent" /> Backend-powered content intelligence
              </div>
              <h1 className="text-balance font-serif text-5xl leading-[.98] tracking-[-.045em] md:text-7xl">Make your next post feel <em className="text-primary">inevitable.</em></h1>
              <p className="mt-7 max-w-lg text-lg leading-8 text-muted-foreground">KAIROS turns one product thought into backend-generated hooks, memes, dialogues, captions, and short-form scripts.</p>
              <button onClick={() => setStep('form')} className="mt-9 inline-flex items-center gap-3 rounded-full bg-primary px-6 py-3.5 font-semibold text-primary-foreground shadow-lg">
                <WandSparkles className="size-4" /> Create content <ArrowRight className="size-4" />
              </button>
            </div>
            <PreviewCard output={previewOutput} />
          </motion.section>
        )}

        {step === 'form' && (
          <motion.section key="form" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mx-auto min-h-dvh max-w-5xl px-5 pb-20 pt-16 md:px-10">
            <button onClick={() => setStep('home')} className="mb-5 text-sm text-muted-foreground transition hover:text-foreground">Back to studio</button>
            <h1 className="font-serif text-5xl leading-tight tracking-tight">Give your brand a <em className="text-primary">point of view.</em></h1>
            <div className="mt-8 grid gap-5 lg:grid-cols-[1.2fr_.8fr]">
              <div className="rounded-3xl border border-border bg-card p-6 shadow-md md:p-8">
                <div className="grid gap-5 md:grid-cols-2">
                  <Field label="Brand name" value={form.brand} placeholder="KAIROS Labs" onChange={(v) => update('brand', v)} />
                  <Field label="Audience" value={form.audience} placeholder="College students, founders, gamers..." onChange={(v) => update('audience', v)} />
                  <div className="md:col-span-2"><Field label="Product or service" value={form.product} placeholder="Describe what you want to promote" onChange={(v) => update('product', v)} multiline /></div>
                </div>
                <ChoiceGroup label="Platform" options={platforms} value={form.platform} onChange={(v) => update('platform', v)} />
                <ChoiceGroup label="Tone" options={tones} value={form.tone} onChange={(v) => update('tone', v)} />
              </div>
              <div className="flex flex-col gap-5">
                <div className="rounded-3xl border border-border bg-secondary p-6">
                  <Field label="Requirements" value={form.requirements} placeholder="Language, style, things to avoid, or campaign notes" onChange={(v) => update('requirements', v)} multiline />
                </div>
                <div className="rounded-3xl bg-primary p-6 text-primary-foreground">
                  <div className="flex items-center gap-2"><span className="grid size-7 place-items-center rounded-lg bg-accent text-accent-foreground"><Check className="size-4" /></span><p className="font-semibold">Backend generation</p></div>
                  <p className="mt-5 text-sm leading-6 text-primary-foreground/75">Calls /api/product/create and /api/content/generate.</p>
                  <button disabled={isGenerating || !canGenerate} onClick={() => generate()} className="mt-7 flex w-full items-center justify-center gap-2 rounded-xl bg-accent px-4 py-3.5 font-semibold text-accent-foreground disabled:cursor-wait disabled:opacity-70">
                    {isGenerating ? <><RefreshCw className="size-4 animate-spin" /> Generating...</> : <><Sparkles className="size-4" /> Generate content</>}
                  </button>
                </div>
              </div>
            </div>
          </motion.section>
        )}

        {step === 'results' && output && (
          <ResultsView output={output} feedback={feedback} isGenerating={isGenerating} onBack={() => setStep('form')} onGenerate={() => generate(true)} onCopy={copy} onFeedback={submitFeedback} />
        )}
      </AnimatePresence>
    </main>
  )
}

function Field({ label, value, onChange, multiline = false, placeholder = '' }: { label: string; value: string; onChange: (value: string) => void; multiline?: boolean; placeholder?: string }) {
  const className = 'mt-2 w-full rounded-xl border border-border bg-background px-4 py-3 text-sm outline-none transition placeholder:text-muted-foreground/60 focus:border-primary focus:ring-2 focus:ring-primary/15'
  return <label className="block"><span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{label}</span>{multiline ? <textarea rows={4} value={value} placeholder={placeholder} onChange={(event) => onChange(event.target.value)} className={className} /> : <input value={value} placeholder={placeholder} onChange={(event) => onChange(event.target.value)} className={className} />}</label>
}

function ChoiceGroup({ label, options, value, onChange }: { label: string; options: string[]; value: string; onChange: (value: string) => void }) {
  return <div className="mt-8 border-t border-border pt-7"><p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{label}</p><div className="mt-3 flex flex-wrap gap-2">{options.map((item) => <button key={item} onClick={() => onChange(item)} className={`rounded-full border px-4 py-2.5 text-sm transition ${value === item ? 'border-primary bg-primary text-primary-foreground' : 'border-border bg-background hover:border-primary/50'}`}>{item}</button>)}</div></div>
}

function PreviewCard({ output }: { output: Output }) {
  return <div className="rounded-[2rem] border border-primary/10 bg-card p-6 shadow-xl"><p className="font-mono text-[10px] uppercase tracking-[.22em] text-muted-foreground">Live content pulse</p><div className="mt-5 rounded-2xl bg-primary p-5 text-primary-foreground"><p className="text-xs font-semibold uppercase tracking-wider text-primary-foreground/70">Viral hook</p><p className="mt-10 font-serif text-2xl leading-tight">{output.hook}</p></div><div className="mt-4 grid grid-cols-2 gap-3"><div className="rounded-2xl border border-border bg-secondary p-4"><MessageCircle className="size-4 text-primary" /><p className="mt-9 text-sm font-semibold">{output.dialogue.length}-line dialogue</p></div><div className="rounded-2xl border border-border bg-accent p-4 text-accent-foreground"><Play className="size-4" /><p className="mt-9 text-sm font-semibold">{output.script.length} scenes</p></div></div></div>
}

function ResultsView({ output, feedback, isGenerating, onBack, onGenerate, onCopy, onFeedback }: { output: Output; feedback: string | null; isGenerating: boolean; onBack: () => void; onGenerate: () => void; onCopy: (text: string) => void; onFeedback: (value: string) => void }) {
  const isVideo = isVideoMedia(output.mediaUrl)
  return (
    <motion.section initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mx-auto min-h-dvh max-w-7xl px-5 pb-24 pt-16 md:px-10 lg:px-16">
      <div className="flex flex-wrap items-end justify-between gap-6">
        <div>
          <button onClick={onBack} className="mb-5 text-sm text-muted-foreground transition hover:text-foreground">Edit brief</button>
          <p className="font-mono text-xs uppercase tracking-[.2em] text-primary">Content pulse</p>
          <h1 className="mt-3 font-serif text-5xl tracking-tight">The scroll is <em className="text-primary">calling.</em></h1>
          <p className="mt-4 max-w-lg text-muted-foreground">Generated around <span className="font-semibold text-foreground">{output.trend}</span>.</p>
        </div>
        <div className="flex gap-2">
          <button disabled={isGenerating} onClick={onGenerate} className="inline-flex items-center gap-2 rounded-full border border-border bg-card px-4 py-2.5 text-sm font-semibold disabled:cursor-wait disabled:opacity-70"><RefreshCw className={`size-4 ${isGenerating ? 'animate-spin' : ''}`} /> {isGenerating ? 'Generating' : 'New angle'}</button>
          <button onClick={() => onCopy([output.hook, output.dialogue.join('\n'), output.caption].join('\n\n'))} className="inline-flex items-center gap-2 rounded-full bg-primary px-4 py-2.5 text-sm font-semibold text-primary-foreground"><Copy className="size-4" /> Copy all</button>
        </div>
      </div>

      <div className="mt-10 grid gap-4 lg:grid-cols-3">
        <ContentCard label="Viral hook" icon={Flame} className="bg-primary text-primary-foreground lg:col-span-2">
          <p className="font-serif text-3xl leading-tight md:text-5xl">{output.hook}</p>
        </ContentCard>

        <ContentCard label="Meme format" icon={Heart} className="border-border bg-white text-slate-950">
          <p className="font-serif text-3xl leading-tight">{output.meme}</p>
        </ContentCard>

        <ContentCard label={`Selected media${output.mediaType ? ` - ${output.mediaType}` : ''}`} icon={Play} className="lg:col-span-1">
          {output.mediaUrl ? (
            isVideo ? (
              <video src={output.mediaUrl} controls muted loop playsInline className="aspect-video w-full rounded-2xl bg-black object-contain" />
            ) : (
              <img src={output.mediaUrl} alt={output.mediaTitle || 'Generated media'} className="aspect-video w-full rounded-2xl object-contain bg-black" />
            )
          ) : (
            <div className="grid aspect-video place-items-center rounded-2xl border border-dashed border-border bg-secondary p-4 text-center text-sm text-muted-foreground">No playable URL returned yet</div>
          )}
          <p className="mt-3 text-xs text-muted-foreground">{output.mediaTitle || 'KLIPY media'} - {output.mediaSource || 'pending'} - {output.mediaStatus || 'no status'}</p>
          {output.mediaUrl && <a href={output.mediaUrl} target="_blank" rel="noreferrer" className="mt-3 inline-flex text-xs font-semibold text-primary hover:underline">Open media URL</a>}
          {output.mediaReason && <p className="mt-2 text-xs leading-5 text-muted-foreground">{output.mediaReason}</p>}
        </ContentCard>

        <ContentCard label="Dialogue" icon={MessageCircle}>
          <div className="space-y-4">{output.dialogue.map((line, index) => <div key={`${line}-${index}`} className="flex gap-3"><span className="grid size-6 shrink-0 place-items-center rounded-full bg-secondary font-mono text-[10px] text-primary">{index + 1}</span><p className="text-lg leading-7">{line}</p></div>)}</div>
        </ContentCard>

        <ContentCard label="Reel script" icon={Play} className="lg:col-span-2">
          <div className="space-y-5">{output.script.map((scene) => <div key={`${scene.label}-${scene.detail}`} className="grid gap-1 border-b border-border pb-5 last:border-0 last:pb-0 md:grid-cols-[8rem_1fr]"><p className="font-mono text-xs uppercase tracking-wider text-primary">{scene.label}</p><p className="text-sm leading-6 text-muted-foreground">{scene.detail}</p></div>)}</div>
        </ContentCard>

        <ContentCard label="Caption" icon={Sparkles} className="lg:col-span-3">
          <p className="text-xl leading-8">{output.caption}</p>
        </ContentCard>
      </div>

      <div className="mt-14 rounded-3xl border border-border bg-secondary p-6 md:p-8">
        <div className="flex flex-wrap items-center justify-between gap-4"><div><p className="font-serif text-2xl">Tune the next one</p><p className="mt-1 text-sm text-muted-foreground">Feedback is saved through /api/feedback/create.</p></div>{feedback && <span className="rounded-full bg-card px-3 py-1.5 text-xs font-semibold text-primary">Saved: {feedback}</span>}</div>
        <div className="mt-6 flex flex-wrap gap-2">{['More like this', 'Make it funnier', 'More professional', 'Avoid this style'].map((label) => <button key={label} onClick={() => onFeedback(label)} className="inline-flex items-center gap-2 rounded-full border border-border bg-card px-4 py-2.5 text-sm font-semibold"><Heart className="size-3.5" /> {label}</button>)}</div>
      </div>
    </motion.section>
  )
}

function ContentCard({ label, icon: Icon, children, className = '' }: { label: string; icon: typeof Flame; children: React.ReactNode; className?: string }) {
  return <article className={`rounded-3xl border border-border bg-card p-6 shadow-sm ${className}`}><div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[.16em] text-muted-foreground"><Icon className="size-4 text-primary" /> {label}</div><div className="mt-6">{children}</div></article>
}
