"use client";

import React, { useEffect, useState } from 'react';
import Link from 'next/link';

interface RecentItem {
  id: number;
  product_id: number;
  hook: string;
  tone: string;
  platform: string;
  created_at: string;
}

interface RecentResponse {
  items: RecentItem[];
  total: number;
}

export default function RecentScreen() {
  const [data, setData] = useState<RecentItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/recent')
      .then(res => res.json())
      .then((json: RecentResponse) => {
        setData(json.items || []);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch recent", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="mx-auto max-w-[880px] px-6 py-16 sm:px-12 pb-32 animate-in fade-in duration-500">
      <div className="mb-16">
        <h1 className="font-display text-5xl md:text-7xl tracking-tighter text-[var(--color-ink)] mb-4">
          Recent
        </h1>
        <p className="text-lg text-[var(--color-muted)] max-w-[45ch] leading-relaxed">
          Your previous angles and generations.
        </p>
      </div>
      
      {loading ? (
        <div className="py-24 text-center">
          <div className="w-1.5 h-1.5 rounded-full bg-[var(--color-ink)] animate-[pulse_2s_ease-in-out_infinite] mx-auto" />
        </div>
      ) : data.length === 0 ? (
        <div className="py-24 text-center border border-[var(--color-border)] rounded-[var(--radius-lg)]">
          <p className="text-[14px] text-[var(--color-muted)] mb-4">
            Nothing here yet.<br/>Your generated angles will appear here.
          </p>
          <Link href="/create" className="text-[13px] font-medium text-[var(--color-ink)] hover:text-[var(--color-accent)] transition-colors">
            Create a brief →
          </Link>
        </div>
      ) : (
        <ul className="space-y-6">
          {data.map((item) => (
            <li key={item.id} className="p-8 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-[var(--radius-md)] flex flex-col gap-4">
              <div className="flex flex-wrap items-center gap-2 text-[11px] font-semibold uppercase tracking-[0.15em] text-[var(--color-muted)]">
                <span>{item.platform}</span>
                <span>·</span>
                <span>{item.tone}</span>
                <span className="ml-auto text-[var(--color-muted)]/70">
                  {new Date(item.created_at).toLocaleDateString()}
                </span>
              </div>
              <div className="font-display text-2xl text-[var(--color-ink)] leading-tight">
                {item.hook}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
