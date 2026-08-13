import { useState, useEffect, useRef, useCallback } from "react";
import { Link } from "react-router-dom";
import {
  Sparkles,
  ShieldCheck,
  Utensils,
  Route,

  Brain,
  CloudSun,
  Navigation,
  Clock,
  Wallet,
  ArrowRight,
  Menu,
  X,
  Compass,
  ArrowDown,
  Info,
  MapPin,
} from "lucide-react";

/* ------------------------------------------------------------------ */
/*  Static content                                                     */
/* ------------------------------------------------------------------ */

const destinations = [
  {
    name: "Sigiriya",
    category: "Culture & Heritage",
    image:
      "https://loremflickr.com/800/600/sigiriya,rock/all?lock=10",
  },
  {
    name: "Ella",
    category: "Mountains & Nature",
    image:
      "https://loremflickr.com/800/600/ella,bridge,srilanka/all?lock=11",
  },
  {
    name: "Mirissa",
    category: "Beaches",
    image:
      "https://loremflickr.com/800/600/mirissa,beach,srilanka/all?lock=12",
  },
  {
    name: "Kandy",
    category: "Culture & Heritage",
    image:
      "https://loremflickr.com/800/600/kandy,temple,srilanka/all?lock=13",
  },
  {
    name: "Yala",
    category: "Wildlife",
    image:
      "https://loremflickr.com/800/600/yala,leopard,srilanka/all?lock=14",
  },
  {
    name: "Galle",
    category: "Adventure",
    image:
      "https://loremflickr.com/800/600/galle,fort,srilanka/all?lock=15",
  },
];

const agents = [
  { icon: Brain, title: "Traveler Intelligence", description: "Understands preferences, interests, budget and travel style." },
  { icon: Compass, title: "Destination Discovery", description: "Finds Sri Lankan places suited to the traveler." },
  { icon: Utensils, title: "Local Food Intelligence", description: "Recommends authentic dishes, restaurants and local food experiences." },
  { icon: Route, title: "Smart Trip Planning", description: "Combines all recommendations into a complete itinerary." },
  { icon: Navigation, title: "Route Optimization", description: "Organizes destinations to reduce unnecessary travel and improve trip flow." },
  { icon: CloudSun, title: "Weather & Context", description: "Uses current conditions and travel context when creating or re-planning trips." },
  { icon: Wallet, title: "Budget Intelligence", description: "Estimates spending across accommodation, food, transport, attractions and activities." },
  { icon: ShieldCheck, title: "Safety-Aware Planning", description: "Considers trusted travel information without inventing critical safety data." },
];

/* ------------------------------------------------------------------ */
/*  Reveal — small scroll-reveal wrapper (no extra dependency)         */
/* ------------------------------------------------------------------ */

