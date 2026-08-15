import React from 'react';

export default function PreferencesScreen() {
  return (
    <div className="mx-auto max-w-[880px] px-6 py-16 sm:px-12 pb-32 animate-in fade-in duration-500">
      <div className="mb-16">
        <h1 className="font-display text-5xl md:text-7xl tracking-tighter text-[var(--color-ink)] mb-4">
          Preferences
        </h1>
        <p className="text-lg text-[var(--color-muted)] max-w-[45ch] leading-relaxed">
          Your creative preferences will appear here as KAIROS learns from your feedback.
        </p>
      </div>
      
      <div className="py-24 text-center border border-[var(--color-border)] rounded-[var(--radius-lg)]">
        <p className="text-[14px] text-[var(--color-muted)]">
          No preferences learned yet.
        </p>
      </div>
    </div>
  );
}
