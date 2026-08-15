"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "motion/react";

const FADE_UP = {
  initial: { opacity: 0, y: 16 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-50px" },
  transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] }
};

export default function LandingPage() {
  const [isMounted, setIsMounted] = useState(false);
  useEffect(() => setIsMounted(true), []);

  return (
    <div className="overflow-x-hidden">
      
      {/* 1. HERO SECTION */}
      <section className="relative px-6 sm:px-12 pt-24 pb-16 mx-auto max-w-[1200px] flex items-center min-h-[70vh] max-h-[900px]">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-8 items-center w-full">
          
          {/* HERO LEFT */}
          <motion.div 
            initial="initial" 
            animate="whileInView"
            variants={{
              initial: {},
              whileInView: { transition: { staggerChildren: 0.1 } }
            }}
            className="max-w-[540px] space-y-8 z-10"
          >
            <motion.h1 
              variants={FADE_UP}
              className="font-display text-5xl md:text-7xl tracking-tight leading-[1.05] text-[var(--color-ink)]"
            >
              Say the right thing<br />
              at the right moment.
            </motion.h1>

            <motion.p variants={FADE_UP} className="text-[17px] text-[var(--color-muted)] leading-relaxed">
              KAIROS turns your product, audience and cultural context into content worth talking about.
            </motion.p>

            <motion.div variants={FADE_UP} className="pt-2">
              <Link 
                href="/create"
                className="group relative inline-flex items-center gap-3 rounded-[var(--radius-md)] bg-[var(--color-ink)] text-[var(--color-bg)] px-8 py-4 text-[15px] font-medium hover:bg-black transition-all active:scale-[0.98] shadow-sm"
              >
                <span>Find my angle</span>
                <motion.span 
                  className="block"
                  transition={{ type: "spring", stiffness: 400, damping: 25 }}
                  whileHover={{ x: 4 }}
                >
                  →
                </motion.span>
              </Link>
            </motion.div>

            <motion.div variants={FADE_UP} className="font-mono text-[11px] uppercase tracking-[0.2em] text-[var(--color-muted)] font-semibold pt-4">
              HOOKS · MEMES · DIALOGUE · REELS
            </motion.div>
          </motion.div>

          {/* HERO RIGHT: CREATIVE OUTPUT DESK */}
          <div className="relative h-[450px] w-full mt-8 lg:mt-0">
            {isMounted && (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="absolute inset-0 flex items-center justify-center pointer-events-none"
              >
                {/* Product */}
                <motion.div 
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  className="absolute top-[5%] left-[10%] bg-white p-5 border border-[var(--color-border)] shadow-sm max-w-[200px]"
                >
                  <div className="text-[10px] font-semibold text-[var(--color-muted)] mb-2 tracking-widest uppercase">Product</div>
                  <div className="text-[14px] font-medium text-[var(--color-ink)]">"Resume builder for students"</div>
                </motion.div>

                {/* Angle */}
                <motion.div 
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0, rotate: 2 }}
                  transition={{ duration: 0.5, delay: 0.35 }}
                  className="absolute top-[25%] right-[15%] bg-[#FAF9F5] p-5 border border-[var(--color-border)] shadow-sm max-w-[220px] z-10"
                >
                  <div className="text-[10px] font-semibold text-[var(--color-accent)] mb-2 tracking-widest uppercase">Angle</div>
                  <div className="text-[15px] font-display text-[var(--color-ink)] italic leading-tight">Students trying to get hired</div>
                </motion.div>

                {/* Hook */}
                <motion.div 
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0, rotate: -2 }}
                  transition={{ duration: 0.5, delay: 0.5 }}
                  className="absolute bottom-[25%] left-[5%] bg-white p-6 border border-[var(--color-border)] shadow-md max-w-[280px] z-20"
                >
                  <div className="text-[10px] font-semibold text-[var(--color-muted)] mb-2 tracking-widest uppercase">Hook</div>
                  <div className="text-[18px] font-display text-[var(--color-ink)] leading-tight">"POV: HR rejected your resume before opening it."</div>
                </motion.div>

                {/* Meme */}
                <motion.div 
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0, rotate: 4 }}
                  transition={{ duration: 0.5, delay: 0.65 }}
                  className="absolute bottom-[5%] right-[5%] bg-[var(--color-ink)] p-5 text-white max-w-[220px] shadow-lg z-30"
                >
                  <div className="text-[10px] font-semibold opacity-70 mb-2 tracking-widest uppercase">Meme</div>
                  <div className="text-[14px] font-medium">"bro didn't even make it past the ATS"</div>
                </motion.div>
                
              </motion.div>
            )}
          </div>
        </div>
      </section>

      {/* 2. THE PROBLEM */}
      <section className="py-24 px-6 sm:px-12 bg-white border-y border-[var(--color-border)]">
        <div className="mx-auto max-w-[1200px]">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            
            <motion.div 
              initial="initial"
              whileInView="whileInView"
              viewport={{ once: true, margin: "-100px" }}
              variants={{ whileInView: { transition: { staggerChildren: 0.1 } } }}
              className="max-w-[480px]"
            >
              <motion.h2 variants={FADE_UP} className="font-display text-4xl md:text-6xl text-[var(--color-ink)] leading-[1.05]">
                You know your product.<br />
                <span className="text-[var(--color-muted)]">You don't always know the angle.</span>
              </motion.h2>
            </motion.div>

            <motion.div 
              initial="initial"
              whileInView="whileInView"
              viewport={{ once: true, margin: "-100px" }}
              variants={{ whileInView: { transition: { staggerChildren: 0.15 } } }}
              className="bg-[#FAF9F5] border border-[var(--color-border)] rounded-[var(--radius-lg)] p-8 md:p-10 flex flex-col md:flex-row items-center gap-10"
            >
              <motion.div variants={FADE_UP} className="space-y-4 text-[13px] text-[var(--color-ink)] min-w-[160px]">
                <div><span className="font-mono text-[10px] uppercase text-[var(--color-muted)] mr-2">Product</span> Resume builder</div>
                <div><span className="font-mono text-[10px] uppercase text-[var(--color-muted)] mr-2">Audience</span> College students</div>
                <div><span className="font-mono text-[10px] uppercase text-[var(--color-muted)] mr-2">Platform</span> Instagram</div>
                <div><span className="font-mono text-[10px] uppercase text-[var(--color-muted)] mr-2">Tone</span> Relatable</div>
              </motion.div>

              <motion.div variants={FADE_UP} className="text-[var(--color-muted)] text-[24px]">
                →
              </motion.div>

              <motion.div variants={FADE_UP} className="bg-white p-6 border border-[var(--color-border)] shadow-sm">
                <div className="text-[10px] font-semibold text-[var(--color-accent)] mb-2 tracking-widest uppercase">KAIROS Finds</div>
                <div className="text-[11px] font-mono text-[var(--color-muted)] mb-1 uppercase">Hook</div>
                <div className="text-[18px] font-display text-[var(--color-ink)] leading-tight">
                  "POV: HR rejected your resume before opening it."
                </div>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* 3. TRANSFORMATION */}
      <section className="py-24 px-6 sm:px-12">
        <div className="mx-auto max-w-[1200px]">
          <motion.div 
            initial="initial"
            whileInView="whileInView"
            viewport={{ once: true, margin: "-100px" }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center"
          >
            <motion.div variants={FADE_UP} className="space-y-3 font-mono text-[13px] tracking-wider text-[var(--color-muted)]">
              <div className="text-[10px] uppercase font-sans font-semibold tracking-widest mb-4">Inputs</div>
              <div className="p-4 border border-[var(--color-border)] bg-white flex justify-between"><span>PRODUCT</span></div>
              <div className="p-4 border border-[var(--color-border)] bg-white flex justify-between"><span>AUDIENCE</span></div>
              <div className="p-4 border border-[var(--color-border)] bg-white flex justify-between"><span>PLATFORM</span></div>
              <div className="p-4 border border-[var(--color-border)] bg-white flex justify-between"><span>TONE</span></div>
            </motion.div>
            
            <motion.div variants={FADE_UP} className="flex justify-center text-[var(--color-ink)] text-4xl font-light">
              <span className="hidden md:block">→</span>
              <span className="block md:hidden">↓</span>
            </motion.div>
            
            <motion.div variants={{
              initial: {},
              whileInView: { transition: { staggerChildren: 0.1 } }
            }} className="space-y-3">
              <div className="text-[10px] uppercase font-sans font-semibold tracking-widest text-[var(--color-accent)] mb-4">Outputs</div>
              <motion.div variants={FADE_UP} className="p-4 border-l-2 border-[var(--color-ink)] bg-white font-display text-[22px] text-[var(--color-ink)] shadow-sm">HOOK</motion.div>
              <motion.div variants={FADE_UP} className="p-4 border-l-2 border-[var(--color-ink)] bg-white font-display text-[22px] text-[var(--color-ink)] shadow-sm">MEME</motion.div>
              <motion.div variants={FADE_UP} className="p-4 border-l-2 border-[var(--color-ink)] bg-white font-display text-[22px] text-[var(--color-ink)] shadow-sm">DIALOGUE</motion.div>
              <motion.div variants={FADE_UP} className="p-4 border-l-2 border-[var(--color-ink)] bg-white font-display text-[22px] text-[var(--color-ink)] shadow-sm">REEL</motion.div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* 4. PERSONALIZATION */}
      <section className="py-24 px-6 sm:px-12 bg-[#FAF9F5] border-y border-[var(--color-border)]">
        <div className="mx-auto max-w-[1000px]">
          <div className="text-[11px] font-semibold tracking-[0.2em] text-[var(--color-muted)] uppercase mb-16">Learns your instincts</div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-16">
            <motion.div 
              initial="initial"
              whileInView="whileInView"
              viewport={{ once: true, margin: "-100px" }}
              variants={{ whileInView: { transition: { staggerChildren: 0.15 } } }}
              className="space-y-12"
            >
              <motion.div variants={FADE_UP} className="space-y-2">
                <div className="text-[11px] font-mono text-[var(--color-muted)] uppercase">You</div>
                <div className="text-[24px] font-display text-[var(--color-ink)]">"Make it funnier."</div>
              </motion.div>

              <motion.div 
                variants={FADE_UP} 
                className="space-y-2 pl-6 border-l-2 border-[var(--color-accent)]"
              >
                <div className="text-[11px] font-mono text-[var(--color-accent)] uppercase">Kairos</div>
                <div className="text-[24px] font-display text-[var(--color-muted)] italic">
                  "Got it.<br />I'll lean more sarcastic next time."
                </div>
              </motion.div>
            </motion.div>

            <motion.div 
              initial="initial"
              whileInView="whileInView"
              viewport={{ once: true, margin: "-100px" }}
              variants={FADE_UP}
              className="bg-white border border-[var(--color-border)] rounded-[var(--radius-lg)] p-8 shadow-sm flex flex-col justify-center"
            >
              <div className="text-[10px] uppercase tracking-widest text-[var(--color-ink)] font-semibold mb-6">Your Style</div>
              <div className="flex flex-wrap gap-2 mb-6">
                <span className="px-3 py-1.5 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-full text-[13px] text-[var(--color-ink)]">Sarcastic</span>
                <span className="px-3 py-1.5 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-full text-[13px] text-[var(--color-ink)]">Relatable</span>
                <span className="px-3 py-1.5 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-full text-[13px] text-[var(--color-ink)]">Hinglish</span>
                <span className="px-3 py-1.5 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-full text-[13px] text-[var(--color-ink)]">Short-form</span>
              </div>
              <p className="text-[14px] text-[var(--color-muted)] leading-relaxed">
                Every piece of feedback helps KAIROS understand how you like to communicate.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* 5. MEMES + CULTURE */}
      <section className="py-24 px-6 sm:px-12 bg-[var(--color-ink)] text-white overflow-hidden">
        <div className="mx-auto max-w-[1200px]">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            
            <motion.div 
              initial="initial"
              whileInView="whileInView"
              viewport={{ once: true, margin: "-100px" }}
              variants={{ whileInView: { transition: { staggerChildren: 0.15 } } }}
              className="max-w-[480px]"
            >
              <motion.h2 variants={FADE_UP} className="font-display text-4xl md:text-5xl mb-6 text-white">
                Fluent in internet culture.
              </motion.h2>
              <motion.p variants={FADE_UP} className="text-[16px] text-gray-400 leading-relaxed">
                KAIROS doesn't just write copy. It pairs your product with culturally relevant formats, searches the exact meme structure, and writes the dialogue to match.
              </motion.p>
            </motion.div>

            <motion.div 
              initial="initial"
              whileInView="whileInView"
              viewport={{ once: true, margin: "-100px" }}
              variants={{ whileInView: { transition: { staggerChildren: 0.1 } } }}
              className="relative w-full max-w-[500px] mx-auto"
            >
              <div className="bg-[#1f1f1f] p-8 border border-white/10 rounded-[var(--radius-lg)] shadow-2xl relative">
                
                <motion.div variants={FADE_UP} className="mb-6 pb-6 border-b border-white/10 flex justify-between items-center">
                  <div>
                    <div className="text-[10px] text-gray-500 uppercase tracking-widest mb-1">Meme Format</div>
                    <div className="text-[15px] font-medium">POV</div>
                  </div>
                  <div className="text-right">
                    <div className="text-[10px] text-gray-500 uppercase tracking-widest mb-1">Search</div>
                    <div className="text-[15px] text-[#D94F2B] font-mono bg-[#D94F2B]/10 px-2 py-1 rounded">"student panic"</div>
                  </div>
                </motion.div>

                <motion.div variants={FADE_UP} className="mb-6">
                  <div className="text-[10px] text-gray-500 uppercase tracking-widest mb-2">Generated Angle</div>
                  <div className="text-[16px] italic text-gray-300">
                    Checking your bank balance after ordering food.
                  </div>
                </motion.div>

                <motion.div variants={FADE_UP}>
                  <div className="text-[10px] text-[#D94F2B] font-semibold uppercase tracking-widest mb-2">Hook</div>
                  <div className="font-display text-[28px] leading-tight text-white">
                    "POV: You said you'd save money this month."
                  </div>
                </motion.div>

              </div>
            </motion.div>

          </div>
        </div>
      </section>

      {/* 6. HOW IT WORKS */}
      <section className="py-24 px-6 sm:px-12 bg-white border-b border-[var(--color-border)]">
        <div className="mx-auto max-w-[1000px]">
          <motion.div 
            initial="initial"
            whileInView="whileInView"
            viewport={{ once: true, margin: "-100px" }}
            variants={{ whileInView: { transition: { staggerChildren: 0.1 } } }}
            className="grid grid-cols-1 md:grid-cols-3 gap-12"
          >
            <motion.div variants={FADE_UP} className="space-y-3">
              <div className="font-mono text-[12px] text-[var(--color-muted)] border-b border-[var(--color-border)] pb-2 mb-4">01</div>
              <div className="text-[11px] uppercase tracking-widest font-semibold text-[var(--color-ink)]">Tell KAIROS</div>
              <div className="text-[14px] text-[var(--color-muted)] leading-relaxed">Product + audience + context</div>
            </motion.div>
            <motion.div variants={FADE_UP} className="space-y-3">
              <div className="font-mono text-[12px] text-[var(--color-muted)] border-b border-[var(--color-border)] pb-2 mb-4">02</div>
              <div className="text-[11px] uppercase tracking-widest font-semibold text-[var(--color-ink)]">Choose the voice</div>
              <div className="text-[14px] text-[var(--color-muted)] leading-relaxed">Platform + tone + direction</div>
            </motion.div>
            <motion.div variants={FADE_UP} className="space-y-3">
              <div className="font-mono text-[12px] text-[var(--color-muted)] border-b border-[var(--color-border)] pb-2 mb-4">03</div>
              <div className="text-[11px] uppercase tracking-widest font-semibold text-[var(--color-ink)]">Find the angle</div>
              <div className="text-[14px] text-[var(--color-muted)] leading-relaxed">Hooks + memes + dialogue + reels</div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* 7. FINAL CTA */}
      <section className="py-24 px-6 sm:px-12 text-center bg-[#FAF9F5] flex flex-col items-center justify-center min-h-[50vh] max-h-[600px]">
        <motion.div 
          initial="initial"
          whileInView="whileInView"
          viewport={{ once: true, margin: "-100px" }}
          variants={{ whileInView: { transition: { staggerChildren: 0.1 } } }}
          className="max-w-[600px]"
        >
          <motion.h2 variants={FADE_UP} className="font-display text-5xl md:text-6xl text-[var(--color-ink)] mb-4">
            Your product already has a story.
          </motion.h2>
          <motion.p variants={FADE_UP} className="text-[18px] text-[var(--color-muted)] mb-10">
            You just haven't found the angle yet.
          </motion.p>
          
          <motion.div variants={FADE_UP}>
            <Link 
              href="/create"
              className="group inline-flex items-center gap-3 rounded-[var(--radius-md)] bg-[var(--color-ink)] text-[var(--color-bg)] px-10 py-5 text-[16px] font-medium hover:bg-black transition-all active:scale-[0.98] shadow-sm"
            >
              <span>Find my angle</span>
              <motion.span 
                className="block"
                transition={{ type: "spring", stiffness: 400, damping: 25 }}
                whileHover={{ x: 5 }}
              >
                →
              </motion.span>
            </Link>
          </motion.div>
        </motion.div>
      </section>
      
    </div>
  );
}
