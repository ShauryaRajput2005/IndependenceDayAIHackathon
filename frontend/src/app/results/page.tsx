import React from 'react';
import Link from 'next/link';

export default function ResultsFallback() {
  return (
    <div className="mx-auto max-w-[880px] px-6 py-32 sm:px-12 text-center animate-in fade-in duration-500">
      <div className="text-[11px] uppercase tracking-[0.18em] font-semibold text-[var(--color-muted)] mb-8">
        Results
      </div>
      <h1 className="font-display text-4xl md:text-5xl text-[var(--color-ink)] mb-6">
        Results are created from your brief.
      </h1>
      <p className="text-[17px] text-[var(--color-muted)] mb-12">
        Start by creating a brief.
      </p>
      <Link 
        href="/create" 
        className="rounded-[var(--radius-md)] border border-[var(--color-ink)] text-[var(--color-ink)] px-8 py-3 text-[14px] font-medium hover:bg-[var(--color-ink)] hover:text-[var(--color-bg)] transition-all"
      >
        Create a brief →
      </Link>
    </div>
  );
}
