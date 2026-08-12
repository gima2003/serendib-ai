import {
  Search,
  SlidersHorizontal,
  MapPin,
  Heart,
  CalendarDays,
  Users,
  Sparkles,
  ShieldCheck,
  Utensils,
  Route,
  Bell,
} from "lucide-react";

const destinations = [
  {
    name: "Ella",
    price: "From LKR 18,500",
    duration: "3 days",
    image:
      "https://images.unsplash.com/photo-1586613835343-7e5fc70b1f07?auto=format&fit=crop&w=900&q=80",
  },
  {
    name: "Sigiriya",
    price: "From LKR 12,000",
    duration: "2 days",
    image:
      "https://images.unsplash.com/photo-1588258524675-c6192e3325c3?auto=format&fit=crop&w=900&q=80",
  },
  {
    name: "Mirissa",
    price: "From LKR 22,000",
    duration: "3 days",
    image:
      "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80",
  },
  {
    name: "Kandy",
    price: "From LKR 15,500",
    duration: "2 days",
    image:
      "https://images.unsplash.com/photo-1546708973-b339540b5162?auto=format&fit=crop&w=900&q=80",
  },
];

const agents = [
  {
    icon: Sparkles,
    title: "Destination Intelligence",
    description:
      "Find attractions, hidden destinations, events and local experiences.",
  },
  {
    icon: Utensils,
    title: "Local Food Intelligence",
    description:
      "Discover restaurants and authentic Sri Lankan food matching your preferences.",
  },
  {
    icon: ShieldCheck,
    title: "Safety Intelligence",
    description:
      "Check weather, advisories, emergency services and travel risks.",
  },
  {
    icon: Route,
    title: "Smart Itinerary & Budget",
    description:
      "Generate routes, daily plans, estimated costs and optimized schedules.",
  },
];

