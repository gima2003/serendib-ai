import { useState } from "react";
import {
  Sparkles,
  ArrowRight,
  Calendar,
  CalendarDays,
  Building2,
  UtensilsCrossed,
  Umbrella,
  Calculator,
  Plane,
  FileText,
  Lightbulb,
  MapPin,
  Compass,
  Utensils,
  Heart,
  CheckCircle2,
} from "lucide-react";

/* ================================================================== */
/*  SERENDIB AI — shared data & building blocks                        */
/*  Used by Home.jsx and by SerendibNavbar.jsx (and therefore by every  */
/*  page that mounts the navbar, such as the user dashboard). Keeping   */
/*  this in one file means the navbar looks and behaves identically     */
/*  everywhere it's used.                                               */
/* ================================================================== */

/* ------------------------------------------------------------------ */
/*  Images — Wikimedia Commons (Creative Commons)                      */
/* ------------------------------------------------------------------ */

export const wiki = (file, w = 1200) =>
  `https://commons.wikimedia.org/wiki/Special:FilePath/${file}•?width=${w}`;

export const IMG = {
  sigiriya: "The_Sigiriya_Fortress.jpg",
  sigiriyaRock: "Sigiriya_Rock_fortress.jpg",
  ellaBridge: "Nine_Arches_Bridge_in_Ella.jpg",
  ellaBridge2: "Nine_Arches_Bridge.jpg",
  train: "Train_ride_thru_Sri_Lanka_Upcountry_tea_garden.JPG",
  mirissa: "20160130_Sri_Lanka_4279+82_4_Mirissa_sRGB_(25144418393).jpg",
  mirissaSecret: "Secret_beach_-_Mirissa_Sri_Lanka.jpg",
  tea: "Sri_Lanka,_Tea_plantations,_Nuwara_Eliya.jpg",
  elephants: "Elephants_playing_in_the_Yala_National_Park.jpg",
  leopard: "Srilankan_leopard_(panthera_pardus_kotiya)_shot_in_Yala_National_Park.jpg",
  galle: "SL_Galle_Fort_asv2020-01_img24.jpg",
  galleDutch: "Dutch_Galle_Fort,_Sri_Lanka.jpg",
  tooth: "SL_Kandy_asv2020-01_img33_Sacred_Tooth_Temple.jpg",
  toothAlt: "Zahntempel_Kandy.jpg",
  arugam: "Arugam_bay_beach.jpg",
  horton: "SL_Horton_Plains_NP_asv2020-01_img16.jpg",
  anuradhapura: "035_Ruwanweliseya_Stupa,_Anuradhapura,_Sri_Lanka.jpg",
  nilaveli: "Nillaveli_Beach.JPG",
  colombo: "Beautiful_Sunrise_over_the_Colombo_Skyline_as_seen_from_the_ocean.jpg",
  food: "Sri_Lankan_Rice_and_Curry.jpg",
  dance:
    "Kandyan_dance_performance_at_Kandyan_Cultural_Centre,_Sangaraja_Mawatha,_Kandy,_Sri_Lanka,_20260131_1727_7649.jpg",
};

/* ------------------------------------------------------------------ */
/*  Sri Lanka clock + upcoming festivals (placeholder dates — replace  */
/*  with your events API / CMS later). Used by Home's hero ticker and  */
/*  by the dashboard's Calendar quick-access overlay.                  */
/* ------------------------------------------------------------------ */

export const fmtTime = new Intl.DateTimeFormat("en-US", {
  hour: "numeric",
  minute: "2-digit",
  timeZone: "Asia/Colombo",
});
export const fmtDate = new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
  year: "numeric",
  timeZone: "Asia/Colombo",
});
export const fmtDateLong = new Intl.DateTimeFormat("en-US", {
  weekday: "long",
  month: "long",
  day: "numeric",
  timeZone: "Asia/Colombo",
});

export const UPCOMING_EVENTS = [
  { name: "Deepavali — Festival of Lights", short: "Deepavali", date: "2026-11-08", label: "Nov 8" },
  { name: "Christmas Day", short: "Christmas", date: "2026-12-25", label: "Dec 25" },
  { name: "Sinhala & Tamil New Year", short: "Sinhala & Tamil New Year", date: "2027-04-14", label: "Apr 14" },
];

