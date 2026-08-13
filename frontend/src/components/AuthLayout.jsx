import { Link } from "react-router-dom";
import { Sparkles } from "lucide-react";

export default function AuthLayout({ children, title, subtitle }) {
  return (
    <div className="min-h-screen w-full bg-[#FFFCF8] text-[#1C1917] font-sans antialiased flex flex-col relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(249,115,22,0.05)_0%,transparent_70%)] pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-4xl h-[420px] bg-orange-200/30 blur-[120px] rounded-full pointer-events-none" />
      
      {/* Subtle animated orbs */}
      <div className="absolute top-[20%] left-[20%] w-64 h-64 bg-orange-300/10 rounded-full blur-3xl animate-pulse pointer-events-none" style={{ animationDuration: '4s' }} />
      <div className="absolute bottom-[20%] right-[20%] w-80 h-80 bg-orange-400/10 rounded-full blur-3xl animate-pulse pointer-events-none" style={{ animationDuration: '6s', animationDelay: '1s' }} />

      {/* Header */}
      <header className="w-full p-6 md:p-10 flex justify-center relative z-10">
        <Link to="/" className="flex flex-col items-center gap-1 group">
          <div className="flex items-center gap-2 text-2xl font-bold tracking-tight text-[#1C1917] group-hover:opacity-90 transition-opacity">
            <Sparkles className="text-orange-500" size={24} />
            Serendib <span className="text-orange-500">AI</span>
          </div>
          <span className="text-xs font-medium tracking-[0.15em] text-[#78716C] uppercase">
            Intelligent travel planning for Sri Lanka
          </span>
        </Link>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center p-6 relative z-10">
        <div className="w-full max-w-md animate-in fade-in slide-in-from-bottom-4 duration-700 ease-out">
          
          <div className="mb-8 text-center">
            <h1 className="text-3xl font-bold tracking-tight text-[#1C1917] mb-2">{title}</h1>
            <p className="text-[#57534E] text-sm">{subtitle}</p>
          </div>

          <div className="rounded-3xl border border-[#EAE2D6] bg-white/70 backdrop-blur-xl p-8 shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
            {children}
          </div>

        </div>
      </main>
    </div>
  );
}
