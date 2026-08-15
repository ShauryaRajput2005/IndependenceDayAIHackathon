"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navigation() {
  const pathname = usePathname();
  const isLanding = pathname === '/';

  if (isLanding) return null;

  return (
    <header className="sticky top-0 z-50 w-full border-b border-[color-mix(in_srgb,var(--color-ink)_12%,transparent)] bg-[#efe9de]/95 shadow-[0_1px_0_rgba(23,23,23,0.04)] backdrop-blur-md">
      <div className="flex h-16 w-full items-center justify-between px-6 md:px-12">
        {/* LEFT: BRAND MARK */}
        <div className="flex-1">
          <Link href="/" className="group inline-flex items-center transition-opacity duration-300 hover:opacity-85">
            <img 
              src="/logo.png" 
              alt="KAIROS" 
              className="h-7 w-auto object-contain mix-blend-multiply"
            />
          </Link>
        </div>

        {/* CENTER: PRIMARY NAV */}
        <nav className="flex-1 flex justify-center gap-10">
          {isLanding ? (
            <>
              <a 
                href="#how-it-works" 
                className="text-[15px] font-medium text-[var(--color-muted)] transition-colors duration-300 hover:text-[var(--color-ink)]"
              >
                How it works
              </a>
              <Link 
                href="/create" 
                className="text-[15px] font-medium text-[var(--color-ink)] transition-colors duration-300 hover:text-[var(--color-accent)]"
              >
                Create
              </Link>
            </>
          ) : (
            <>
              <Link 
                href="/create" 
                className={`text-[15px] font-medium transition-colors duration-300 ${pathname === '/create' ? 'text-[var(--color-ink)] underline decoration-[var(--color-accent)] decoration-2 underline-offset-[10px]' : 'text-[var(--color-muted)] hover:text-[var(--color-ink)]'}`}
              >
                Create
              </Link>
              <Link 
                href="/recent" 
                className={`text-[15px] font-medium transition-colors duration-300 ${pathname === '/recent' ? 'text-[var(--color-ink)] underline decoration-[var(--color-accent)] decoration-2 underline-offset-[10px]' : 'text-[var(--color-muted)] hover:text-[var(--color-ink)]'}`}
              >
                Recent
              </Link>
            </>
          )}
        </nav>

        {/* RIGHT: PREFERENCES */}
        <div className="flex-1 flex justify-end">
          {!isLanding && (
            <Link 
              href="/preferences" 
              className={`text-[15px] font-medium transition-colors duration-300 ${pathname === '/preferences' ? 'text-[var(--color-ink)] underline decoration-[var(--color-accent)] decoration-2 underline-offset-[10px]' : 'text-[var(--color-muted)] hover:text-[var(--color-ink)]'}`}
            >
              Preferences
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