export const daysUntil = (iso, now) => Math.ceil((new Date(`${iso}T00:00:00+05:30`) - now) / 86400000);

export function upcomingEvents(now) {
  return UPCOMING_EVENTS.map((e) => ({ ...e, days: daysUntil(e.date, now) }))
    .filter((e) => e.days >= 0)
    .sort((a, b) => a.days - b.days);
}

/* ------------------------------------------------------------------ */
/*  Languages (cosmetic selector — wire up real i18n later)            */
/* ------------------------------------------------------------------ */

export const LANGUAGES = [
  { code: "EN", label: "English" },
  { code: "SI", label: "••••• (Sinhala)" },
  { code: "TA", label: "••••• (Tamil)" },
];

/* ------------------------------------------------------------------ */
/*  Navigation content — every `to` is a placeholder route             */
/* ------------------------------------------------------------------ */

export const THINGS = [
  { title: "Culture & Heritage", desc: "Ancient temples, forts and royal cities", img: IMG.sigiriyaRock, to: "/things-to-do/culture-heritage" },
  { title: "Adventure", desc: "Surfing, hiking, white-water rafting", img: IMG.arugam, to: "/things-to-do/adventure" },
  { title: "Relaxation", desc: "Pristine beaches and Ayurveda spas", img: IMG.mirissaSecret, to: "/things-to-do/relaxation" },
  { title: "Food & Dining", desc: "Spice trails and street food tours", img: IMG.food, to: "/things-to-do/food-dining" },
];

export const EXPLORE_ITEMS = [
  { title: "Destinations", icon: MapPin, to: "/explore/destinations" },
  { title: "Attractions", icon: Compass, to: "/explore/attractions" },
  { title: "Experiences", icon: Sparkles, to: "/explore/experiences" },
  { title: "Food", icon: Utensils, to: "/explore/food" },
  { title: "Accommodation", icon: Building2, to: "/explore/accommodation" },
];

export const REGIONS = [
  { title: "Cultural Triangle", tag: "Sigiriya, Dambulla and the ancient capitals", img: IMG.sigiriya, to: "/where-to-go/cultural-triangle" },
  { title: "Hill Country", tag: "Tea estates, waterfalls and misty peaks", img: IMG.tea, to: "/where-to-go/hill-country" },
  { title: "North & North Central", tag: "Sacred stupas and northern culture", img: IMG.anuradhapura, to: "/where-to-go/north" },
  { title: "Western Province", tag: "Colombo and the west coast", img: IMG.colombo, to: "/where-to-go/western-province" },
  { title: "Southern Coast", tag: "Beaches, whales and Galle Fort", img: IMG.mirissa, to: "/where-to-go/southern-coast" },
  { title: "East Coast", tag: "Turquoise bays and surf breaks", img: IMG.nilaveli, to: "/where-to-go/east-coast" },
  { title: "Safari Zone", tag: "Leopards and elephants in the wild", img: IMG.leopard, to: "/where-to-go/safari-zone" },
];

export const CITY_GUIDES = [
  { title: "Colombo", img: IMG.colombo, to: "/cities/colombo" },
  { title: "Kandy", img: IMG.toothAlt, to: "/cities/kandy" },
  { title: "Galle", img: IMG.galleDutch, to: "/cities/galle" },
  { title: "Ella", img: IMG.ellaBridge2, to: "/cities/ella" },
];

export const EVENTS = [
  { title: "Kandy Esala Perahera", date: "Jul – Aug", img: IMG.tooth, to: "/events/esala-perahera" },
  { title: "Vesak Festival", date: "May", img: IMG.anuradhapura, to: "/events/vesak" },
  { title: "Sinhala & Tamil New Year", date: "Apr 13–14", img: IMG.food, to: "/events/new-year" },
  { title: "Deepavali", date: "Oct – Nov", img: IMG.colombo, to: "/events/deepavali" },
];

export const BLOG_POSTS = [
  { title: "The Perfect 10-Day Sri Lanka Route", category: "Itineraries", img: IMG.sigiriya, to: "/blog/10-day-route" },
  { title: "Kandy to Ella: The Scenic Train Guide", category: "Transport", img: IMG.train, to: "/blog/kandy-ella-train" },
  { title: "A Beginner's Guide to Rice & Curry", category: "Food", img: IMG.food, to: "/blog/rice-and-curry" },
  { title: "When to Go: Sri Lanka's Two Monsoons", category: "Travel Tips", img: IMG.mirissa, to: "/blog/best-time-to-visit" },
];
export const BLOG_CATEGORIES = ["Itineraries", "Food", "Culture", "Adventure", "Travel Tips", "AI Insights"];

