"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navigation() {
  const pathname = usePathname();
  const isLanding = pathname === '/';

  if (isLanding) return null;

  return (
    <header className="w-full border-b border-[var(--color-border)] bg-white/80 backdrop-blur-md sticky top-0 z-50">
      <div className="w-full px-6 md:px-12 h-16 flex items-center justify-between">
        {/* LEFT: BRAND MARK */}
        <div className="flex-1">
          <Link href="/" className="flex items-center group">
            <img 
              src="/logo.png" 
              alt="KAIROS" 
              className="max-h-8 w-auto object-contain transition-opacity duration-300 group-hover:opacity-80 mix-blend-multiply"
            />
          </Link>
        </div>

        {/* CENTER: PRIMARY NAV */}
        <nav className="flex-1 flex justify-center gap-10">
          {isLanding ? (
            <>
              <a 
                href="#how-it-works" 
                className="text-[15px] font-medium text-[var(--color-muted)] hover:text-[var(--color-ink)] transition-colors duration-300"
              >
                How it works
              </a>
              <Link 
                href="/create" 
                className="text-[15px] font-medium text-[var(--color-ink)] hover:text-[var(--color-accent)] transition-colors duration-300"
              >
                Create
              </Link>
            </>
          ) : (
            <>
              <Link 
                href="/create" 
                className={`text-[15px] font-medium transition-colors duration-300 ${pathname === '/create' ? 'text-[var(--color-ink)]' : 'text-[var(--color-muted)] hover:text-[var(--color-ink)]'}`}
              >
                Create
              </Link>
              <Link 
                href="/recent" 
                className={`text-[15px] font-medium transition-colors duration-300 ${pathname === '/recent' ? 'text-[var(--color-ink)]' : 'text-[var(--color-muted)] hover:text-[var(--color-ink)]'}`}
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
              className={`text-[15px] font-medium transition-colors duration-300 ${pathname === '/preferences' ? 'text-[var(--color-ink)]' : 'text-[var(--color-muted)] hover:text-[var(--color-ink)]'}`}
            >
              Preferences
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