function Home() {
  return (
    <div className="min-h-screen w-full bg-[#0b0b0c] text-white">
      {/* NAVBAR */}
      <header className="w-full border-b border-white/10 bg-[#0b0b0c]">
        <div className="flex w-full items-center justify-between px-6 py-5 md:px-10 xl:px-16">
          <div className="flex items-center gap-10">
            <span className="text-xl font-bold tracking-wide">
              SERENDIB <span className="text-orange-500">AI</span>
            </span>

            <nav className="hidden gap-7 text-sm text-zinc-400 md:flex">
              <a href="#" className="text-white">
                Home
              </a>
              <a href="#" className="transition hover:text-white">
                Explore
              </a>
              <a href="#" className="transition hover:text-white">
                My Trips
              </a>
              <a href="#" className="transition hover:text-white">
                AI Planner
              </a>
            </nav>
          </div>

          <div className="flex items-center gap-4">
            <button className="rounded-full border border-white/10 p-2.5 text-zinc-300 transition hover:bg-white/5">
              <Bell size={18} />
            </button>

            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-full bg-gradient-to-br from-orange-400 to-orange-700" />

              <div className="hidden sm:block">
                <p className="text-sm font-medium">Traveler</p>
                <p className="text-xs text-zinc-500">Explorer</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* MAIN */}
      <main className="w-full px-6 py-10 md:px-10 xl:px-16">
        {/* HERO */}
        <section className="mb-10 grid w-full gap-10 lg:grid-cols-[1fr_650px] lg:items-end">
          <div>
            <div className="mb-5 h-1 w-12 bg-orange-500" />

            <h1 className="max-w-3xl text-5xl font-semibold leading-[1.03] tracking-tight md:text-6xl xl:text-7xl">
              PLAN YOUR
              <br />
              NEXT{" "}
              <span className="text-orange-500">SRI LANKAN</span>
              <br />
              JOURNEY
            </h1>

            <p className="mt-6 max-w-2xl text-sm leading-7 text-zinc-400 md:text-base">
              Discover Sri Lanka with intelligent travel agents that understand
              destinations, food, safety, budget and your personal travel style.
            </p>
          </div>

          {/* SEARCH */}
          <div className="flex w-full items-center rounded-2xl border border-white/10 bg-[#181819] px-5 py-5 shadow-lg shadow-black/20">
            <Search size={21} className="text-zinc-500" />

            <input
              type="text"
              placeholder="Where do you want to go?"
              className="flex-1 bg-transparent px-4 text-sm text-white outline-none placeholder:text-zinc-600"
            />

            <button className="rounded-lg p-2 text-zinc-400 transition hover:bg-white/5">
              <SlidersHorizontal size={20} />
            </button>
          </div>
        </section>

        {/* MAIN CONTENT GRID */}
        <section className="grid w-full gap-6 xl:grid-cols-[380px_minmax(0,1fr)_420px]">
          {/* RECOMMENDED */}
          <div className="rounded-2xl border border-white/10 bg-[#121214] p-5">
            <div className="mb-5">
              <h2 className="text-xl font-semibold">Recommended</h2>
              <p className="mt-1 text-xs text-zinc-500">
                Handpicked destinations around Sri Lanka.
              </p>
            </div>

            <div className="mb-5 flex flex-wrap gap-2">
              {["All", "Culture", "Nature", "Beach"].map((item, index) => (
                <button
                  key={item}
                  className={`rounded-full px-4 py-2 text-xs transition ${
                    index === 0
                      ? "bg-orange-500 text-white"
                      : "bg-[#202023] text-zinc-400 hover:text-white"
                  }`}
                >
                  {item}
                </button>
              ))}
            </div>

            <div className="grid grid-cols-2 gap-3">
              {destinations.map((destination) => (
                <article
                  key={destination.name}
                  className="overflow-hidden rounded-xl border border-white/10 bg-[#1a1a1d] transition hover:-translate-y-1 hover:border-orange-500/30"
                >
                  <img
                    src={destination.image}
                    alt={destination.name}
                    className="h-40 w-full object-cover"
                  />

                  <div className="p-3">
                    <h3 className="font-medium">{destination.name}</h3>
                    <p className="mt-1 text-[11px] text-zinc-500">
                      {destination.price}
                    </p>
                    <p className="text-[11px] text-zinc-600">
                      {destination.duration}
                    </p>
                  </div>
                </article>
              ))}
            </div>
          </div>

          {/* CENTER COLUMN */}
          <div className="space-y-6">
            <div className="overflow-hidden rounded-2xl border border-white/10 bg-[#151517]">
              <div className="p-6">
                <div className="flex items-start justify-between gap-6">
                  <div>
                    <p className="text-xl font-semibold">Escape to Ella</p>

                    <div className="mt-3 flex flex-wrap gap-2">
                      <span className="rounded-full bg-yellow-500/10 px-3 py-1 text-xs text-yellow-400">
                        ★ 4.9
                      </span>

                      <span className="rounded-full bg-white/5 px-3 py-1 text-xs text-zinc-400">
                        Best Seller
                      </span>
                    </div>
                  </div>

                  <div className="text-right">
                    <p className="text-2xl font-semibold">LKR 32,500</p>
                    <p className="text-xs text-zinc-500">4 days</p>
                  </div>
                </div>

                <p className="mt-5 text-sm leading-7 text-zinc-400">
                  Explore misty mountains, tea estates, Nine Arch Bridge,
                  waterfalls and unforgettable train journeys.
                </p>
              </div>

              <div className="grid grid-cols-3 gap-3 px-6 pb-6">
                {destinations.slice(0, 3).map((item) => (
                  <img
                    key={item.name}
                    src={item.image}
                    alt={item.name}
                    className="h-44 w-full rounded-xl object-cover"
                  />
                ))}
              </div>
            </div>

            {/* AI CTA */}
            <div className="rounded-2xl border border-orange-500/20 bg-gradient-to-r from-orange-500/10 via-orange-500/5 to-transparent p-7">
              <div className="flex items-start justify-between gap-6">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] text-orange-500">
                    Serendib Intelligence
                  </p>

                  <h3 className="mt-3 text-2xl font-semibold">
                    Let our AI agents plan it for you.
                  </h3>

                  <p className="mt-3 max-w-2xl text-sm leading-7 text-zinc-400">
                    Tell us your dates, budget, interests and preferences.
                    Serendib AI coordinates specialized agents to build your
                    complete journey.
                  </p>
                </div>

                <Sparkles className="shrink-0 text-orange-500" size={32} />
              </div>

              <button className="mt-6 rounded-full bg-orange-500 px-6 py-3 text-sm font-semibold transition hover:bg-orange-400">
                Plan with AI
              </button>
            </div>
          </div>

          {/* FEATURED EXPERIENCE */}
          <div className="overflow-hidden rounded-2xl border border-white/10 bg-[#151517]">
            <div className="relative">
              <img
                src="https://images.unsplash.com/photo-1566296314736-6eaac1ca0cb9?auto=format&fit=crop&w=1200&q=80"
                className="h-96 w-full object-cover"
                alt="Sri Lanka wildlife"
              />

              <button className="absolute right-4 top-4 rounded-full bg-black/50 p-2 backdrop-blur transition hover:bg-black/70">
                <Heart size={18} />
              </button>
            </div>

            <div className="p-6">
              <h2 className="text-2xl font-semibold">
                Wildlife Adventure in Yala
              </h2>

              <div className="mt-2 flex items-center gap-2 text-sm text-zinc-400">
                <MapPin size={15} className="text-orange-500" />
                Yala National Park, Sri Lanka
              </div>

              <div className="mt-5 flex flex-wrap gap-2">
                <span className="rounded-full bg-white/5 px-3 py-2 text-xs text-zinc-400">
                  Wildlife
                </span>

                <span className="rounded-full bg-white/5 px-3 py-2 text-xs text-zinc-400">
                  Adventure
                </span>

                <span className="rounded-full bg-orange-500 px-3 py-2 text-xs">
                  Popular
                </span>
              </div>

              <p className="mt-5 text-sm leading-7 text-zinc-400">
                Experience Sri Lanka&apos;s incredible wildlife with an
                AI-planned safari including travel time, safety information,
                weather and nearby dining recommendations.
              </p>

              <div className="mt-5 grid grid-cols-2 gap-3 text-xs">
                <div className="flex items-center gap-2 rounded-xl bg-[#202023] p-3 text-zinc-400">
                  <CalendarDays size={16} />
                  2 days
                </div>

                <div className="flex items-center gap-2 rounded-xl bg-[#202023] p-3 text-zinc-400">
                  <Users size={16} />
                  2 travelers
                </div>
              </div>

              <div className="mt-7 flex items-center justify-between border-t border-white/10 pt-6">
                <div>
                  <p className="text-xs text-zinc-500">Starting from</p>
                  <p className="text-2xl font-semibold">LKR 28,500</p>
                </div>

                <button className="rounded-full bg-orange-500 px-5 py-3 text-sm font-medium transition hover:bg-orange-400">
                  Explore
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* AGENTS SECTION */}
        <section className="py-20">
          <div className="mb-10">
            <p className="text-xs font-semibold uppercase tracking-[0.25em] text-orange-500">
              Powered by specialized intelligence
            </p>

            <h2 className="mt-3 text-3xl font-semibold md:text-4xl">
              Four agents. One unforgettable journey.
            </h2>
          </div>

          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {agents.map(({ icon: Icon, title, description }) => (
              <article
                key={title}
                className="rounded-2xl border border-white/10 bg-[#141416] p-6 transition hover:-translate-y-1 hover:border-orange-500/40"
              >
                <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-orange-500/10 text-orange-500">
                  <Icon size={24} />
                </div>

                <h3 className="font-semibold">{title}</h3>

                <p className="mt-3 text-sm leading-6 text-zinc-500">
                  {description}
                </p>
              </article>
            ))}
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer className="w-full border-t border-white/10 py-8">
        <div className="flex w-full flex-col justify-between gap-4 px-6 text-sm text-zinc-500 md:flex-row md:px-10 xl:px-16">
          <p>© 2026 Serendib AI</p>
          <p>Intelligent journeys through Sri Lanka.</p>
        </div>
      </footer>
    </div>
  );
}

export default Home;