export const PLAN_ITEMS = [
  { title: "Hotels", desc: "Find the perfect stay", icon: Building2, to: "/plan/hotels" },
  { title: "Restaurants", desc: "Best dining across Sri Lanka", icon: UtensilsCrossed, to: "/plan/restaurants" },
  { title: "Resorts", desc: "Boutique stays & beach resorts", icon: Umbrella, to: "/plan/resorts" },
  { title: "Itinerary Builder", desc: "Build your custom trip", icon: CalendarDays, to: "/plan-trip" },
  { title: "Trip Cost Estimator", desc: "Budget your Sri Lanka trip", icon: Calculator, to: "/plan/trip-cost" },
  { title: "Getting Here", desc: "Flights and entry info", icon: Plane, to: "/plan/getting-here" },
  { title: "Visa Information", desc: "ETA guide & requirements", icon: FileText, to: "/plan/visa" },
  { title: "Travel Tips", desc: "Essentials for your visit", icon: Lightbulb, to: "/plan/travel-tips" },
];

export const MY_TRIPS_ITEMS = [
  { title: "Upcoming", desc: "Trips you're about to take", icon: CalendarDays, to: "/my-trips/upcoming" },
  { title: "Saved", desc: "Ideas and itineraries you've bookmarked", icon: Heart, to: "/my-trips/saved" },
  { title: "Completed", desc: "Journeys you've already finished", icon: CheckCircle2, to: "/my-trips/completed" },
];

export const QUICK_CITIES = ["Colombo", "Hill Country", "South Coast", "Jaffna"];

/* ------------------------------------------------------------------ */
/*  Small shared components                                            */
/* ------------------------------------------------------------------ */

/* Placeholder link. Swap the <a> for react-router's <Link to={to}> once routes exist. */
export function NavAnchor({ to = "#", className = "", children, ...rest }) {
  return (
    <a href={to} onClick={(e) => e.preventDefault()} className={className} {...rest}>
      {children}
    </a>
  );
}

/* Image with a graceful gradient fallback if the remote file fails */
export function SmartImg({ src, alt, className = "", eager = false, style }) {
  const [failed, setFailed] = useState(false);
  if (failed) {
    return (
      <div
        role="img"
        aria-label={alt}
        className={`${className} bg-gradient-to-br from-emerald-900 via-emerald-800 to-orange-900`}
        style={style}
      />
    );
  }
  return (
    <img
      src={src}
      alt={alt}
      loading={eager ? "eager" : "lazy"}
      onError={() => setFailed(true)}
      className={className}
      style={style}
    />
  );
}

/* ------------------------------------------------------------------ */
/*  Mega-menu panels (shown on hover / focus under each top-level item) */
/* ------------------------------------------------------------------ */

export const PanelLabel = ({ children }) => (
  <p className="mb-3 text-[11px] font-semibold uppercase tracking-[0.18em] text-stone-400">{children}</p>
);

export function PanelFooter({ label, to = "#" }) {
  return (
    <div className="mt-5 border-t border-stone-100 pt-4">
      <NavAnchor
        to={to}
        className="group inline-flex items-center gap-2 text-[13px] font-bold uppercase tracking-wider text-emerald-900 transition-colors hover:text-orange-600"
      >
        {label}
        <ArrowRight size={15} className="transition-transform duration-300 group-hover:translate-x-1" />
      </NavAnchor>
    </div>
  );
}