function Reveal({ children, className = "", delay = 0 }) {
  const ref = useRef(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.15 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      className={`${className} transition-all duration-700 ease-out motion-reduce:transition-none ${visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
        }`}
      style={{ transitionDelay: visible ? `${delay}ms` : "0ms" }}
    >
      {children}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Home                                                                */
/* ------------------------------------------------------------------ */

function Home() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [heroLoaded, setHeroLoaded] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handleVideoReady = useCallback(() => setHeroLoaded(true), []);

  return (
    <div className="min-h-screen w-full bg-[#FFFCF8] text-[#1C1917] font-sans antialiased overflow-x-hidden">
      <style>{`
        @keyframes gentlePulse { 0%, 100% { opacity: .55; transform: scale(1); } 50% { opacity: 1; transform: scale(1.12); } }
        .pulse-dot { animation: gentlePulse 2.4s ease-in-out infinite; }
        @keyframes scrollHint { 0%, 100% { transform: translateY(0); opacity: .6; } 50% { transform: translateY(6px); opacity: 1; } }
        .scroll-hint { animation: scrollHint 2s ease-in-out infinite; }
        @media (prefers-reduced-motion: reduce) {
          .pulse-dot, .scroll-hint { animation: none; }
        }
      `}</style>

      {/* ============================================================ */}
      {/* 1. NAVIGATION BAR                                              */}
      {/* ============================================================ */}
      <nav
        className={`fixed top-0 z-50 w-full transition-all duration-300 ${scrolled
          ? "bg-white/80 backdrop-blur-md border-b border-[#EAE2D6] py-3 shadow-[0_1px_0_rgba(0,0,0,0.02)]"
          : "bg-transparent py-6 border-b border-transparent"
          }`}
      >
        <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-6 md:px-10">
          <div className="flex items-center gap-12">
            <a
              href="#top"
              className={`text-xl font-bold tracking-tight flex items-center gap-2 transition-colors ${scrolled ? "text-[#1C1917]" : "text-white"
                }`}
            >
              <Sparkles className="text-orange-500" size={22} />
              Serendib <span className="text-orange-500">AI</span>
            </a>

            <div
              className={`hidden lg:flex items-center gap-8 text-sm font-medium transition-colors ${scrolled ? "text-[#57534E]" : "text-white/85"
                }`}
            >
              <a href="#top" className={`transition-colors hover:text-orange-500 ${scrolled ? "text-[#1C1917]" : "text-white"}`}>Home</a>
              <a href="#explore" className="transition-colors hover:text-orange-500">Explore</a>
              <a href="#how-it-works" className="transition-colors hover:text-orange-500">How It Works</a>
              <a href="#features" className="transition-colors hover:text-orange-500">Features</a>
            </div>
          </div>

          <div className="hidden lg:flex items-center gap-3">
            <Link
              to="/login"
              className={`px-5 py-2.5 rounded-full text-sm font-semibold border transition-colors ${scrolled
                ? "border-[#EAE2D6] text-[#1C1917] hover:bg-[#FBF3EA]"
                : "border-white/30 text-white hover:bg-white/10"
                }`}
            >
              Login
            </Link>
            <Link to="/register" className="rounded-full bg-orange-500 px-6 py-2.5 text-sm font-semibold text-white shadow-md shadow-orange-500/20 hover:bg-orange-600 transition-colors">
              Register
            </Link>
          </div>

          <button
            className={`lg:hidden ${scrolled ? "text-[#1C1917]" : "text-white"}`}
            onClick={() => setMobileMenuOpen((v) => !v)}
            aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
            aria-expanded={mobileMenuOpen}
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {mobileMenuOpen && (
          <div className="lg:hidden absolute top-full left-0 w-full bg-white/95 backdrop-blur-lg border-b border-[#EAE2D6] py-4 px-6 flex flex-col gap-4 shadow-xl">
            <a href="#top" className="text-[#1C1917] text-lg font-medium">Home</a>
            <a href="#explore" className="text-[#57534E] text-lg font-medium">Explore</a>
            <a href="#how-it-works" className="text-[#57534E] text-lg font-medium">How It Works</a>
            <a href="#features" className="text-[#57534E] text-lg font-medium">Features</a>
            <div className="w-full h-px bg-[#EAE2D6] my-2" />
            <Link to="/login" className="w-full text-left text-[#57534E] text-lg font-medium">Login</Link>
            <Link to="/register" className="w-full rounded-full bg-orange-500 px-6 py-3 text-center text-lg font-semibold text-white">
              Register
            </Link>
          </div>
        )}
      </nav>

      {/* ============================================================ */}
      {/* 2 & 3 & 4. CINEMATIC VIDEO HERO + CONTENT + SCROLL INDICATOR  */}
      {/* ============================================================ */}
      <section id="top" className="relative w-full h-screen min-h-[640px] overflow-hidden">
        {/* Full-screen background video */}
        <video
          autoPlay
          muted
          loop
          playsInline
          preload="auto"
          onCanPlay={handleVideoReady}
          aria-hidden="true"
          className={`absolute inset-0 h-full w-full object-cover transition-opacity duration-1000 ${heroLoaded ? "opacity-100" : "opacity-0"
            }`}
        >
          <source src="/videos/Serendib-AI.mp4.mp4" type="video/mp4" />
        </video>

        {/* Fallback base so the hero never shows a blank/broken frame while the video loads */}
        <div className="absolute inset-0 bg-gradient-to-br from-[#3a2a1a] to-[#1c1512] -z-10" />

        {/* Readability overlay: subtle dark gradient + vignette, not too dark */}
        <div className="absolute inset-0 bg-gradient-to-b from-black/55 via-black/30 to-black/60" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_35%,rgba(0,0,0,0.35)_100%)]" />
        {/* Soft transition into the next (light) section */}
        <div className="absolute bottom-0 left-0 w-full h-40 bg-gradient-to-t from-[#FFFCF8] to-transparent" />

        {/* Hero content */}
        <div className="relative z-10 flex h-full w-full flex-col items-center justify-center px-6 text-center">
          <Reveal delay={0}>
            <div className="flex items-center gap-2 rounded-full border border-white/25 bg-white/10 px-4 py-1.5 text-xs font-medium tracking-wide backdrop-blur-md mb-8 text-white/90">
              <span className="h-1.5 w-1.5 rounded-full bg-orange-400 pulse-dot" />
              AI-Powered Sri Lankan Travel Intelligence
            </div>
          </Reveal>

          <Reveal delay={120}>
            <h1 className="max-w-4xl text-5xl font-bold leading-[1.08] tracking-tight text-white md:text-6xl lg:text-7xl">
              Discover Sri Lanka. <br />
              <span className="text-orange-400">Planned Around You.</span>
            </h1>
          </Reveal>

          <Reveal delay={240}>
            <p className="mt-6 max-w-2xl text-base leading-relaxed text-white/80 md:text-lg">
              Serendib AI brings destinations, local food, smart routes, weather, budgets and travel
              context together to create a journey designed around you.
            </p>
          </Reveal>

          <Reveal delay={360}>
            <div className="mt-10 flex flex-col gap-4 sm:flex-row sm:gap-4">
              <button className="rounded-full bg-orange-500 px-8 py-4 text-base font-semibold text-white shadow-lg shadow-orange-500/30 transition-all hover:bg-orange-600 hover:scale-[1.03]">
                Plan My Trip
              </button>
              <button className="rounded-full border border-white/30 bg-white/10 px-8 py-4 text-base font-semibold text-white backdrop-blur-sm transition-all hover:bg-white/20 flex items-center gap-2 justify-center">
                Explore Serendib AI <ArrowRight size={18} />
              </button>
            </div>
          </Reveal>

          <Reveal delay={480}>
            <div className="mt-10 flex items-center justify-center gap-2 md:gap-3 text-xs md:text-sm font-medium text-white/70 flex-wrap">
              <span>Personalized</span>
              <span className="w-1 h-1 rounded-full bg-white/40" />
              <span>Context-Aware</span>
              <span className="w-1 h-1 rounded-full bg-white/40" />
              <span>Local Intelligence</span>
              <span className="w-1 h-1 rounded-full bg-white/40" />
              <span>AI Powered</span>
            </div>
          </Reveal>
        </div>

        {/* Scroll indicator */}
        <a
          href="#intro"
          className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10 flex flex-col items-center gap-2 text-white/70 hover:text-white transition-colors scroll-hint"
          aria-label="Scroll to explore"
        >
          <span className="text-xs font-medium tracking-[0.2em] uppercase">Explore</span>
          <ArrowDown size={18} />
        </a>
      </section>

      {/* ============================================================ */}
      {/* 5. INTRODUCTION SECTION                                       */}
      {/* ============================================================ */}
      <section id="intro" className="relative w-full px-6 py-24 md:py-32">
        <Reveal className="mx-auto flex max-w-4xl flex-col items-center text-center">
          <span className="mb-4 text-xs font-bold uppercase tracking-[0.3em] text-orange-500">
            Travel, Reimagined
          </span>
          <h2 className="mb-8 text-3xl font-semibold leading-tight md:text-5xl">
            One intelligent platform for your entire Sri Lankan journey.
          </h2>
          <p className="text-lg leading-relaxed text-[#57534E] md:text-xl">
            Travelers usually have to switch between maps, travel blogs, restaurant websites, weather
            apps, reviews, budget calculations, and safety information.{" "}
            <strong className="text-[#1C1917] font-semibold">
              Serendib AI brings these decisions together into one intelligent travel experience.
            </strong>
          </p>
        </Reveal>
      </section>

      {/* ============================================================ */}
      {/* 6. HOW SERENDIB AI WORKS                                      */}
      {/* ============================================================ */}
      <section id="how-it-works" className="w-full bg-[#FBF3EA] px-6 py-24 border-y border-[#EAE2D6]">
        <div className="mx-auto max-w-6xl">
          <Reveal className="mb-16 text-center">
            <h2 className="text-3xl font-semibold md:text-4xl">From an idea to a complete journey</h2>
          </Reveal>

          <div className="relative grid gap-10 md:grid-cols-4">
            <div className="hidden md:block absolute top-8 left-0 w-full h-px bg-gradient-to-r from-transparent via-orange-300 to-transparent -translate-y-1/2 z-0" />

            {[
              { num: "01", title: "Tell Us About Your Trip", desc: "Share your budget, travel dates, interests, travel style, and preferred experiences." },
              { num: "02", title: "AI Understands You", desc: "Serendib AI deeply analyzes your unique traveler preferences and trip requirements." },
              { num: "03", title: "Specialized Agents Collaborate", desc: "Different AI agents work together to research destinations, food, context and travel options." },
              { num: "04", title: "Receive Your Smart Itinerary", desc: "The system produces an optimized, personalized Sri Lankan itinerary designed just for you." },
            ].map((step, idx) => (
              <Reveal key={idx} delay={idx * 100} className="relative z-10 flex flex-col items-center text-center group">
                <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-white border border-[#EAE2D6] text-xl font-bold text-orange-500 shadow-sm transition-transform duration-300 group-hover:scale-105">
                  {step.num}
                </div>
                <h3 className="mb-3 text-lg font-semibold">{step.title}</h3>
                <p className="text-sm leading-relaxed text-[#78716C]">{step.desc}</p>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* ============================================================ */}
      {/* 7. MULTI-AGENT INTELLIGENCE SECTION                           */}
      {/* ============================================================ */}
      <section id="features" className="w-full px-6 py-24 md:py-32">
        <div className="mx-auto max-w-7xl">
          <Reveal className="mb-16 text-center">
            <span className="mb-4 inline-block rounded-full bg-orange-50 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-orange-600 border border-orange-100">
              System Architecture
            </span>
            <h2 className="text-3xl font-semibold md:text-5xl mt-4">
              Multiple AI specialists. <br className="hidden md:block" />One seamless journey.
            </h2>
          </Reveal>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {agents.map((agent, idx) => {
              const Icon = agent.icon;
              return (
                <Reveal key={idx} delay={(idx % 4) * 80}>
                  <div className="group relative h-full overflow-hidden rounded-2xl border border-[#EAE2D6] bg-white/60 backdrop-blur-sm p-8 transition-all duration-300 hover:-translate-y-1.5 hover:border-orange-200 hover:shadow-[0_12px_30px_-14px_rgba(249,115,22,0.35)]">
                    <div className="mb-6 inline-flex h-11 w-11 items-center justify-center rounded-xl bg-orange-50 text-orange-500 transition-transform duration-300 group-hover:-translate-y-0.5 group-hover:scale-105">
                      <Icon size={22} />
                    </div>
                    <h3 className="mb-3 text-lg font-semibold">{agent.title}</h3>
                    <p className="text-sm leading-relaxed text-[#78716C]">{agent.description}</p>
                  </div>
                </Reveal>
              );
            })}
          </div>
        </div>
      </section>

      {/* ============================================================ */}
      {/* 8. AI COLLABORATION VISUAL                                    */}
      {/* ============================================================ */}
      <section className="w-full bg-[#FBF3EA] px-6 py-24 border-y border-[#EAE2D6] overflow-hidden">
        <div className="mx-auto max-w-5xl text-center">
          <Reveal>
            <h2 className="mb-16 text-2xl font-medium text-[#57534E]">How our agents communicate</h2>
          </Reveal>

          <Reveal className="flex flex-col items-center">
            <div className="flex h-16 px-8 items-center justify-center rounded-full border border-[#EAE2D6] bg-white font-medium shadow-sm">
              Traveler
            </div>

            <ArrowDown className="my-4 text-[#D6D3D1]" />

            <div className="relative flex h-20 px-10 items-center justify-center rounded-2xl border border-orange-200 bg-gradient-to-r from-orange-50 to-orange-100/60 text-lg font-bold text-orange-600">
              <span className="absolute -right-1.5 -top-1.5 h-4 w-4 rounded-full bg-orange-400 pulse-dot" />
              Serendib AI
            </div>

            <ArrowDown className="my-4 text-[#D6D3D1]" />

            <div className="flex flex-col md:flex-row gap-4 w-full justify-center">
              {["Profile Intelligence", "Destination Intelligence", "Food Intelligence"].map((agent, i) => (
                <div key={i} className="flex h-14 flex-1 max-w-[220px] items-center justify-center rounded-xl border border-[#EAE2D6] bg-white text-sm font-medium text-[#44403C] mx-auto">
                  {agent}
                </div>
              ))}
            </div>

            <ArrowDown className="my-4 text-[#D6D3D1]" />

            <div className="flex h-16 px-10 items-center justify-center rounded-xl border border-[#EAE2D6] bg-white font-semibold text-orange-600">
              Smart Planner
            </div>

            <ArrowDown className="my-4 text-[#D6D3D1]" />

            <div className="flex flex-wrap items-center justify-center gap-3 text-xs md:text-sm font-medium text-[#78716C] bg-white border border-[#EAE2D6] rounded-full px-6 py-3">
              <span>Route</span>
              <span className="w-1 h-1 rounded-full bg-[#D6D3D1]" />
              <span>Weather</span>
              <span className="w-1 h-1 rounded-full bg-[#D6D3D1]" />
              <span>Budget</span>
              <span className="w-1 h-1 rounded-full bg-[#D6D3D1]" />
              <span>Context</span>
            </div>

            <ArrowDown className="my-4 text-orange-400" />

            <div className="flex h-16 px-12 items-center justify-center rounded-full bg-orange-500 font-bold text-white shadow-md shadow-orange-500/25">
              Personalized Itinerary
            </div>
          </Reveal>
        </div>
      </section>

      {/* ============================================================ */}
      {/* 9. EXPERIENCE SRI LANKA SECTION                               */}
      {/* ============================================================ */}
      <section id="explore" className="w-full px-6 py-24 md:py-32">
        <div className="mx-auto max-w-7xl">
          <Reveal className="mb-12 flex flex-col md:flex-row md:items-end justify-between gap-6">
            <div>
              <h2 className="text-3xl font-semibold md:text-5xl mb-4">
                One island. <br className="hidden md:block" />Endless experiences.
              </h2>
              <p className="max-w-xl text-[#57534E]">
                From ancient heritage to pristine beaches and misty mountains, Sri Lanka offers an
                unmatched diversity of travel experiences.
              </p>
            </div>
            <button className="flex items-center gap-2 text-orange-500 font-medium hover:text-orange-600 transition-colors">
              View all destinations <ArrowRight size={18} />
            </button>
          </Reveal>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {destinations.map((dest, idx) => (
              <Reveal key={idx} delay={(idx % 3) * 100}>
                <div className="group relative h-80 w-full overflow-hidden rounded-2xl cursor-pointer shadow-sm">
                  <img
                    src={dest.image}
                    alt={`${dest.name} — ${dest.category}`}
                    loading="lazy"
                    className="absolute inset-0 h-full w-full object-cover transition-transform duration-700 group-hover:scale-110"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
                  <div className="absolute bottom-0 left-0 p-6">
                    <span className="mb-2 inline-flex items-center gap-1 rounded-full bg-white/20 px-3 py-1 text-xs font-medium backdrop-blur-md text-white">
                      <MapPin size={12} /> {dest.category}
                    </span>
                    <h3 className="text-2xl font-bold text-white">{dest.name}</h3>
                  </div>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* ============================================================ */}
      {/* 10. SMART ITINERARY SHOWCASE                                  */}
      {/* ============================================================ */}
      <section className="w-full bg-[#FBF3EA] px-6 py-24 border-y border-[#EAE2D6]">
        <div className="mx-auto max-w-7xl">
          <div className="grid gap-16 lg:grid-cols-2 lg:items-center">
            <Reveal>
              <h2 className="mb-6 text-3xl font-semibold md:text-5xl">
                A complete journey, intelligently connected.
              </h2>
              <p className="mb-8 text-lg leading-relaxed text-[#57534E]">
                Recommendations are not simply displayed individually. Serendib AI acts as an expert
                travel coordinator, combining destinations, routes, and timing into a perfectly
                optimized, realistic travel plan.
              </p>
              <ul className="space-y-4">
                {[
                  "Day-by-day logical scheduling",
                  "Accurate travel times between locations",
                  "Integrated dining and attraction recommendations",
                  "Real-time weather and budget context",
                ].map((item, i) => (
                  <li key={i} className="flex items-center gap-3 text-[#44403C]">
                    <div className="flex h-6 w-6 items-center justify-center rounded-full bg-orange-50 text-orange-500">
                      <Sparkles size={12} />
                    </div>
                    {item}
                  </li>
                ))}
              </ul>
              <button className="mt-10 rounded-full bg-white px-6 py-3 text-sm font-medium hover:bg-orange-50 transition-colors border border-[#EAE2D6]">
                View Sample Itinerary
              </button>
            </Reveal>

            <Reveal delay={150}>
              <div className="rounded-3xl border border-[#EAE2D6] bg-white p-6 md:p-8 shadow-xl shadow-black/5 relative overflow-hidden">
                <div className="mb-8 border-b border-[#EAE2D6] pb-6">
                  <h3 className="text-xl font-bold">Your Sri Lanka Journey</h3>
                  <div className="mt-2 flex items-center gap-2 text-xs font-medium text-[#78716C] flex-wrap">
                    <span className="bg-[#F5F0E8] px-2 py-1 rounded">6 Days</span>
                    <span className="bg-[#F5F0E8] px-2 py-1 rounded">Nature</span>
                    <span className="bg-[#F5F0E8] px-2 py-1 rounded">Culture</span>
                    <span className="bg-[#F5F0E8] px-2 py-1 rounded">Food</span>
                  </div>
                </div>

                <div className="space-y-7">
                  {/* Day 1 */}
                  <div className="relative pl-6 border-l border-[#EAE2D6]">
                    <div className="absolute -left-1.5 top-1 h-3 w-3 rounded-full border-2 border-white bg-orange-500" />
                    <h4 className="text-sm font-bold text-orange-500">
                      DAY 01 <span className="ml-2 text-[#1C1917] text-base font-semibold">Colombo</span>
                    </h4>
                    <ul className="mt-3 space-y-1.5 text-sm text-[#57534E]">
                      <li>Gangaramaya Temple</li>
                      <li>Pettah Market</li>
                      <li>Galle Face</li>
                    </ul>
                  </div>

                  {/* Day 2 */}
                  <div className="relative pl-6 border-l border-[#EAE2D6]">
                    <div className="absolute -left-1.5 top-1 h-3 w-3 rounded-full border-2 border-white bg-[#D6D3D1]" />
                    <h4 className="text-sm font-bold text-[#78716C]">
                      DAY 02 <span className="ml-2 text-[#1C1917] text-base font-semibold">Colombo → Kandy</span>
                    </h4>
                    <ul className="mt-3 space-y-1.5 text-sm text-[#57534E]">
                      <li>Temple of the Tooth</li>
                      <li>Kandy Lake</li>
                      <li>Local Dining</li>
                    </ul>
                  </div>

                  {/* Day 3 */}
                  <div className="relative pl-6 border-l border-[#EAE2D6]">
                    <div className="absolute -left-1.5 top-1 h-3 w-3 rounded-full border-2 border-white bg-[#D6D3D1]" />
                    <h4 className="text-sm font-bold text-[#78716C]">
                      DAY 03 <span className="ml-2 text-[#1C1917] text-base font-semibold">Kandy → Ella</span>
                    </h4>
                    <ul className="mt-3 space-y-1.5 text-sm text-[#57534E]">
                      <li>Scenic Train Journey</li>
                      <li>Nine Arch Bridge</li>
                      <li>Local Food Experience</li>
                    </ul>
                  </div>
                </div>

                <div className="mt-7 pt-6 border-t border-[#EAE2D6] grid grid-cols-4 gap-3 text-center">
                  <div>
                    <Wallet size={16} className="mx-auto mb-1 text-orange-500" />
                    <p className="text-[11px] text-[#78716C]">Est. Cost</p>
                    <p className="text-xs font-semibold">Rs. 65,000</p>
                  </div>
                  <div>
                    <CloudSun size={16} className="mx-auto mb-1 text-orange-500" />
                    <p className="text-[11px] text-[#78716C]">Weather</p>
                    <p className="text-xs font-semibold">Mild, dry</p>
                  </div>
                  <div>
                    <Clock size={16} className="mx-auto mb-1 text-orange-500" />
                    <p className="text-[11px] text-[#78716C]">Travel Time</p>
                    <p className="text-xs font-semibold">~7h total</p>
                  </div>
                  <div>
                    <Route size={16} className="mx-auto mb-1 text-orange-500" />
                    <p className="text-[11px] text-[#78716C]">Distance</p>
                    <p className="text-xs font-semibold">~190 km</p>
                  </div>
                </div>
              </div>
            </Reveal>
          </div>
        </div>
      </section>

      {/* ============================================================ */}
      {/* 11 & 12. ROUTE INTELLIGENCE + WEATHER/CONTEXT/SAFETY          */}
      {/* ============================================================ */}
      <section className="w-full px-6 py-24 md:py-32">
        <div className="mx-auto max-w-7xl">
          <div className="grid gap-16 lg:grid-cols-2">
            {/* Route Intelligence */}
            <Reveal>
              <h2 className="mb-6 text-3xl font-semibold">
                Less time planning. <br />More time exploring.
              </h2>
              <p className="mb-10 text-[#57534E]">
                The Smart Planner considers location, distance, travel time, opening hours, attraction
                duration, budget, and weather context automatically.
              </p>

              <div className="flex flex-col rounded-2xl border border-[#EAE2D6] bg-[#FBF3EA] p-8">
                {["Kandy", "Dambulla", "Nuwara Eliya", "Ella"].map((place, i, arr) => (
                  <div key={place} className="flex items-start gap-4">
                    <div className="flex flex-col items-center">
                      <div className="flex h-8 w-8 items-center justify-center rounded-full bg-white border border-[#EAE2D6] text-xs font-bold text-orange-500">
                        {i + 1}
                      </div>
                      {i < arr.length - 1 && (
                        <div className="h-12 w-px my-1 border-l-2 border-dashed border-orange-200" />
                      )}
                    </div>
                    <div className="pt-1 pb-4">
                      <h4 className="font-semibold text-lg">{place}</h4>
                      {i < arr.length - 1 && (
                        <p className="text-xs text-[#78716C] mt-1 flex items-center gap-1">
                          <Route size={12} /> Optimized route
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </Reveal>

            {/* Weather, Context & Safety */}
            <Reveal delay={150}>
              <h2 className="mb-6 text-3xl font-semibold">Plans that adapt to the real world.</h2>
              <p className="mb-10 text-[#57534E]">
                Serendib AI uses relevant travel information such as weather, opening hours,
                seasonality, and road context when producing recommendations.
              </p>

              <div className="grid grid-cols-2 gap-4">
                <div className="rounded-xl bg-white border border-[#EAE2D6] p-5">
                  <CloudSun className="text-orange-500 mb-3" size={22} />
                  <h4 className="text-sm font-medium text-[#78716C] mb-1">Weather</h4>
                  <p className="font-semibold text-sm">24°C — Light Rain</p>
                </div>
                <div className="rounded-xl bg-white border border-[#EAE2D6] p-5">
                  <Route className="text-orange-500 mb-3" size={22} />
                  <h4 className="text-sm font-medium text-[#78716C] mb-1">Route</h4>
                  <p className="font-semibold text-sm">Kandy → Ella, 3h 45m</p>
                </div>
                <div className="rounded-xl bg-white border border-[#EAE2D6] p-5">
                  <Info className="text-orange-500 mb-3" size={22} />
                  <h4 className="text-sm font-medium text-[#78716C] mb-1">Context</h4>
                  <p className="font-semibold text-sm">Outdoor activity adjusted</p>
                </div>
                <div className="rounded-xl bg-white border border-[#EAE2D6] p-5">
                  <Wallet className="text-orange-500 mb-3" size={22} />
                  <h4 className="text-sm font-medium text-[#78716C] mb-1">Budget</h4>
                  <p className="font-semibold text-sm">Within planned budget</p>
                </div>
                <div className="rounded-xl bg-white border border-[#EAE2D6] p-5 border-l-2 border-l-orange-500 col-span-2">
                  <ShieldCheck className="text-orange-500 mb-3" size={22} />
                  <h4 className="text-sm font-medium text-[#78716C] mb-1">Safety Information</h4>
                  <p className="font-semibold text-sm">Verified information sources</p>
                </div>
              </div>

              <div className="mt-8 rounded-xl bg-orange-50 border border-orange-100 p-5 text-sm text-orange-900">
                <strong>Responsible AI:</strong> Critical safety information should be supported by
                trusted sources, freshness information and confidence indicators whenever possible.
              </div>
            </Reveal>
          </div>
        </div>
      </section>

      {/* ============================================================ */}
      {/* 13. WHY SERENDIB AI                                           */}
      {/* ============================================================ */}
      <section className="w-full bg-[#FBF3EA] px-6 py-24 border-y border-[#EAE2D6]">
        <div className="mx-auto max-w-7xl">
          <Reveal className="mb-16 text-center">
            <h2 className="text-3xl font-semibold md:text-5xl">Why choose Serendib AI</h2>
          </Reveal>

          <div className="grid gap-x-12 gap-y-10 md:grid-cols-2 lg:grid-cols-3">
            {[
              { title: "Personalized", desc: "Every journey is based on the traveler's interests and constraints." },
              { title: "Locally Relevant", desc: "Designed specifically around authentic Sri Lankan travel." },
              { title: "Context Aware", desc: "Recommendations can respond to changing trip conditions." },
              { title: "Budget Conscious", desc: "Travel costs are actively considered during planning." },
              { title: "Explainable", desc: "Understand exactly why important recommendations were made." },
              { title: "Responsible", desc: "Critical information relies on trusted sources instead of AI guesses." },
            ].map((benefit, idx) => (
              <Reveal key={idx} delay={(idx % 3) * 100} className="flex gap-4">
                <div className="mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-orange-50 text-orange-500">
                  <div className="h-2 w-2 rounded-full bg-orange-500" />
                </div>
                <div>
                  <h3 className="mb-2 text-lg font-semibold">{benefit.title}</h3>
                  <p className="text-sm leading-relaxed text-[#78716C]">{benefit.desc}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* ============================================================ */}
      {/* 14. FINAL CALL TO ACTION                                      */}
      {/* ============================================================ */}
      <section className="relative w-full px-6 py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-[#FFFCF8] to-[#FBF3EA]" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-4xl h-[420px] bg-orange-200/25 blur-[120px] rounded-full" />

        <Reveal className="relative z-10 mx-auto flex max-w-3xl flex-col items-center text-center">
          <h2 className="mb-6 text-4xl font-bold md:text-6xl">Your Sri Lankan story starts here.</h2>
          <p className="mb-10 text-lg md:text-xl text-[#57534E]">
            Tell Serendib AI what you love, and let intelligent agents help shape the journey.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
            <button className="rounded-full bg-orange-500 px-8 py-4 text-base font-semibold text-white shadow-lg shadow-orange-500/25 transition-all hover:bg-orange-600 hover:scale-[1.03]">
              Start Planning
            </button>
            <Link to="/register" className="rounded-full flex items-center justify-center border border-[#EAE2D6] bg-white px-8 py-4 text-base font-semibold text-[#1C1917] transition-all hover:bg-orange-50">
              Create Account
            </Link>
          </div>
        </Reveal>
      </section>

      {/* ============================================================ */}
      {/* 15. FOOTER                                                    */}
      {/* ============================================================ */}
      <footer className="w-full border-t border-[#EAE2D6] bg-[#FFFCF8] pt-16 pb-8">
        <div className="mx-auto max-w-7xl px-6 md:px-10">
          <div className="grid gap-10 md:grid-cols-4 mb-16">
            <div className="md:col-span-1">
              <span className="text-xl font-bold tracking-tight flex items-center gap-2 mb-4">
                <Sparkles className="text-orange-500" size={20} />
                Serendib <span className="text-orange-500">AI</span>
              </span>
              <p className="text-sm text-[#78716C] leading-relaxed">
                Intelligent travel planning for discovering Sri Lanka your way.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-4 text-[#1C1917]">Product</h4>
              <ul className="space-y-3 text-sm text-[#78716C]">
                <li><a href="#" className="hover:text-orange-500 transition-colors">Plan a Trip</a></li>
                <li><a href="#explore" className="hover:text-orange-500 transition-colors">Destinations</a></li>
                <li><a href="#" className="hover:text-orange-500 transition-colors">Experiences</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4 text-[#1C1917]">Platform</h4>
              <ul className="space-y-3 text-sm text-[#78716C]">
                <li><a href="#how-it-works" className="hover:text-orange-500 transition-colors">How It Works</a></li>
                <li><a href="#features" className="hover:text-orange-500 transition-colors">AI Agents</a></li>
                <li><a href="#" className="hover:text-orange-500 transition-colors">Responsible AI</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4 text-[#1C1917]">Company</h4>
              <ul className="space-y-3 text-sm text-[#78716C]">
                <li><a href="#" className="hover:text-orange-500 transition-colors">About</a></li>
                <li><a href="#" className="hover:text-orange-500 transition-colors">Contact</a></li>
              </ul>
            </div>
          </div>

          <div className="flex flex-col md:flex-row items-center justify-between border-t border-[#EAE2D6] pt-8 text-xs text-[#78716C] gap-4 text-center md:text-left">
            <p>© 2026 Serendib AI. All rights reserved.</p>
            <p>Built for intelligent travel across Sri Lanka.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default Home;