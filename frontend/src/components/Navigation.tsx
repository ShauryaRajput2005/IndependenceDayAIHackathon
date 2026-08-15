import Link from 'next/link';

export default function Navigation() {
  return (
    <header className="w-full border-b border-[#D9D5CC]">
      <div className="mx-auto max-w-7xl px-6 sm:px-12 h-24 flex items-center justify-between">
        {/* LEFT: BRAND MARK */}
        <div className="flex-1">
          <Link href="/" className="font-display text-4xl tracking-tighter text-[#171717] hover:text-[#D94F2B] transition-colors duration-300">
            KAIROS
          </Link>
        </div>

        {/* CENTER: PRIMARY NAV */}
        <nav className="flex-1 flex justify-center gap-10">
          <Link 
            href="/" 
            className="text-[15px] font-medium text-[#171717] hover:text-[#D94F2B] transition-colors duration-300"
          >
            Create
          </Link>
          <Link 
            href="/recent" 
            className="text-[15px] font-medium text-[#69665F] hover:text-[#171717] transition-colors duration-300"
          >
            Recent
          </Link>
        </nav>

        {/* RIGHT: PREFERENCES */}
        <div className="flex-1 flex justify-end">
          <Link 
            href="/preferences" 
            className="text-[15px] font-medium text-[#69665F] hover:text-[#171717] transition-colors duration-300"
          >
            Preferences
          </Link>
        </div>
      </div>
    </header>
  );
}