export function ThingsPanel() {
  return (
    <>
      <PanelLabel>Discover</PanelLabel>
      <div className="grid grid-cols-2 gap-x-3 gap-y-1">
        {THINGS.map((t) => (
          <NavAnchor
            key={t.title}
            to={t.to}
            className="group flex items-center gap-4 rounded-xl p-2.5 transition-colors hover:bg-orange-50"
          >
            <span className="h-[68px] w-[68px] shrink-0 overflow-hidden rounded-xl">
              <SmartImg
                src={wiki(t.img, 300)}
                alt={t.title}
                className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
              />
            </span>
            <span>
              <span className="block text-[15px] font-semibold text-stone-900 transition-colors group-hover:text-orange-600">
                {t.title}
              </span>
              <span className="mt-0.5 block text-[13px] leading-snug text-stone-500">{t.desc}</span>
            </span>
          </NavAnchor>
        ))}
      </div>

      <div className="my-4 h-px bg-stone-100" />
      <PanelLabel>Explore</PanelLabel>
      <div className="flex flex-wrap gap-2">
        {EXPLORE_ITEMS.map((e) => {
          const Icon = e.icon;
          return (
            <NavAnchor
              key={e.title}
              to={e.to}
              className="group flex items-center gap-2 rounded-full border border-stone-200 py-1.5 pl-2 pr-3.5 text-[13.5px] font-medium text-stone-800 transition-colors hover:border-orange-300 hover:bg-orange-50"
            >
              <span className="grid h-6 w-6 shrink-0 place-items-center rounded-full bg-orange-50 text-orange-500 transition-colors group-hover:bg-orange-500 group-hover:text-white">
                <Icon size={13} />
              </span>
              {e.title}
            </NavAnchor>
          );
        })}
      </div>

      <div className="my-4 h-px bg-stone-100" />
      <PanelLabel>Legends & Heritage</PanelLabel>
      <NavAnchor
        to="/things-to-do/ravana-trail"
        className="group relative flex h-24 items-end overflow-hidden rounded-xl"
      >
        <SmartImg
          src={wiki(IMG.ellaBridge, 800)}
          alt="Ravana's Lanka Trail"
          className="absolute inset-0 h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
        />
        <span className="absolute inset-0 bg-gradient-to-r from-black/75 via-black/40 to-transparent" />
        <span className="relative p-4 text-white">
          <span className="block text-[15px] font-semibold">Ravana's Lanka Trail</span>
          <span className="block text-[13px] text-white/80">Walk the mythological sites of the Ramayana</span>
        </span>
      </NavAnchor>
      <PanelFooter label="View all experiences" to="/things-to-do" />
    </>
  );
}

export function WherePanel() {
  const [hover, setHover] = useState(REGIONS[0]);
  return (
    <div className="grid grid-cols-[1fr_270px] gap-6">
      <div>
        <PanelLabel>Regions</PanelLabel>
        <div className="grid grid-cols-2 gap-x-2 gap-y-0.5">
          {REGIONS.map((r) => (
            <NavAnchor
              key={r.title}
              to={r.to}
              onMouseEnter={() => setHover(r)}
              onFocus={() => setHover(r)}
              className="group flex items-center gap-3 rounded-xl p-2 transition-colors hover:bg-orange-50"
            >
              <span className="h-11 w-11 shrink-0 overflow-hidden rounded-lg">
                <SmartImg
                  src={wiki(r.img, 200)}
                  alt=""
                  className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
              </span>
              <span className="text-[14.5px] font-medium leading-tight text-stone-900 transition-colors group-hover:text-orange-600">
                {r.title}
              </span>
            </NavAnchor>
          ))}
        </div>

        <div className="my-4 h-px bg-stone-100" />
        <PanelLabel>City guides</PanelLabel>
        <div className="flex flex-wrap gap-2">
          {CITY_GUIDES.map((c) => (
            <NavAnchor
              key={c.title}
              to={c.to}
              className="group flex items-center gap-2 rounded-full border border-stone-200 py-1 pl-1 pr-3.5 text-[13.5px] font-medium text-stone-800 transition-colors hover:border-orange-300 hover:bg-orange-50"
            >
              <span className="h-7 w-7 overflow-hidden rounded-full">
                <SmartImg src={wiki(c.img, 120)} alt="" className="h-full w-full object-cover" />
              </span>
              {c.title}
            </NavAnchor>
          ))}
        </div>
      </div>

      {/* Live preview of the hovered region */}
      <NavAnchor to={hover.to} className="group relative block min-h-[300px] overflow-hidden rounded-2xl">
        <SmartImg
          key={hover.title}
          src={wiki(hover.img, 700)}
          alt={hover.title}
          className="fade-in absolute inset-0 h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
        />
        <span className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/15 to-transparent" />
        <span key={`${hover.title}-t`} className="fade-in absolute inset-x-0 bottom-0 p-5 text-white">
          <span className="font-display block text-3xl font-semibold leading-none">{hover.title}</span>
          <span className="mt-2 block text-[13px] leading-snug text-white/80">{hover.tag}</span>
        </span>
      </NavAnchor>
    </div>
  );
}

export function EventsPanel() {
  return (
    <>
      <PanelLabel>Festivals & events</PanelLabel>
      <div className="grid grid-cols-2 gap-4">
        {EVENTS.map((e) => (
          <NavAnchor
            key={e.title}
            to={e.to}
            className="group overflow-hidden rounded-2xl border border-stone-200/80 bg-white transition-shadow duration-300 hover:shadow-lg"
          >
            <span className="relative block h-32 overflow-hidden">
              <SmartImg
                src={wiki(e.img, 600)}
                alt={e.title}
                className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-110"
              />
              <span className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
              <span className="absolute bottom-2.5 left-3 inline-flex items-center gap-1 rounded-full bg-white/90 px-2.5 py-1 text-[11px] font-bold text-stone-900">
                <Calendar size={11} className="text-orange-500" />
                {e.date}
              </span>
            </span>
            <span className="block px-4 py-3 text-[14.5px] font-semibold text-stone-900 transition-colors group-hover:text-orange-600">
              {e.title}
            </span>
          </NavAnchor>
        ))}
      </div>
      <PanelFooter label="View all events & festivals" to="/events" />
    </>
  );
}

export function BlogPanel() {
  const [feature, ...rest] = BLOG_POSTS;
  return (
    <>
      <div className="grid grid-cols-[1.1fr_1fr] gap-6">
        <NavAnchor to={feature.to} className="group relative block min-h-[260px] overflow-hidden rounded-2xl">
          <SmartImg
            src={wiki(feature.img, 800)}
            alt={feature.title}
            className="absolute inset-0 h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
          />
          <span className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/20 to-transparent" />
          <span className="absolute inset-x-0 bottom-0 p-5 text-white">
            <span className="mb-2 inline-block rounded-full bg-orange-500 px-2.5 py-0.5 text-[11px] font-semibold">
              Featured · {feature.category}
            </span>
            <span className="font-display block text-[28px] font-semibold leading-[1.05]">{feature.title}</span>
          </span>
        </NavAnchor>

        <div>
          <PanelLabel>Latest stories</PanelLabel>
          <div className="space-y-1">
            {rest.map((p) => (
              <NavAnchor
                key={p.title}
                to={p.to}
                className="group flex items-center gap-3.5 rounded-xl p-2 transition-colors hover:bg-orange-50"
              >
                <span className="h-16 w-20 shrink-0 overflow-hidden rounded-lg">
                  <SmartImg
                    src={wiki(p.img, 300)}
                    alt=""
                    className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
                  />
                </span>
                <span>
                  <span className="block text-[12px] font-semibold text-orange-600">{p.category}</span>
                  <span className="block text-[14px] font-semibold leading-snug text-stone-900">{p.title}</span>
                </span>
              </NavAnchor>
            ))}
          </div>
        </div>
      </div>

      <div className="mt-5 flex flex-wrap items-center justify-between gap-3 border-t border-stone-100 pt-4">
        <div className="flex flex-wrap gap-2">
          {BLOG_CATEGORIES.map((c) => (
            <NavAnchor
              key={c}
              to={`/blog/category/${c.toLowerCase().replace(/\s+/g, "-")}`}
              className="rounded-full border border-stone-200 px-3 py-1 text-[12.5px] font-medium text-stone-600 transition-colors hover:border-orange-300 hover:bg-orange-50 hover:text-orange-700"
            >
              {c}
            </NavAnchor>
          ))}
        </div>
        <NavAnchor
          to="/blog"
          className="group inline-flex items-center gap-2 text-[13px] font-bold uppercase tracking-wider text-emerald-900 hover:text-orange-600"
        >
          Read the blog
          <ArrowRight size={15} className="transition-transform duration-300 group-hover:translate-x-1" />
        </NavAnchor>
      </div>
    </>
  );
}

export function PlanPanel() {
  return (
    <div className="grid grid-cols-[1fr_290px] gap-6">
      <div>
        <PanelLabel>Plan</PanelLabel>
        <div className="grid grid-cols-2 gap-x-2 gap-y-0.5">
          {PLAN_ITEMS.map((p) => {
            const Icon = p.icon;
            return (
              <NavAnchor
                key={p.title}
                to={p.to}
                className="group flex items-start gap-3.5 rounded-xl p-3 transition-colors hover:bg-orange-50"
              >
                <span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-orange-50 text-orange-500 transition-all duration-300 group-hover:bg-orange-500 group-hover:text-white">
                  <Icon size={19} />
                </span>
                <span>
                  <span className="block text-[15px] font-semibold text-stone-900 transition-colors group-hover:text-orange-600">
                    {p.title}
                  </span>
                  <span className="mt-0.5 block text-[13px] leading-snug text-stone-500">{p.desc}</span>
                </span>
              </NavAnchor>
            );
          })}
        </div>
      </div>

      {/* Featured: the AI planner */}
      <div className="relative flex min-h-[320px] flex-col justify-end overflow-hidden rounded-2xl p-5 text-white">
        <SmartImg
          src={wiki(IMG.sigiriya, 700)}
          alt="Sigiriya Rock Fortress"
          className="absolute inset-0 h-full w-full object-cover"
        />
        <span className="absolute inset-0 bg-gradient-to-t from-[#0E1512] via-[#0E1512]/60 to-[#0E1512]/10" />
        <div className="relative">
          <span className="inline-flex items-center gap-1.5 rounded-full bg-white/15 px-2.5 py-1 text-[11px] font-semibold backdrop-blur">
            <Sparkles size={12} className="text-orange-300" /> Serendib AI
          </span>
          <p className="font-display mt-3 text-[28px] font-semibold leading-[1.05]">Let the agents plan your trip.</p>
          <p className="mt-2 text-[13px] leading-snug text-white/75">
            Tell us your budget, dates and interests — get a complete day-by-day route.
          </p>
          <NavAnchor
            to="/plan-trip"
            className="btn-shine relative mt-4 inline-flex items-center gap-2 overflow-hidden rounded-full bg-orange-500 px-5 py-2.5 text-[13px] font-semibold text-white transition-colors hover:bg-orange-600"
          >
            Build my itinerary <ArrowRight size={15} />
          </NavAnchor>
        </div>
      </div>
    </div>
  );
}

export function MyTripsPanel() {
  return (
    <>
      <PanelLabel>My Trips</PanelLabel>
      <div className="space-y-1">
        {MY_TRIPS_ITEMS.map((t) => {
          const Icon = t.icon;
          return (
            <NavAnchor
              key={t.title}
              to={t.to}
              className="group flex items-center gap-3.5 rounded-xl p-3 transition-colors hover:bg-orange-50"
            >
              <span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-orange-50 text-orange-500 transition-all duration-300 group-hover:bg-orange-500 group-hover:text-white">
                <Icon size={18} />
              </span>
              <span>
                <span className="block text-[15px] font-semibold text-stone-900 transition-colors group-hover:text-orange-600">
                  {t.title}
                </span>
                <span className="mt-0.5 block text-[13px] leading-snug text-stone-500">{t.desc}</span>
              </span>
            </NavAnchor>
          );
        })}
      </div>
      <PanelFooter label="View all my trips" to="/my-trips" />
    </>
  );
}

/* Base menu config. SerendibNavbar appends a "My Trips" entry itself   */
/* when isAuth is true, since that item only makes sense once signed in.*/
export const BASE_MENUS = [
  { key: "things", label: "Things To Do", width: 700, Panel: ThingsPanel, subs: THINGS.map((t) => t.title) },
  { key: "where", label: "Where To Go", width: 860, Panel: WherePanel, subs: REGIONS.map((r) => r.title) },
  { key: "events", label: "Events", width: 700, Panel: EventsPanel, subs: EVENTS.map((e) => e.title) },
  { key: "blog", label: "Blog", width: 780, Panel: BlogPanel, subs: BLOG_POSTS.map((b) => b.title) },
  { key: "plan", label: "Plan Your Trip", width: 900, Panel: PlanPanel, subs: PLAN_ITEMS.map((p) => p.title) },
];

export const TRIPS_MENU = {
  key: "trips",
  label: "My Trips",
  width: 360,
  Panel: MyTripsPanel,
  subs: MY_TRIPS_ITEMS.map((t) => t.title),
};
