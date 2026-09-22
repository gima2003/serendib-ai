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
  Info,
  MapPin,
  ChevronLeft,
  ChevronRight,
  ChevronDown,
  Search,
  Heart,
  Map as MapIcon,
  Globe,
  LogIn,
  UserPlus,
  Calendar,
  CalendarDays,
  Building2,
  UtensilsCrossed,
  Umbrella,
  Calculator,
  Plane,
  FileText,
  Lightbulb,
  Bus,
  Banknote,
  Droplets,
  Wind,
  Sun,
  Cloud,
  CloudRain,
  CloudLightning,
  CloudFog,
} from "lucide-react";

/* ================================================================== */
/*  SERENDIB AI — HOME PAGE                                            */
/*                                                                     */
/*  Design tokens                                                      */
/*    Ink     #0E1512  deep jungle black-green (hero, ticker, footer)  */
/*    Paper   #FFFCF8  page background                                 */
/*    Sand    #FBF3EA  alternate section background                   */
/*    Line    #EAE2D6  borders                                         */
/*    Saffron orange-500 (#F97316) primary accent / CTA                */
/*  Type: Cormorant Garamond (display) + Inter (interface/body)        */
/* ================================================================== */

const SLIDE_MS = 6000;

/* ------------------------------------------------------------------ */
/*  Images — Wikimedia Commons (Creative Commons). Only the file names */
/*  from your original file are used, so nothing new can 404.          */
/*  Swap any of these for your own hosted images at any time.          */
/* ------------------------------------------------------------------ */

const wiki = (file, w = 1200) =>
  `https://commons.wikimedia.org/wiki/Special:FilePath/${file}?width=${w}`;

const IMG = {
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
/*  Hero slides — each has its own headline, line of copy and the      */
/*  place used for the live weather widget                             */
/* ------------------------------------------------------------------ */

const heroSlides = [
  {
    file: IMG.sigiriya,
    location: "Sigiriya Rock Fortress",
    region: "Cultural Triangle",
    place: "Sigiriya",
    headline: "Rise Above the Ancient Jungle.",
    sub: "Climb the 5th-century rock fortress and step into a kingdom in the sky.",
    alt: "Panoramic view of Sigiriya Rock Fortress rising above the jungle, Sri Lanka",
  },
  {
    file: IMG.ellaBridge,
    location: "Ella — Nine Arch Bridge",
    region: "Hill Country",
    place: "Ella",
    headline: "Where Iron Meets the Mist.",
    sub: "Watch trains cross the Nine Arch Bridge, wrapped in Ella's green hills.",
    alt: "The Nine Arch Bridge viaduct surrounded by lush hills in Ella, Sri Lanka",
  },
  {
    file: IMG.train,
    location: "Kandy–Ella Scenic Train",
    region: "Hill Country",
    place: "Hatton",
    headline: "Ride the Blue Train Through Tea Country.",
    sub: "One of the island's most loved rail journeys, with a plantation view from every window.",
    alt: "Blue train winding through tea plantations in Sri Lanka's hill country",
  },
  {
    file: IMG.mirissa,
    location: "Mirissa Beach",
    region: "Southern Coast",
    place: "Mirissa",
    headline: "Golden Shores, Endless Horizons.",
    sub: "Palm-lined sand and whale-watching waters on the southern coast.",
    alt: "Golden sand and palm-lined coastline at Mirissa Beach, Sri Lanka",
  },
  {
    file: IMG.tea,
    location: "Nuwara Eliya Tea Plantations",
    region: "Hill Country",
    place: "Nuwara Eliya",
    headline: "Journey Through the Tea-Kissed Hills.",
    sub: "Rolling plantations and cool mountain air in the island's Little England.",
    alt: "Rolling green tea plantations in Nuwara Eliya, Sri Lanka",
  },
  {
    file: IMG.elephants,
    location: "Yala National Park",
    region: "Safari Zone",
    place: "Yala",
    headline: "Meet the Wild Side of the Island.",
    sub: "Track leopards, elephants and more across Yala's open grasslands.",
    alt: "Wild elephants in the grasslands of Yala National Park, Sri Lanka",
  },
  {
    file: IMG.galle,
    location: "Galle Fort",
    region: "Southern Coast",
    place: "Galle",
    headline: "Walk the Ramparts of a Living Fort.",
    sub: "Colonial walls, boutique cafés and ocean sunsets in Galle Fort.",
    alt: "The historic Dutch lighthouse and ramparts of Galle Fort, Sri Lanka",
  },
  {
    file: IMG.tooth,
    location: "Kandy — Temple of the Tooth",
    region: "Cultural Triangle",
    place: "Kandy",
    headline: "Sacred Traditions, Alive Today.",
    sub: "Visit the Temple of the Tooth Relic, the spiritual heart of Kandy.",
    alt: "The Sacred Temple of the Tooth Relic in Kandy, Sri Lanka",
  },
  {
    file: IMG.arugam,
    location: "Arugam Bay",
    region: "East Coast",
    place: "Arugam Bay",
    headline: "Catch the Island's Best Waves.",
    sub: "Laid-back surf culture on the sunny east coast.",
    alt: "Surf beach and coastline at Arugam Bay, Sri Lanka",
  },
  {
    file: IMG.horton,
    location: "Horton Plains — World's End",
    region: "Hill Country",
    place: "Horton Plains",
    headline: "Stand at the Edge of the World.",
    sub: "Hike to World's End through misty cloud forest and open grassland.",
    alt: "The sheer cliff drop at World's End, Horton Plains National Park, Sri Lanka",
  },
  {
    file: IMG.anuradhapura,
    location: "Anuradhapura — Ruwanwelisaya",
    region: "North Central",
    place: "Anuradhapura",
    headline: "Wander Through Ancient Kingdoms.",
    sub: "White stupas and 2,000-year-old ruins in the first royal capital.",
    alt: "The ancient white Ruwanwelisaya stupa in Anuradhapura, Sri Lanka",
  },
  {
    file: IMG.nilaveli,
    location: "Trincomalee — Nilaveli Beach",
    region: "East Coast",
    place: "Nilaveli",
    headline: "Find Your Quiet Turquoise Shore.",
    sub: "Calm, clear water and white sand just north of Trincomalee.",
    alt: "Turquoise water and white sand at Nilaveli Beach, Trincomalee, Sri Lanka",
  },
  {
    file: IMG.colombo,
    location: "Colombo Skyline — Lotus Tower",
    region: "Western Province",
    place: "Colombo",
    headline: "Begin in Colombo, a City by the Sea.",
    sub: "Skyline sunrises, street food and heritage in the island's gateway.",
    alt: "Sunrise over the Colombo skyline with the Lotus Tower, Sri Lanka",
  },
  {
    file: IMG.food,
    location: "Traditional Sri Lankan Cuisine",
    region: "Food & Dining",
    place: "Colombo",
    headline: "Taste the Island, One Curry at a Time.",
    sub: "Rice and curry, hoppers and sambols — food that tells the island's story.",
    alt: "A traditional Sri Lankan rice and curry spread",
  },
  {
    file: IMG.dance,
    location: "Kandyan Cultural Performance",
    region: "Culture",
    place: "Kandy",
    headline: "Feel the Rhythm of Kandyan Drums.",
    sub: "Ceremonial costumes and dance traditions passed down for generations.",
    alt: "Traditional Kandyan dancers performing in ceremonial costume, Sri Lanka",
  },
];

/* ------------------------------------------------------------------ */
/*  Live weather — Open-Meteo (free, no API key). Fails silently and   */
/*  the UI shows "--" so the page never breaks.                        */
/* ------------------------------------------------------------------ */

const WEATHER_PLACES = {
  Sigiriya: [7.957, 80.76],
  Ella: [6.8667, 81.0466],
  Hatton: [6.8911, 80.5951],
  Mirissa: [5.9483, 80.4716],
  "Nuwara Eliya": [6.9497, 80.7891],
  Yala: [6.3728, 81.5081],
  Galle: [6.0329, 80.2168],
  Kandy: [7.2906, 80.6337],
  "Arugam Bay": [6.8406, 81.8364],
  "Horton Plains": [6.8025, 80.8032],
  Anuradhapura: [8.3114, 80.4037],
  Nilaveli: [8.6929, 81.1854],
  Colombo: [6.9271, 79.8612],
  Trincomalee: [8.5874, 81.2152],
  Jaffna: [9.6615, 80.0255],
};

function wmo(code) {
  if (code === 0) return { label: "Clear sky", icon: Sun };
  if (code === 1 || code === 2) return { label: "Partly cloudy", icon: CloudSun };
  if (code === 3) return { label: "Overcast", icon: Cloud };
  if (code === 45 || code === 48) return { label: "Foggy", icon: CloudFog };
  if (code >= 51 && code <= 57) return { label: "Drizzle", icon: CloudRain };
  if (code >= 61 && code <= 67) return { label: "Rain", icon: CloudRain };
  if (code >= 80 && code <= 82) return { label: "Rain showers", icon: CloudRain };
  if (code >= 95) return { label: "Thunderstorm", icon: CloudLightning };
  return { label: "Cloudy", icon: Cloud };
}

function useWeather() {
  const [data, setData] = useState({});
  useEffect(() => {
    let cancelled = false;
    const names = Object.keys(WEATHER_PLACES);
    const load = async () => {
      try {
        const lat = names.map((n) => WEATHER_PLACES[n][0]).join(",");
        const lon = names.map((n) => WEATHER_PLACES[n][1]).join(",");
        const url =
          `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}` +
          `&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m` +
          `&timezone=Asia%2FColombo`;
        const res = await fetch(url);
        if (!res.ok) throw new Error("weather unavailable");
        const json = await res.json();
        const list = Array.isArray(json) ? json : [json];
        const next = {};
        list.forEach((row, i) => {
          const c = row.current;
          if (c && names[i]) {
            next[names[i]] = {
              temp: c.temperature_2m,
              feels: c.apparent_temperature,
              humidity: c.relative_humidity_2m,
              wind: c.wind_speed_10m,
              code: c.weather_code,
            };
          }
        });
        if (!cancelled) setData(next);
      } catch {
        /* keep placeholders */
      }
    };
    load();
    const id = setInterval(load, 15 * 60 * 1000);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, []);
  return data;
}

/* ------------------------------------------------------------------ */
/*  Sri Lanka clock + upcoming festivals (placeholder dates — replace  */
/*  with your events API / CMS later)                                  */
/* ------------------------------------------------------------------ */

const fmtTime = new Intl.DateTimeFormat("en-US", {
  hour: "numeric",
  minute: "2-digit",
  timeZone: "Asia/Colombo",
});
const fmtDate = new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
  year: "numeric",
  timeZone: "Asia/Colombo",
});

function useColomboClock() {
  const [now, setNow] = useState(() => new Date());
  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 15000);
    return () => clearInterval(id);
  }, []);
  return now;
}

const UPCOMING_EVENTS = [
  { name: "Deepavali — Festival of Lights", short: "Deepavali", date: "2026-11-08", label: "Nov 8" },
  { name: "Christmas Day", short: "Christmas", date: "2026-12-25", label: "Dec 25" },
  { name: "Sinhala & Tamil New Year", short: "Sinhala & Tamil New Year", date: "2027-04-14", label: "Apr 14" },
];

const daysUntil = (iso, now) =>
  Math.ceil((new Date(`${iso}T00:00:00+05:30`) - now) / 86400000);

function upcomingEvents(now) {
  return UPCOMING_EVENTS.map((e) => ({ ...e, days: daysUntil(e.date, now) }))
    .filter((e) => e.days >= 0)
    .sort((a, b) => a.days - b.days);
}

/* ------------------------------------------------------------------ */
/*  Navigation content                                                 */
/*  Every `to` is a placeholder route — wire them up later.            */
/* ------------------------------------------------------------------ */

const THINGS = [
  { title: "Culture & Heritage", desc: "Ancient temples, forts and royal cities", img: IMG.sigiriyaRock, to: "/things-to-do/culture-heritage" },
  { title: "Adventure", desc: "Surfing, hiking, white-water rafting", img: IMG.arugam, to: "/things-to-do/adventure" },
  { title: "Relaxation", desc: "Pristine beaches and Ayurveda spas", img: IMG.mirissaSecret, to: "/things-to-do/relaxation" },
  { title: "Food & Dining", desc: "Spice trails and street food tours", img: IMG.food, to: "/things-to-do/food-dining" },
];

const REGIONS = [
  { title: "Cultural Triangle", tag: "Sigiriya, Dambulla and the ancient capitals", img: IMG.sigiriya, to: "/where-to-go/cultural-triangle" },
  { title: "Hill Country", tag: "Tea estates, waterfalls and misty peaks", img: IMG.tea, to: "/where-to-go/hill-country" },
  { title: "North & North Central", tag: "Sacred stupas and northern culture", img: IMG.anuradhapura, to: "/where-to-go/north" },
  { title: "Western Province", tag: "Colombo and the west coast", img: IMG.colombo, to: "/where-to-go/western-province" },
  { title: "Southern Coast", tag: "Beaches, whales and Galle Fort", img: IMG.mirissa, to: "/where-to-go/southern-coast" },
  { title: "East Coast", tag: "Turquoise bays and surf breaks", img: IMG.nilaveli, to: "/where-to-go/east-coast" },
  { title: "Safari Zone", tag: "Leopards and elephants in the wild", img: IMG.leopard, to: "/where-to-go/safari-zone" },
];

const CITY_GUIDES = [
  { title: "Colombo", img: IMG.colombo, to: "/cities/colombo" },
  { title: "Kandy", img: IMG.toothAlt, to: "/cities/kandy" },
  { title: "Galle", img: IMG.galleDutch, to: "/cities/galle" },
  { title: "Ella", img: IMG.ellaBridge2, to: "/cities/ella" },
];

const EVENTS = [
  { title: "Kandy Esala Perahera", date: "Jul – Aug", img: IMG.tooth, to: "/events/esala-perahera" },
  { title: "Vesak Festival", date: "May", img: IMG.anuradhapura, to: "/events/vesak" },
  { title: "Sinhala & Tamil New Year", date: "Apr 13–14", img: IMG.food, to: "/events/new-year" },
  { title: "Deepavali", date: "Oct – Nov", img: IMG.colombo, to: "/events/deepavali" },
];

const BLOG_POSTS = [
  { title: "The Perfect 10-Day Sri Lanka Route", category: "Itineraries", img: IMG.sigiriya, to: "/blog/10-day-route" },
  { title: "Kandy to Ella: The Scenic Train Guide", category: "Transport", img: IMG.train, to: "/blog/kandy-ella-train" },
  { title: "A Beginner's Guide to Rice & Curry", category: "Food", img: IMG.food, to: "/blog/rice-and-curry" },
  { title: "When to Go: Sri Lanka's Two Monsoons", category: "Travel Tips", img: IMG.mirissa, to: "/blog/best-time-to-visit" },
];
const BLOG_CATEGORIES = ["Itineraries", "Food", "Culture", "Adventure", "Travel Tips", "AI Insights"];

const PLAN_ITEMS = [
  { title: "Hotels", desc: "Find the perfect stay", icon: Building2, to: "/plan/hotels" },
  { title: "Restaurants", desc: "Best dining across Sri Lanka", icon: UtensilsCrossed, to: "/plan/restaurants" },
  { title: "Resorts", desc: "Boutique stays & beach resorts", icon: Umbrella, to: "/plan/resorts" },
  { title: "Itinerary Builder", desc: "Build your custom trip", icon: CalendarDays, to: "/plan/itinerary-builder" },
  { title: "Trip Cost Estimator", desc: "Budget your Sri Lanka trip", icon: Calculator, to: "/plan/trip-cost" },
  { title: "Getting Here", desc: "Flights and entry info", icon: Plane, to: "/plan/getting-here" },
  { title: "Visa Information", desc: "ETA guide & requirements", icon: FileText, to: "/plan/visa" },
  { title: "Travel Tips", desc: "Essentials for your visit", icon: Lightbulb, to: "/plan/travel-tips" },
];

/* ------------------------------------------------------------------ */
/*  Small shared components                                            */
/* ------------------------------------------------------------------ */

/* Placeholder link. Swap the <a> for <Link to={to}> once routes exist. */
function NavAnchor({ to = "#", className = "", children, ...rest }) {
  return (
    <a href={to} onClick={(e) => e.preventDefault()} className={className} {...rest}>
      {children}
    </a>
  );
}

/* Image with a graceful gradient fallback if the remote file fails */
function SmartImg({ src, alt, className = "", eager = false, style }) {
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

const REVEAL_HIDDEN = {
  up: "opacity-0 translate-y-8",
  left: "opacity-0 -translate-x-8",
  right: "opacity-0 translate-x-8",
  scale: "opacity-0 scale-95",
};

/* Scroll-reveal wrapper (no extra dependency) */
function Reveal({ children, className = "", delay = 0, from = "up" }) {
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
      { threshold: 0.12 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      className={`${className} transition-all duration-[900ms] ease-[cubic-bezier(.22,1,.36,1)] motion-reduce:!transform-none motion-reduce:!opacity-100 motion-reduce:!transition-none ${
        visible ? "opacity-100 translate-x-0 translate-y-0 scale-100" : REVEAL_HIDDEN[from]
      }`}
      style={{ transitionDelay: visible ? `${delay}ms` : "0ms" }}
    >
      {children}
    </div>
  );
}

/* Count-up number that starts when scrolled into view */
function CountUp({ to, suffix = "", duration = 1600 }) {
  const ref = useRef(null);
  const [val, setVal] = useState(0);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    let raf;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        observer.disconnect();
        if (reduce) {
          setVal(to);
          return;
        }
        const start = performance.now();
        const tick = (t) => {
          const p = Math.min((t - start) / duration, 1);
          setVal(Math.round(to * (1 - Math.pow(1 - p, 3))));
          if (p < 1) raf = requestAnimationFrame(tick);
        };
        raf = requestAnimationFrame(tick);
      },
      { threshold: 0.4 }
    );
    observer.observe(el);
    return () => {
      observer.disconnect();
      cancelAnimationFrame(raf);
    };
  }, [to, duration]);

  return (
    <span ref={ref}>
      {val.toLocaleString()}
      {suffix}
    </span>
  );
}

/* ------------------------------------------------------------------ */
/*  Mega-menu panels (shown on hover under each top-level item)        */
/* ------------------------------------------------------------------ */

const PanelLabel = ({ children }) => (
  <p className="mb-3 text-[11px] font-semibold uppercase tracking-[0.18em] text-stone-400">{children}</p>
);

function PanelFooter({ label, to = "#" }) {
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

function ThingsPanel() {
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

function WherePanel() {
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

function EventsPanel() {
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

function BlogPanel() {
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

function PlanPanel() {
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
            to="/plan/itinerary-builder"
            className="btn-shine relative mt-4 inline-flex items-center gap-2 overflow-hidden rounded-full bg-orange-500 px-5 py-2.5 text-[13px] font-semibold text-white transition-colors hover:bg-orange-600"
          >
            Build my itinerary <ArrowRight size={15} />
          </NavAnchor>
        </div>
      </div>
    </div>
  );
}

const MENUS = [
  { key: "things", label: "Things To Do", width: 700, Panel: ThingsPanel, subs: THINGS.map((t) => t.title) },
  { key: "where", label: "Where To Go", width: 860, Panel: WherePanel, subs: REGIONS.map((r) => r.title) },
  { key: "events", label: "Events", width: 700, Panel: EventsPanel, subs: EVENTS.map((e) => e.title) },
  { key: "blog", label: "Blog", width: 780, Panel: BlogPanel, subs: BLOG_POSTS.map((b) => b.title) },
  { key: "plan", label: "Plan Your Trip", width: 900, Panel: PlanPanel, subs: PLAN_ITEMS.map((p) => p.title) },
];

const QUICK_CITIES = ["Colombo", "Hill Country", "South Coast", "Jaffna"];

/* ------------------------------------------------------------------ */
/*  Navbar — utility bar + main bar + hover mega-menu + mobile sheet   */
/* ------------------------------------------------------------------ */

function Navbar({ onSearch }) {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(null); // { key, left, width, caret }
  const [animatePos, setAnimatePos] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [mobileSection, setMobileSection] = useState(null);
  const closeTimer = useRef(null);
  const barRef = useRef(null);

  useEffect(() => {
    const onScroll = () => {
      const y = window.scrollY;
      setScrolled(y > 40);
      const max = document.documentElement.scrollHeight - window.innerHeight;
      if (barRef.current) {
        barRef.current.style.transform = `scaleX(${max > 0 ? Math.min(y / max, 1) : 0})`;
      }
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => () => clearTimeout(closeTimer.current), []);

  const cancelClose = () => clearTimeout(closeTimer.current);
  const scheduleClose = () => {
    clearTimeout(closeTimer.current);
    closeTimer.current = setTimeout(() => setOpen(false), 140);
  };

  const openMenu = (key, el) => {
    cancelClose();
    const cfg = MENUS.find((m) => m.key === key);
    const r = el.getBoundingClientRect();
    const vw = window.innerWidth;
    const width = Math.min(cfg.width, vw - 32);
    const center = r.left + r.width / 2;
    const left = Math.max(16, Math.min(center - width / 2, vw - width - 16));
    setAnimatePos(open); // glide between items, but don't glide in from a stale position
    setActive({ key, left, width, caret: center - left });
    setOpen(true);
  };

  const activeCfg = active ? MENUS.find((m) => m.key === active.key) : null;
  const solid = scrolled || open || mobileOpen;

  const iconBtn = `grid h-10 w-10 place-items-center rounded-full border transition-all duration-300 ${
    solid
      ? "border-stone-200 text-stone-700 hover:border-orange-300 hover:bg-orange-50 hover:text-orange-600"
      : "border-white/30 text-white hover:bg-white/15"
  }`;

  return (
    <>
      {/* Page dimmer while a menu is open */}
      <div
        aria-hidden
        className={`pointer-events-none fixed inset-0 z-40 bg-black/35 backdrop-blur-[2px] transition-opacity duration-300 ${
          open ? "opacity-100" : "opacity-0"
        }`}
      />

      <header
        className={`fixed inset-x-0 top-0 z-50 transition-[background-color,box-shadow] duration-300 ${
          solid
            ? "bg-white/95 shadow-[0_10px_40px_-18px_rgba(14,21,18,0.35)] backdrop-blur-xl"
            : "bg-gradient-to-b from-black/55 via-black/25 to-transparent"
        }`}
        onMouseLeave={scheduleClose}
        onKeyDown={(e) => e.key === "Escape" && setOpen(false)}
      >
        {/* Scroll progress */}
        <div
          ref={barRef}
          aria-hidden
          className="absolute left-0 top-0 h-[3px] w-full origin-left bg-gradient-to-r from-orange-400 to-amber-300"
          style={{ transform: "scaleX(0)" }}
        />

        {/* Utility bar */}
        <div
          className={`nav-d-block util-bar overflow-hidden border-b text-[12.5px] font-medium transition-all duration-300 ${
            scrolled ? "max-h-0 border-transparent opacity-0" : "max-h-10 opacity-100"
          } ${solid ? "border-stone-200 text-stone-500" : "border-white/15 text-white/80"}`}
        >
          <div className="flex h-10 w-full items-center justify-between px-[var(--page-x)]">
            <div className="flex items-center gap-6">
              {QUICK_CITIES.map((c) => (
                <NavAnchor key={c} to="#explore" className="transition-colors hover:text-orange-400">
                  {c}
                </NavAnchor>
              ))}
            </div>
            <div className="flex items-center gap-6">
              <NavAnchor to="/about" className="transition-colors hover:text-orange-400">
                About Serendib AI
              </NavAnchor>
              <NavAnchor to="/partners" className="transition-colors hover:text-orange-400">
                For Tour Operators
              </NavAnchor>
            </div>
          </div>
        </div>

        {/* Main bar */}
        <div
          className={`flex w-full items-center justify-between gap-6 px-[var(--page-x)] transition-[padding] duration-300 ${
            scrolled ? "py-3" : "py-4"
          }`}
        >
          <a href="#top" className="group flex shrink-0 items-center gap-2.5" aria-label="Serendib AI — home">
            <span className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-orange-400 to-orange-600 shadow-lg shadow-orange-500/30 transition-transform duration-500 group-hover:rotate-[8deg]">
              <Sparkles size={20} className="text-white" />
            </span>
            <span
              className={`font-display text-[28px] font-bold leading-none tracking-tight transition-colors ${
                solid ? "text-stone-900" : "text-white"
              }`}
            >
              Serendib <span className="text-orange-500">AI</span>
            </span>
          </a>

          {/* Desktop menu */}
          <nav className="nav-d-flex items-center gap-[clamp(1.1rem,1.9vw,2rem)]" aria-label="Main">
            {MENUS.map((m) => {
              const isActive = open && active?.key === m.key;
              return (
                <button
                  key={m.key}
                  type="button"
                  aria-haspopup="true"
                  aria-expanded={isActive}
                  onMouseEnter={(e) => openMenu(m.key, e.currentTarget)}
                  onFocus={(e) => openMenu(m.key, e.currentTarget)}
                  onClick={(e) => (isActive ? setOpen(false) : openMenu(m.key, e.currentTarget))}
                  className={`relative flex shrink-0 items-center gap-1 whitespace-nowrap py-2 text-[clamp(12px,0.9vw,13px)] font-semibold uppercase tracking-[0.1em] transition-colors ${
                    solid ? "text-stone-900 hover:text-orange-600" : "text-white hover:text-orange-300"
                  } ${isActive ? (solid ? "!text-orange-600" : "") : ""}`}
                >
                  {m.label}
                  <ChevronDown
                    size={14}
                    className={`transition-transform duration-300 ${isActive ? "rotate-180" : ""}`}
                  />
                  <span
                    aria-hidden
                    className={`absolute -bottom-0.5 left-0 h-[2px] rounded bg-orange-500 transition-all duration-300 ${
                      isActive ? "w-full" : "w-0"
                    }`}
                  />
                </button>
              );
            })}
          </nav>

          {/* Desktop actions */}
          <div className="nav-d-flex shrink-0 items-center gap-2">
            <button type="button" aria-label="Search" onClick={onSearch} className={iconBtn}>
              <Search size={17} />
            </button>
            <button type="button" aria-label="Saved places" className={`${iconBtn} nav-2xl-grid`}>
              <Heart size={17} />
            </button>
            <button type="button" aria-label="Map" className={`${iconBtn} nav-2xl-grid`}>
              <MapIcon size={17} />
            </button>
            <button
              type="button"
              aria-label="Language: English"
              className={`nav-xl-flex h-10 items-center gap-1.5 rounded-full border px-3.5 text-[13px] font-semibold transition-all duration-300 ${
                solid
                  ? "border-stone-200 text-stone-700 hover:border-orange-300 hover:bg-orange-50"
                  : "border-white/30 text-white hover:bg-white/15"
              }`}
            >
              <Globe size={16} /> EN
            </button>

            <span aria-hidden className={`mx-2 h-6 w-px ${solid ? "bg-stone-200" : "bg-white/25"}`} />

            <Link
              to="/login"
              className={`inline-flex items-center gap-2 whitespace-nowrap rounded-full px-4 py-2.5 text-sm font-semibold transition-all duration-300 ${
                solid
                  ? "text-stone-800 hover:bg-stone-100"
                  : "text-white hover:bg-white/15"
              }`}
            >
              <LogIn size={16} /> Login
            </Link>
            <Link
              to="/register"
              className="btn-shine group relative inline-flex items-center gap-2 overflow-hidden whitespace-nowrap rounded-full bg-gradient-to-r from-orange-500 to-amber-500 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-orange-500/30 transition-all duration-300 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-orange-500/40"
            >
              <UserPlus size={16} /> Register
            </Link>
          </div>

          {/* Mobile toggle */}
          <div className="nav-m-flex items-center gap-2">
            <button type="button" aria-label="Search" onClick={onSearch} className={iconBtn}>
              <Search size={17} />
            </button>
            <button
              type="button"
              className={iconBtn}
              onClick={() => setMobileOpen((v) => !v)}
              aria-label={mobileOpen ? "Close menu" : "Open menu"}
              aria-expanded={mobileOpen}
            >
              {mobileOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>
        </div>

        {/* Desktop mega panel — one persistent card that glides between items */}
        {activeCfg && (
          <div
            className="nav-d-block absolute top-full"
            style={{
              left: active.left,
              width: active.width,
              opacity: open ? 1 : 0,
              transform: open ? "translateY(0)" : "translateY(-8px)",
              visibility: open ? "visible" : "hidden",
              pointerEvents: open ? "auto" : "none",
              transition: `${
                animatePos
                  ? "left 320ms cubic-bezier(.22,1,.36,1), width 320ms cubic-bezier(.22,1,.36,1), "
                  : ""
              }opacity 220ms ease, transform 220ms ease, visibility 220ms`,
            }}
            onMouseEnter={cancelClose}
          >
            <div className="pt-2">
              <div className="relative rounded-2xl border border-stone-200/70 bg-white p-6 shadow-[0_30px_80px_-20px_rgba(14,21,18,0.4)]">
                <span
                  aria-hidden
                  className="absolute -top-1.5 h-3 w-3 rotate-45 border-l border-t border-stone-200/70 bg-white"
                  style={{ left: active.caret - 6, transition: "left 320ms cubic-bezier(.22,1,.36,1)" }}
                />
                <div key={activeCfg.key} className="menu-in">
                  <activeCfg.Panel />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Mobile sheet */}
        {mobileOpen && (
          <div className="absolute inset-x-0 top-full max-h-[80vh] overflow-y-auto border-t border-stone-200 bg-white px-6 pb-6 pt-2 shadow-2xl nav-m-block">
            {MENUS.map((m) => {
              const isOpen = mobileSection === m.key;
              return (
                <div key={m.key} className="border-b border-stone-100">
                  <button
                    type="button"
                    className="flex w-full items-center justify-between py-4 text-left text-[15px] font-semibold uppercase tracking-wider text-stone-900"
                    aria-expanded={isOpen}
                    onClick={() => setMobileSection(isOpen ? null : m.key)}
                  >
                    {m.label}
                    <ChevronDown size={18} className={`transition-transform duration-300 ${isOpen ? "rotate-180" : ""}`} />
                  </button>
                  {isOpen && (
                    <ul className="menu-in space-y-1 pb-4">
                      {m.subs.map((s) => (
                        <li key={s}>
                          <NavAnchor
                            to="#"
                            className="block rounded-lg px-3 py-2 text-[15px] text-stone-600 hover:bg-orange-50 hover:text-orange-600"
                          >
                            {s}
                          </NavAnchor>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              );
            })}
            <div className="mt-6 grid grid-cols-2 gap-3">
              <Link
                to="/login"
                className="flex items-center justify-center gap-2 rounded-full border border-stone-200 py-3 text-[15px] font-semibold text-stone-900"
              >
                <LogIn size={17} /> Login
              </Link>
              <Link
                to="/register"
                className="flex items-center justify-center gap-2 rounded-full bg-gradient-to-r from-orange-500 to-amber-500 py-3 text-[15px] font-semibold text-white"
              >
                <UserPlus size={17} /> Register
              </Link>
            </div>
          </div>
        )}
      </header>
    </>
  );
}

/* ------------------------------------------------------------------ */
/*  Search modal                                                       */
/* ------------------------------------------------------------------ */

function SearchModal({ open, onClose }) {
  const inputRef = useRef(null);
  const [q, setQ] = useState("");

  useEffect(() => {
    if (!open) return;
    setQ("");
    const t = setTimeout(() => inputRef.current?.focus(), 60);
    const onKey = (e) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => {
      clearTimeout(t);
      window.removeEventListener("keydown", onKey);
    };
  }, [open, onClose]);

  if (!open) return null;

  const popular = ["Sigiriya", "Kandy to Ella train", "Whale watching in Mirissa", "Best time to visit", "Rice & curry"];

  return (
    <div className="fixed inset-0 z-[70] flex items-start justify-center px-4 pt-[14vh]" role="dialog" aria-modal="true" aria-label="Search">
      <div className="fade-in absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="fade-up relative w-full max-w-2xl overflow-hidden rounded-2xl bg-white shadow-2xl">
        <div className="flex items-center gap-3 border-b border-stone-200 px-5 py-4">
          <Search size={20} className="text-orange-500" />
          <input
            ref={inputRef}
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Search destinations, food, events, guides…"
            className="w-full bg-transparent text-lg text-stone-900 outline-none placeholder:text-stone-400"
          />
          <button
            type="button"
            onClick={onClose}
            className="rounded-md border border-stone-200 px-2 py-1 text-xs font-medium text-stone-500 hover:bg-stone-50"
          >
            Esc
          </button>
        </div>
        <div className="p-5">
          <button
            type="button"
            className="group mb-5 flex w-full items-center gap-3 rounded-xl bg-orange-50 p-3.5 text-left transition-colors hover:bg-orange-100"
          >
            <span className="grid h-9 w-9 place-items-center rounded-lg bg-orange-500 text-white">
              <Sparkles size={17} />
            </span>
            <span className="text-[15px] text-stone-800">
              Ask Serendib AI: <span className="font-semibold">“{q || "Plan 5 days in Ella and Kandy"}”</span>
            </span>
          </button>
          <p className="mb-3 text-[12px] font-semibold text-stone-400">Popular searches</p>
          <div className="flex flex-wrap gap-2">
            {popular.map((p) => (
              <button
                key={p}
                type="button"
                onClick={() => setQ(p)}
                className="rounded-full border border-stone-200 px-3.5 py-1.5 text-sm text-stone-700 transition-colors hover:border-orange-300 hover:bg-orange-50"
              >
                {p}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Global CSS (keyframes + a few helpers Tailwind can't express)      */
/* ------------------------------------------------------------------ */

const STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

html { scroll-behavior: smooth; }
.serendib-root section[id] { scroll-margin-top: 72px; }
.font-display { font-family: 'Cormorant Garamond', Georgia, 'Times New Roman', serif; }

/* ---- Full-width layout ---------------------------------------------------
   One fluid side-padding token used by every page wrapper (replaces the old
   max-w-7xl caps): 40px at 1280px wide, growing to 80px on very wide screens. */
:root { --page-x: clamp(1.25rem, 3.2vw, 5rem); }

/* ---- Navbar: desktop menu from 1240px, optional extras on wider screens - */
.nav-d-flex, .nav-d-block, .nav-xl-flex, .nav-2xl-grid { display: none; }
.nav-m-flex { display: flex; }
.nav-m-block { display: block; }
@media (min-width: 1240px) {
  .nav-d-flex { display: flex; }
  .nav-d-block { display: block; }
  .nav-m-flex, .nav-m-block { display: none; }
}
@media (min-width: 1440px) { .nav-xl-flex { display: flex; } }
@media (min-width: 1600px) { .nav-2xl-grid { display: grid; } }

/* ---- Hero: fills the viewport height, never clips on short screens ------ */
.hero-section { min-height: 100vh; min-height: 100svh; }
.hero-pad { padding-top: 10rem; padding-bottom: 9.5rem; }
.hero-controls { bottom: 5.25rem; }
@media (max-height: 820px) {
  .hero-pad { padding-top: 8.25rem; padding-bottom: 9.75rem; }
}
@media (max-height: 700px) {
  .util-bar { display: none !important; }
  .hero-pad { padding-top: 6rem; padding-bottom: 7.25rem; }
  .hero-controls { bottom: 4.25rem; }
  .hero-loc { display: none !important; }
  .hero-panel { gap: .375rem; }
  .hero-panel .hp-tile { padding-top: .6rem; padding-bottom: .6rem; }
  .hero-panel .hp-tall { height: 60px; }
  .hero-panel .hp-weather { padding: .65rem .9rem; }
  .hero-panel .hp-festival { display: none; }
}
.serendib-root a:focus-visible,
.serendib-root button:focus-visible,
.serendib-root input:focus-visible { outline: 2px solid #F97316; outline-offset: 2px; }

@keyframes wordIn {
  from { opacity: 0; transform: translateY(45%) rotate(1.5deg); filter: blur(8px); }
  to   { opacity: 1; transform: none; filter: blur(0); }
}
.word-in { display: inline-block; opacity: 0; animation: wordIn .95s cubic-bezier(.22,1,.36,1) forwards; }

@keyframes fadeUp { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: none; } }
.fade-up { opacity: 0; animation: fadeUp .8s cubic-bezier(.22,1,.36,1) forwards; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.fade-in { animation: fadeIn .5s ease both; }

@keyframes menuIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.menu-in { animation: menuIn .28s ease both; }

@keyframes kenburns { from { transform: scale(1); } to { transform: scale(1.11); } }
.kenburns { animation: kenburns 10s ease-out forwards; }

@keyframes dashFill { from { transform: scaleX(0); } to { transform: scaleX(1); } }
.dash-fill { transform-origin: left; animation: dashFill ${SLIDE_MS}ms linear forwards; }

@keyframes marquee { to { transform: translateX(-50%); } }
.marquee { animation: marquee 70s linear infinite; }
.marquee:hover { animation-play-state: paused; }
.mask-x {
  -webkit-mask-image: linear-gradient(to right, transparent, #000 5%, #000 95%, transparent);
          mask-image: linear-gradient(to right, transparent, #000 5%, #000 95%, transparent);
}

@keyframes pulseDot { 0%, 100% { opacity: .55; transform: scale(1); } 50% { opacity: 1; transform: scale(1.35); } }
.pulse-dot { animation: pulseDot 2.2s ease-in-out infinite; }

@keyframes flowDown {
  0%   { top: 0; opacity: 0; }
  20%  { opacity: 1; }
  80%  { opacity: 1; }
  100% { top: 100%; opacity: 0; }
}
.flow-dot { position: absolute; left: 50%; margin-left: -3px; animation: flowDown 1.8s ease-in-out infinite; }

.btn-shine { isolation: isolate; }
.btn-shine::after {
  content: ""; position: absolute; inset: 0; pointer-events: none; z-index: -1;
  background: linear-gradient(115deg, transparent 30%, rgba(255,255,255,.4) 50%, transparent 70%);
  transform: translateX(-120%); transition: transform .8s ease;
}
.btn-shine:hover::after { transform: translateX(120%); }

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .word-in, .fade-up { opacity: 1; animation: none; filter: none; }
  .fade-in, .menu-in, .kenburns, .marquee, .pulse-dot, .flow-dot { animation: none; }
  .dash-fill { animation: none; transform: scaleX(1); }
}
`;

const pad = (n) => String(n).padStart(2, "0");

/* ------------------------------------------------------------------ */
/*  Hero: side panel (weather + quick tools)                           */
/* ------------------------------------------------------------------ */

const tileBase =
  "hp-tile group flex items-center justify-center gap-2.5 rounded-2xl border border-white/10 bg-[#141a17]/60 px-4 py-3.5 text-[12px] font-bold uppercase tracking-[0.12em] text-white backdrop-blur-xl transition-all duration-300 hover:-translate-y-0.5 hover:border-orange-400/50 hover:bg-[#1b231f]/80";

function WeatherCard({ place, region, data }) {
  const meta = data ? wmo(data.code) : null;
  const Icon = meta ? meta.icon : Cloud;
  return (
    <div className="hp-weather rounded-2xl border border-white/10 bg-[#141a17]/60 p-4 text-white backdrop-blur-xl">
      <div className="flex items-center justify-between text-[11px] font-semibold uppercase tracking-[0.16em] text-white/50">
        <span>Weather in {place}</span>
        <span className="flex items-center gap-1.5 normal-case tracking-normal text-emerald-300">
          <span className="pulse-dot h-1.5 w-1.5 rounded-full bg-emerald-400" /> Live
        </span>
      </div>
      <div key={place} className="fade-in mt-3 flex items-end justify-between">
        <div className="flex items-center gap-3.5">
          <Icon size={34} className="text-orange-300" strokeWidth={1.6} />
          <div>
            <p className="text-[32px] font-semibold leading-none">
              {data ? `${Math.round(data.temp)}°C` : "--"}
              {data && (
                <span className="ml-2 text-xs font-normal text-white/60">feels {Math.round(data.feels)}°</span>
              )}
            </p>
            <p className="mt-1.5 text-[13px] text-white/70">{meta ? meta.label : region}</p>
          </div>
        </div>
        <div className="space-y-1.5 text-right text-xs text-white/70">
          <p className="flex items-center justify-end gap-1.5">
            <Droplets size={13} /> {data ? `${Math.round(data.humidity)}%` : "--"}
          </p>
          <p className="flex items-center justify-end gap-1.5">
            <Wind size={13} /> {data ? `${Math.round(data.wind)} km/h` : "--"}
          </p>
        </div>
      </div>
    </div>
  );
}

function HeroPanel({ slide, weather, nextEvent }) {
  return (
    <aside className="hero-panel hidden w-full flex-col gap-2.5 xl:flex" aria-label="Quick tools">
      <WeatherCard place={slide.place} region={slide.region} data={weather[slide.place]} />

      <div className="grid grid-cols-2 gap-2.5">
        <button type="button" className={tileBase}>
          <FileText size={17} className="text-orange-300" /> Visa info
        </button>
        <button type="button" className={tileBase}>
          <Bus size={17} className="text-orange-300" /> Transport
        </button>
      </div>

      <div className="grid grid-cols-2 gap-2.5">
        <button
          type="button"
          className="hp-tall group relative h-[92px] overflow-hidden rounded-2xl border border-white/10 text-left"
        >
          <SmartImg
            src={wiki(IMG.ellaBridge2, 500)}
            alt=""
            className="absolute inset-0 h-full w-full object-cover transition-transform duration-700 group-hover:scale-110"
          />
          <span className="absolute inset-0 bg-gradient-to-t from-black/80 to-black/20" />
          <span className="absolute bottom-3 left-4 flex items-center gap-2 text-[12px] font-bold uppercase tracking-[0.12em] text-white">
            <Building2 size={16} className="text-orange-300" /> Hotels
          </span>
        </button>
        <button type="button" className={`${tileBase} hp-tall h-[92px] flex-col !gap-2`}>
          <MapIcon size={22} className="text-orange-300" /> Map
        </button>
      </div>

      <button
        type="button"
        className="hp-tile btn-shine relative flex items-center justify-center gap-2.5 overflow-hidden rounded-2xl bg-gradient-to-r from-orange-500 to-amber-500 px-4 py-4 text-[12px] font-bold uppercase tracking-[0.12em] text-white shadow-lg shadow-orange-500/25 transition-all duration-300 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-orange-500/35"
      >
        <Sparkles size={17} /> Build your itinerary
      </button>

      <div className="grid grid-cols-2 gap-2.5">
        <button type="button" className={tileBase}>
          <Wallet size={17} className="text-orange-300" /> Trip budget
        </button>
        <button type="button" className={tileBase}>
          <Banknote size={17} className="text-orange-300" /> Currency
        </button>
      </div>

      {nextEvent && (
        <button
          type="button"
          className="hp-festival group flex items-center gap-3.5 rounded-2xl border border-white/10 bg-[#141a17]/60 p-4 text-left text-white backdrop-blur-xl transition-all duration-300 hover:-translate-y-0.5 hover:border-orange-400/50"
        >
          <span className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-orange-500/20 text-orange-300">
            <Calendar size={20} />
          </span>
          <span className="min-w-0 flex-1">
            <span className="block text-[11px] font-semibold text-amber-300">Next festival</span>
            <span className="block truncate text-[15px] font-semibold">{nextEvent.name}</span>
            <span className="block text-[12px] text-white/60">
              {nextEvent.label} · {nextEvent.days === 0 ? "today" : `in ${nextEvent.days} days`}
            </span>
          </span>
          <ArrowRight size={16} className="text-white/50 transition-transform group-hover:translate-x-1" />
        </button>
      )}
    </aside>
  );
}

/* ------------------------------------------------------------------ */
/*  Hero: live ticker along the bottom edge                            */
/* ------------------------------------------------------------------ */

const TICKER_CITIES = ["Colombo", "Kandy", "Ella", "Galle", "Trincomalee", "Jaffna"];

function LiveTicker({ weather, now }) {
  const events = upcomingEvents(now);
  const items = [];
  const n = Math.max(TICKER_CITIES.length, events.length);
  for (let i = 0; i < n; i += 1) {
    const city = TICKER_CITIES[i];
    if (city && weather[city]) items.push({ type: "weather", name: city, data: weather[city] });
    if (events[i]) items.push({ type: "event", ...events[i] });
  }
  const half = [...items, ...items];
  const track = [...half, ...half];

  return (
    <div className="absolute inset-x-0 bottom-0 z-20 flex h-14 items-center border-t border-white/10 bg-[#0B100D]/90 backdrop-blur-md">
      <div className="flex shrink-0 items-center gap-2.5 px-5 text-[11px] font-bold uppercase tracking-[0.16em] text-orange-400 md:px-8">
        <span className="pulse-dot h-2 w-2 rounded-full bg-orange-400" />
        <span className="hidden sm:inline">Live from Sri Lanka</span>
        <span className="sm:hidden">Live</span>
      </div>

      <div className="hidden shrink-0 flex-col justify-center border-x border-white/10 px-5 sm:flex">
        <p className="text-[15px] font-bold leading-none text-white">
          {fmtTime.format(now)} <span className="text-[10px] font-medium text-white/50">SLST</span>
        </p>
        <p className="mt-1 text-[10px] font-medium uppercase tracking-wider text-white/50">{fmtDate.format(now)}</p>
      </div>

      <div className="mask-x relative min-w-0 flex-1 overflow-hidden">
        {items.length > 0 && (
          <div className="marquee flex w-max items-center gap-3 py-2 pl-4">
            {track.map((it, i) => {
              if (it.type === "weather") {
                const Icon = wmo(it.data.code).icon;
                return (
                  <span
                    key={i}
                    className="flex shrink-0 items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3.5 py-1.5 text-[13px] text-white/85"
                  >
                    <Icon size={15} className="text-orange-300" />
                    {it.name}
                    <b className="font-semibold text-white">{Math.round(it.data.temp)}°</b>
                  </span>
                );
              }
              return (
                <span
                  key={i}
                  className="flex shrink-0 items-center gap-2 rounded-full border border-orange-400/25 bg-orange-500/10 px-3.5 py-1.5 text-[13px] text-white/85"
                >
                  <Calendar size={15} className="text-orange-300" />
                  {it.short}
                  <b className="font-semibold text-white">{it.days === 0 ? "today" : `in ${it.days} days`}</b>
                </span>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Page content data                                                  */
/* ------------------------------------------------------------------ */

const STATS = [
  { to: 9, label: "Provinces to explore" },
  { to: 8, label: "UNESCO World Heritage Sites" },
  { to: 1340, suffix: " km", label: "Of coastline" },
  { to: 8, label: "Specialist AI agents" },
];

const STEPS = [
  { num: "01", title: "Tell us about your trip", desc: "Share your budget, travel dates, interests, travel style, and preferred experiences." },
  { num: "02", title: "AI understands you", desc: "Serendib AI analyzes your traveler preferences and trip requirements." },
  { num: "03", title: "Specialized agents collaborate", desc: "Different AI agents research destinations, food, context and travel options together." },
  { num: "04", title: "Receive your smart itinerary", desc: "The system produces an optimized, personalized Sri Lankan itinerary designed just for you." },
];

const AGENTS = [
  { icon: Brain, title: "Traveler Intelligence", description: "Understands preferences, interests, budget and travel style." },
  { icon: Compass, title: "Destination Discovery", description: "Finds Sri Lankan places suited to the traveler." },
  { icon: Utensils, title: "Local Food Intelligence", description: "Recommends authentic dishes, restaurants and local food experiences." },
  { icon: Route, title: "Smart Trip Planning", description: "Combines all recommendations into a complete itinerary." },
  { icon: Navigation, title: "Route Optimization", description: "Organizes destinations to reduce unnecessary travel and improve trip flow." },
  { icon: CloudSun, title: "Weather & Context", description: "Uses current conditions and travel context when creating or re-planning trips." },
  { icon: Wallet, title: "Budget Intelligence", description: "Estimates spending across accommodation, food, transport, attractions and activities." },
  { icon: ShieldCheck, title: "Safety-Aware Planning", description: "Considers trusted travel information without inventing critical safety data." },
];

const DESTINATIONS = [
  { name: "Sigiriya", category: "Culture & Heritage", desc: "Climb the 5th-century rock fortress rising out of the jungle.", img: IMG.sigiriyaRock, span: "lg:col-span-2 lg:row-span-2", big: true },
  { name: "Ella", category: "Mountains & Nature", desc: "Tea hills, waterfalls and the Nine Arch Bridge.", img: IMG.ellaBridge2 },
  { name: "Mirissa", category: "Beaches", desc: "Whale watching and quiet sunset coves.", img: IMG.mirissaSecret },
  { name: "Kandy", category: "Culture & Heritage", desc: "The Temple of the Tooth and lakeside evenings.", img: IMG.toothAlt },
  { name: "Yala", category: "Wildlife", desc: "Leopards, elephants and open savanna.", img: IMG.leopard },
  { name: "Galle", category: "Heritage & Coast", desc: "Dutch-era ramparts above the Indian Ocean.", img: IMG.galleDutch },
];

const SAMPLE_DAYS = [
  {
    day: "01",
    title: "Colombo",
    items: [
      ["09:00", "Gangaramaya Temple"],
      ["12:30", "Pettah Market and lunch"],
      ["16:30", "Galle Face at sunset"],
    ],
  },
  {
    day: "02",
    title: "Colombo → Kandy",
    items: [
      ["08:30", "Scenic drive to Kandy"],
      ["13:00", "Temple of the Tooth"],
      ["16:30", "Kandy Lake walk and local dining"],
    ],
  },
  {
    day: "03",
    title: "Kandy → Ella",
    items: [
      ["Morning", "Scenic train journey"],
      ["Afternoon", "Nine Arch Bridge"],
      ["Evening", "Local food experience"],
    ],
  },
];

const BENEFITS = [
  { title: "Personalized", desc: "Every journey is based on the traveler's interests and constraints." },
  { title: "Locally relevant", desc: "Designed specifically around authentic Sri Lankan travel." },
  { title: "Context aware", desc: "Recommendations can respond to changing trip conditions." },
  { title: "Budget conscious", desc: "Travel costs are actively considered during planning." },
  { title: "Explainable", desc: "Understand exactly why important recommendations were made." },
  { title: "Responsible", desc: "Critical information relies on trusted sources instead of AI guesses." },
];

const FOOTER_COLS = [
  { title: "Explore", links: ["Cultural Triangle", "Hill Country", "Southern Coast", "East Coast", "Safari Zone"] },
  { title: "Plan", links: ["Itinerary Builder", "Trip Cost Estimator", "Hotels", "Visa Information", "Travel Tips"] },
  { title: "Platform", links: ["How It Works", "AI Agents", "Responsible AI", "Blog"] },
  { title: "Company", links: ["About", "Contact", "For Tour Operators"] },
];

/* Animated connector used in the "how agents communicate" diagram */
function Connector({ accent = false }) {
  return (
    <div className={`relative my-3 h-10 w-px ${accent ? "bg-orange-300" : "bg-[#E4D9C8]"}`} aria-hidden>
      <span className="flow-dot h-1.5 w-1.5 rounded-full bg-orange-400" />
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Home                                                                */
/* ------------------------------------------------------------------ */

function Home() {
  const [pos, setPos] = useState({ cur: 0, last: 0 });
  const [searchOpen, setSearchOpen] = useState(false);
  const [day, setDay] = useState(0);
  const weather = useWeather();
  const now = useColomboClock();
  const total = heroSlides.length;

  const goTo = useCallback((i) => setPos((p) => ({ cur: (i + total) % total, last: p.cur })), [total]);
  const next = useCallback(() => setPos((p) => ({ cur: (p.cur + 1) % total, last: p.cur })), [total]);
  const prev = useCallback(() => setPos((p) => ({ cur: (p.cur - 1 + total) % total, last: p.cur })), [total]);
  const closeSearch = useCallback(() => setSearchOpen(false), []);

  // Auto-advance. The timer restarts whenever the slide changes (including manual clicks).
  useEffect(() => {
    const t = setTimeout(next, SLIDE_MS);
    return () => clearTimeout(t);
  }, [pos.cur, next]);

  const slide = heroSlides[pos.cur];
  const words = slide.headline.split(" ");
  const mounted = new Set([pos.cur, pos.last, (pos.cur + 1) % total, (pos.cur - 1 + total) % total]);
  const nextEvent = upcomingEvents(now)[0];

  return (
    <div
      className="serendib-root min-h-screen w-full overflow-x-hidden bg-[#FFFCF8] text-[#1C1917] antialiased"
      style={{ fontFamily: "'Inter', ui-sans-serif, system-ui, sans-serif" }}
    >
      <style>{STYLES}</style>

      <Navbar onSearch={() => setSearchOpen(true)} />
      <SearchModal open={searchOpen} onClose={closeSearch} />

      <main>
        {/* ============================================================ */}
        {/* HERO — slideshow, per-slide headline, live tools + ticker     */}
        {/* ============================================================ */}
        <section id="top" className="hero-section relative flex w-full flex-col overflow-hidden bg-[#0E1512]">
          {/* Only the current / previous / neighbouring slides are mounted, so the browser never downloads all 15 large photos at once */}
          {heroSlides.map((s, i) => {
            if (!mounted.has(i)) return null;
            const isCur = i === pos.cur;
            const animate = isCur || i === pos.last;
            return (
              <div
                key={s.file}
                aria-hidden={!isCur}
                className="absolute inset-0 transition-opacity duration-[1600ms] ease-in-out"
                style={{ opacity: isCur ? 1 : 0 }}
              >
                <SmartImg
                  src={wiki(s.file, 2400)}
                  alt={s.alt}
                  eager
                  className={`absolute inset-0 h-full w-full object-cover ${animate ? "kenburns" : ""}`}
                />
              </div>
            );
          })}

          {/* Readability overlays */}
          <div className="absolute inset-0 bg-gradient-to-r from-black/70 via-black/25 to-black/10" />
          <div className="absolute inset-x-0 top-0 h-52 bg-gradient-to-b from-black/55 to-transparent" />
          <div className="absolute inset-x-0 bottom-0 h-56 bg-gradient-to-t from-[#0E1512] via-[#0E1512]/60 to-transparent" />

          {/* Content */}
          <div className="hero-pad relative z-10 grid w-full flex-1 items-center gap-10 px-[var(--page-x)] xl:grid-cols-[minmax(0,1fr)_clamp(340px,24vw,460px)]">
            <div className="max-w-3xl">
              <div className="fade-up mb-[clamp(1rem,3vh,1.75rem)] inline-flex items-center gap-2.5 rounded-full border border-white/25 bg-white/10 px-4 py-1.5 text-[13px] font-medium text-white/90 backdrop-blur-md">
                <span className="pulse-dot h-1.5 w-1.5 rounded-full bg-orange-400" />
                AI-powered Sri Lankan travel planning
              </div>

              <div key={pos.cur}>
                <h1
                  aria-label={slide.headline}
                  className="font-display text-[clamp(2.75rem,min(7.2vw,12.5vh),6.25rem)] font-semibold leading-[0.98] tracking-tight text-white drop-shadow-[0_4px_24px_rgba(0,0,0,0.45)]"
                >
                  {words.map((w, i) => (
                    <span key={i} aria-hidden className="word-in mr-[0.22em]" style={{ animationDelay: `${120 + i * 90}ms` }}>
                      {w}
                    </span>
                  ))}
                </h1>
                <p
                  className="fade-up mt-[clamp(1rem,2.6vh,1.5rem)] max-w-xl text-[clamp(1rem,2.4vh,1.125rem)] leading-relaxed text-white/85"
                  style={{ animationDelay: `${260 + words.length * 90}ms` }}
                >
                  {slide.sub}
                </p>
              </div>

              <div className="fade-up mt-[clamp(1.25rem,4vh,2.25rem)] flex flex-wrap items-center gap-4" style={{ animationDelay: "500ms" }}>
                <button
                  type="button"
                  className="btn-shine relative overflow-hidden rounded-full bg-orange-500 px-8 py-[clamp(0.7rem,2vh,1rem)] text-base font-semibold text-white shadow-lg shadow-orange-500/30 transition-all duration-300 hover:-translate-y-0.5 hover:bg-orange-600 hover:shadow-xl hover:shadow-orange-500/40"
                >
                  Plan my trip
                </button>
                <a
                  href="#how-it-works"
                  className="group inline-flex items-center gap-2 rounded-full border border-white/30 bg-white/10 px-7 py-[clamp(0.7rem,2vh,1rem)] text-base font-semibold text-white backdrop-blur-sm transition-all duration-300 hover:bg-white/20"
                >
                  Find out more
                  <ArrowRight size={18} className="transition-transform duration-300 group-hover:translate-x-1" />
                </a>
              </div>
            </div>

            <HeroPanel slide={slide} weather={weather} nextEvent={nextEvent} />
          </div>

          {/* Slide controls */}
          <div className="hero-controls absolute inset-x-0 z-20">
            <div className="w-full px-[var(--page-x)]">
              <p key={pos.cur} className="hero-loc fade-in flex items-center gap-1.5 text-sm font-medium text-white/90">
                <MapPin size={15} className="text-orange-400" />
                {slide.location}
              </p>
              <div className="mt-3 flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={prev}
                    aria-label="Previous photo"
                    className="grid h-9 w-9 place-items-center rounded-full border border-white/25 bg-black/25 text-white backdrop-blur-sm transition-colors hover:bg-black/50"
                  >
                    <ChevronLeft size={18} />
                  </button>
                  <button
                    type="button"
                    onClick={next}
                    aria-label="Next photo"
                    className="grid h-9 w-9 place-items-center rounded-full border border-white/25 bg-black/25 text-white backdrop-blur-sm transition-colors hover:bg-black/50"
                  >
                    <ChevronRight size={18} />
                  </button>
                </div>

                <div className="flex items-center gap-1.5">
                  {heroSlides.map((s, i) => (
                    <button
                      key={s.file}
                      type="button"
                      onClick={() => goTo(i)}
                      aria-label={`Go to photo ${i + 1} of ${total}: ${s.location}`}
                      aria-current={i === pos.cur}
                      className="group flex h-6 items-center"
                    >
                      <span
                        className={`relative block h-[3px] overflow-hidden rounded-full bg-white/30 transition-all duration-500 ${
                          i === pos.cur ? "w-12" : "w-3.5 group-hover:bg-white/60"
                        }`}
                      >
                        {i === pos.cur && <span key={pos.cur} className="dash-fill absolute inset-0 bg-orange-400" />}
                      </span>
                    </button>
                  ))}
                </div>

                <span className="hidden text-xs tabular-nums text-white/60 sm:inline">
                  {pad(pos.cur + 1)} / {pad(total)}
                </span>
              </div>
            </div>
          </div>

          <LiveTicker weather={weather} now={now} />
        </section>

        {/* ============================================================ */}
        {/* INTRODUCTION + STATS                                          */}
        {/* ============================================================ */}
        <section id="intro" className="w-full px-[var(--page-x)] py-24 md:py-32">
          <div className="w-full">
            <Reveal className="mx-auto max-w-4xl text-center">
              <h2 className="font-display text-4xl font-semibold leading-[1.05] md:text-6xl">
                One intelligent platform for your entire Sri Lankan journey.
              </h2>
              <p className="mx-auto mt-8 max-w-3xl text-lg leading-relaxed text-[#57534E] md:text-xl">
                Travelers usually have to switch between maps, travel blogs, restaurant websites, weather apps,
                reviews, budget calculations, and safety information.{" "}
                <strong className="font-semibold text-[#1C1917]">
                  Serendib AI brings these decisions together into one intelligent travel experience.
                </strong>
              </p>
            </Reveal>

            <div className="mx-auto mt-16 grid max-w-5xl grid-cols-2 gap-y-10 border-t border-[#EAE2D6] pt-12 md:grid-cols-4">
              {STATS.map((s, i) => (
                <div key={s.label} className={`px-4 text-center ${i > 0 ? "md:border-l md:border-[#EAE2D6]" : ""}`}>
                  <p className="font-display text-5xl font-semibold text-[#1C1917] md:text-6xl">
                    <CountUp to={s.to} suffix={s.suffix} />
                  </p>
                  <p className="mt-2 text-sm text-[#78716C]">{s.label}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ============================================================ */}
        {/* HOW IT WORKS                                                  */}
        {/* ============================================================ */}
        <section id="how-it-works" className="w-full border-y border-[#EAE2D6] bg-[#FBF3EA] px-[var(--page-x)] py-24">
          <div className="w-full">
            <Reveal className="mb-16 text-center">
              <h2 className="font-display text-4xl font-semibold md:text-5xl">From an idea to a complete journey</h2>
            </Reveal>

            <div className="relative grid gap-10 md:grid-cols-4">
              <div className="absolute left-[12.5%] right-[12.5%] top-8 z-0 hidden h-px bg-gradient-to-r from-transparent via-orange-300 to-transparent md:block" />
              {STEPS.map((step, idx) => (
                <Reveal key={step.num} delay={idx * 100} className="group relative z-10 flex flex-col items-center text-center">
                  <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl border border-[#EAE2D6] bg-white text-xl font-bold text-orange-500 shadow-sm transition-all duration-300 group-hover:-translate-y-1 group-hover:bg-orange-500 group-hover:text-white group-hover:shadow-lg group-hover:shadow-orange-500/25">
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
        {/* MULTI-AGENT INTELLIGENCE                                      */}
        {/* ============================================================ */}
        <section id="features" className="w-full px-[var(--page-x)] py-24 md:py-32">
          <div className="w-full">
            <Reveal className="mb-16 text-center">
              <h2 className="font-display text-4xl font-semibold leading-[1.05] md:text-6xl">
                Multiple AI specialists. <br className="hidden md:block" />
                One seamless journey.
              </h2>
            </Reveal>

            <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-4">
              {AGENTS.map((agent, idx) => {
                const Icon = agent.icon;
                return (
                  <Reveal key={agent.title} delay={(idx % 4) * 80} className="h-full">
                    <div className="group relative h-full overflow-hidden rounded-2xl border border-[#EAE2D6] bg-white p-7 transition-all duration-300 hover:-translate-y-1.5 hover:border-orange-300 hover:shadow-[0_18px_40px_-18px_rgba(249,115,22,0.45)]">
                      <span className="absolute -right-10 -top-10 h-28 w-28 rounded-full bg-orange-100/0 blur-2xl transition-all duration-500 group-hover:bg-orange-200/60" />
                      <div className="relative mb-6 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-orange-50 text-orange-500 transition-all duration-300 group-hover:bg-orange-500 group-hover:text-white">
                        <Icon size={22} />
                      </div>
                      <h3 className="relative mb-2.5 text-lg font-semibold">{agent.title}</h3>
                      <p className="relative text-sm leading-relaxed text-[#78716C]">{agent.description}</p>
                    </div>
                  </Reveal>
                );
              })}
            </div>
          </div>
        </section>

        {/* ============================================================ */}
        {/* HOW OUR AGENTS COMMUNICATE                                    */}
        {/* ============================================================ */}
        <section className="w-full overflow-hidden border-y border-[#EAE2D6] bg-[#FBF3EA] px-[var(--page-x)] py-24">
          <div className="mx-auto max-w-5xl text-center">
            <Reveal>
              <h2 className="font-display mb-14 text-3xl font-semibold text-[#44403C] md:text-4xl">
                How our agents communicate
              </h2>
            </Reveal>

            <Reveal className="flex flex-col items-center" from="scale">
              <div className="flex h-14 items-center justify-center rounded-full border border-[#EAE2D6] bg-white px-8 font-medium shadow-sm">
                Traveler
              </div>
              <Connector />
              <div className="relative flex h-20 items-center justify-center rounded-2xl border border-orange-200 bg-gradient-to-r from-orange-50 to-orange-100/60 px-10 text-lg font-bold text-orange-600">
                <span className="pulse-dot absolute -right-1.5 -top-1.5 h-4 w-4 rounded-full bg-orange-400" />
                Serendib AI
              </div>
              <Connector />
              <div className="flex w-full flex-col justify-center gap-4 md:flex-row">
                {["Profile Intelligence", "Destination Intelligence", "Food Intelligence"].map((a) => (
                  <div
                    key={a}
                    className="mx-auto flex h-14 w-full max-w-[220px] flex-1 items-center justify-center rounded-xl border border-[#EAE2D6] bg-white text-sm font-medium text-[#44403C] transition-all duration-300 hover:-translate-y-1 hover:border-orange-300"
                  >
                    {a}
                  </div>
                ))}
              </div>
              <Connector />
              <div className="flex h-16 items-center justify-center rounded-xl border border-[#EAE2D6] bg-white px-10 font-semibold text-orange-600">
                Smart Planner
              </div>
              <Connector />
              <div className="flex flex-wrap items-center justify-center gap-x-5 gap-y-2 rounded-full border border-[#EAE2D6] bg-white px-7 py-3 text-xs font-medium text-[#78716C] md:text-sm">
                {["Route", "Weather", "Budget", "Context"].map((x) => (
                  <span key={x} className="flex items-center gap-2">
                    <span className="h-1 w-1 rounded-full bg-orange-300" />
                    {x}
                  </span>
                ))}
              </div>
              <Connector accent />
              <div className="flex h-16 items-center justify-center rounded-full bg-orange-500 px-12 font-bold text-white shadow-md shadow-orange-500/25">
                Personalized Itinerary
              </div>
            </Reveal>
          </div>
        </section>

        {/* ============================================================ */}
        {/* EXPERIENCE SRI LANKA — bento destinations                     */}
        {/* ============================================================ */}
        <section id="explore" className="w-full px-[var(--page-x)] py-24 md:py-32">
          <div className="w-full">
            <Reveal className="mb-12 flex flex-col justify-between gap-6 md:flex-row md:items-end">
              <div>
                <h2 className="font-display mb-4 text-4xl font-semibold leading-[1.05] md:text-6xl">
                  One island. <br className="hidden md:block" />
                  Endless experiences.
                </h2>
                <p className="max-w-xl text-[#57534E]">
                  From ancient heritage to pristine beaches and misty mountains, Sri Lanka offers an unmatched
                  diversity of travel experiences.
                </p>
              </div>
              <button
                type="button"
                className="group flex items-center gap-2 font-medium text-orange-500 transition-colors hover:text-orange-600"
              >
                View all destinations
                <ArrowRight size={18} className="transition-transform duration-300 group-hover:translate-x-1" />
              </button>
            </Reveal>

            <div className="grid gap-4 sm:grid-cols-2 lg:auto-rows-[290px] lg:grid-cols-3">
              {DESTINATIONS.map((d, idx) => (
                <Reveal key={d.name} delay={(idx % 3) * 100} className={`${d.span || ""} min-h-[18rem] lg:min-h-0`} from="scale">
                  <div className="group relative h-full min-h-[18rem] w-full cursor-pointer overflow-hidden rounded-2xl lg:min-h-0">
                    <SmartImg
                      src={wiki(d.img, d.big ? 1400 : 900)}
                      alt={`${d.name} — ${d.category}`}
                      className="absolute inset-0 h-full w-full object-cover transition-transform duration-[900ms] ease-out group-hover:scale-110"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/15 to-transparent" />
                    <div className="absolute inset-x-0 bottom-0 p-6">
                      <span className="mb-2 inline-flex items-center gap-1 rounded-full bg-white/20 px-3 py-1 text-xs font-medium text-white backdrop-blur-md">
                        <MapPin size={12} /> {d.category}
                      </span>
                      <h3 className={`font-display font-semibold leading-none text-white ${d.big ? "text-5xl md:text-6xl" : "text-4xl"}`}>
                        {d.name}
                      </h3>
                      <p className={`mt-2 max-w-md text-sm leading-snug text-white/80 ${d.big ? "" : "line-clamp-2"}`}>{d.desc}</p>
                    </div>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        {/* ============================================================ */}
        {/* SMART ITINERARY SHOWCASE (interactive day tabs)               */}
        {/* ============================================================ */}
        <section className="w-full border-y border-[#EAE2D6] bg-[#FBF3EA] px-[var(--page-x)] py-24">
          <div className="w-full">
            <div className="grid gap-16 lg:grid-cols-2 lg:items-center">
              <Reveal from="left">
                <h2 className="font-display mb-6 text-4xl font-semibold leading-[1.05] md:text-6xl">
                  A complete journey, intelligently connected.
                </h2>
                <p className="mb-8 text-lg leading-relaxed text-[#57534E]">
                  Recommendations are not simply displayed individually. Serendib AI acts as an expert travel
                  coordinator, combining destinations, routes, and timing into an optimized, realistic travel plan.
                </p>
                <ul className="space-y-4">
                  {[
                    "Day-by-day logical scheduling",
                    "Accurate travel times between locations",
                    "Integrated dining and attraction recommendations",
                    "Real-time weather and budget context",
                  ].map((item) => (
                    <li key={item} className="flex items-center gap-3 text-[#44403C]">
                      <div className="flex h-6 w-6 items-center justify-center rounded-full bg-orange-100 text-orange-500">
                        <Sparkles size={12} />
                      </div>
                      {item}
                    </li>
                  ))}
                </ul>
                <button
                  type="button"
                  className="mt-10 rounded-full border border-[#EAE2D6] bg-white px-6 py-3 text-sm font-medium transition-all duration-300 hover:-translate-y-0.5 hover:border-orange-300 hover:bg-orange-50"
                >
                  View sample itinerary
                </button>
              </Reveal>

              <Reveal delay={150} from="right">
                <div className="relative overflow-hidden rounded-3xl border border-[#EAE2D6] bg-white p-6 shadow-xl shadow-black/5 md:p-8">
                  <div className="mb-6 flex flex-wrap items-start justify-between gap-4 border-b border-[#EAE2D6] pb-6">
                    <div>
                      <h3 className="font-display text-3xl font-semibold">Your Sri Lanka journey</h3>
                      <div className="mt-3 flex flex-wrap items-center gap-2 text-xs font-medium text-[#78716C]">
                        {["6 days", "Nature", "Culture", "Food"].map((c) => (
                          <span key={c} className="rounded bg-[#F5F0E8] px-2 py-1">
                            {c}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div className="flex gap-2" role="tablist" aria-label="Sample itinerary days">
                      {SAMPLE_DAYS.map((d, i) => (
                        <button
                          key={d.day}
                          type="button"
                          role="tab"
                          aria-selected={day === i}
                          onClick={() => setDay(i)}
                          className={`rounded-full px-4 py-2 text-sm font-semibold transition-all duration-300 ${
                            day === i
                              ? "bg-orange-500 text-white shadow-md shadow-orange-500/25"
                              : "bg-[#F5F0E8] text-[#57534E] hover:bg-orange-50"
                          }`}
                        >
                          Day {d.day}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div key={day} className="menu-in min-h-[250px]">
                    <h4 className="font-display text-3xl font-semibold">{SAMPLE_DAYS[day].title}</h4>
                    <ol className="mt-6 space-y-6 border-l border-[#EAE2D6] pl-6">
                      {SAMPLE_DAYS[day].items.map(([time, what]) => (
                        <li key={what} className="relative">
                          <span className="absolute -left-[31px] top-1.5 h-3 w-3 rounded-full border-2 border-white bg-orange-500 shadow" />
                          <p className="text-xs font-semibold text-orange-600">{time}</p>
                          <p className="text-[15px] font-medium text-[#1C1917]">{what}</p>
                        </li>
                      ))}
                    </ol>
                  </div>

                  <div className="mt-4 grid grid-cols-4 gap-3 border-t border-[#EAE2D6] pt-6 text-center">
                    {[
                      { icon: Wallet, label: "Est. cost", value: "Rs. 65,000" },
                      { icon: CloudSun, label: "Weather", value: "Mild, dry" },
                      { icon: Clock, label: "Travel time", value: "~10h total" },
                      { icon: Route, label: "Distance", value: "~250 km" },
                    ].map(({ icon: Icon, label, value }) => (
                      <div key={label}>
                        <Icon size={16} className="mx-auto mb-1 text-orange-500" />
                        <p className="text-[11px] text-[#78716C]">{label}</p>
                        <p className="text-xs font-semibold">{value}</p>
                      </div>
                    ))}
                  </div>
                  <p className="mt-4 text-center text-[11px] text-[#A8A29E]">Sample itinerary — days 1–3 of 6 shown</p>
                </div>
              </Reveal>
            </div>
          </div>
        </section>

        {/* ============================================================ */}
        {/* ROUTE INTELLIGENCE + WEATHER / CONTEXT / SAFETY               */}
        {/* ============================================================ */}
        <section className="w-full px-[var(--page-x)] py-24 md:py-32">
          <div className="w-full">
            <div className="grid gap-16 lg:grid-cols-2">
              <Reveal>
                <h2 className="font-display mb-6 text-4xl font-semibold leading-[1.05] md:text-5xl">
                  Less time planning. <br />
                  More time exploring.
                </h2>
                <p className="mb-10 text-[#57534E]">
                  The Smart Planner considers location, distance, travel time, opening hours, attraction duration,
                  budget, and weather context automatically.
                </p>

                <div className="flex flex-col rounded-2xl border border-[#EAE2D6] bg-[#FBF3EA] p-8">
                  {["Dambulla", "Kandy", "Nuwara Eliya", "Ella"].map((place, i, arr) => (
                    <div key={place} className="group flex items-start gap-4">
                      <div className="flex flex-col items-center">
                        <div className="flex h-8 w-8 items-center justify-center rounded-full border border-[#EAE2D6] bg-white text-xs font-bold text-orange-500 transition-all duration-300 group-hover:bg-orange-500 group-hover:text-white">
                          {i + 1}
                        </div>
                        {i < arr.length - 1 && <div className="my-1 h-12 w-px border-l-2 border-dashed border-orange-200" />}
                      </div>
                      <div className="pb-4 pt-1">
                        <h4 className="text-lg font-semibold">{place}</h4>
                        {i < arr.length - 1 && (
                          <p className="mt-1 flex items-center gap-1 text-xs text-[#78716C]">
                            <Route size={12} /> Optimized route
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </Reveal>

              <Reveal delay={150}>
                <h2 className="font-display mb-6 text-4xl font-semibold leading-[1.05] md:text-5xl">
                  Plans that adapt to the real world.
                </h2>
                <p className="mb-10 text-[#57534E]">
                  Serendib AI uses relevant travel information such as weather, opening hours, seasonality, and road
                  context when producing recommendations.
                </p>

                <div className="grid grid-cols-2 gap-4">
                  {[
                    { icon: CloudSun, label: "Weather", value: "24°C — Light rain" },
                    { icon: Route, label: "Route", value: "Nuwara Eliya → Ella, ~3h" },
                    { icon: Info, label: "Context", value: "Outdoor activity adjusted" },
                    { icon: Wallet, label: "Budget", value: "Within planned budget" },
                  ].map(({ icon: Icon, label, value }) => (
                    <div
                      key={label}
                      className="rounded-xl border border-[#EAE2D6] bg-white p-5 transition-all duration-300 hover:-translate-y-1 hover:border-orange-300 hover:shadow-lg hover:shadow-orange-500/10"
                    >
                      <Icon className="mb-3 text-orange-500" size={22} />
                      <h4 className="mb-1 text-sm font-medium text-[#78716C]">{label}</h4>
                      <p className="text-sm font-semibold">{value}</p>
                    </div>
                  ))}
                  <div className="col-span-2 rounded-xl border border-l-2 border-[#EAE2D6] border-l-orange-500 bg-white p-5">
                    <ShieldCheck className="mb-3 text-orange-500" size={22} />
                    <h4 className="mb-1 text-sm font-medium text-[#78716C]">Safety information</h4>
                    <p className="text-sm font-semibold">Verified information sources</p>
                  </div>
                </div>

                <div className="mt-8 rounded-xl border border-orange-100 bg-orange-50 p-5 text-sm text-orange-900">
                  <strong>Responsible AI:</strong> Critical safety information should be supported by trusted sources,
                  freshness information and confidence indicators whenever possible.
                </div>
              </Reveal>
            </div>
          </div>
        </section>

        {/* ============================================================ */}
        {/* WHY SERENDIB AI                                               */}
        {/* ============================================================ */}
        <section className="w-full border-y border-[#EAE2D6] bg-[#FBF3EA] px-[var(--page-x)] py-24">
          <div className="w-full">
            <Reveal className="mb-16 text-center">
              <h2 className="font-display text-4xl font-semibold md:text-6xl">Why choose Serendib AI</h2>
            </Reveal>

            <div className="grid gap-x-12 gap-y-10 md:grid-cols-2 lg:grid-cols-3">
              {BENEFITS.map((b, idx) => (
                <Reveal key={b.title} delay={(idx % 3) * 100} className="flex gap-4">
                  <div className="mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-orange-100">
                    <div className="h-2 w-2 rounded-full bg-orange-500" />
                  </div>
                  <div>
                    <h3 className="mb-2 text-lg font-semibold">{b.title}</h3>
                    <p className="text-sm leading-relaxed text-[#78716C]">{b.desc}</p>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        {/* ============================================================ */}
        {/* FINAL CALL TO ACTION                                          */}
        {/* ============================================================ */}
        <section className="relative w-full overflow-hidden px-[var(--page-x)] py-32 md:py-40">
          <SmartImg
            src={wiki(IMG.sigiriyaRock, 2000)}
            alt="Sigiriya Rock Fortress at dawn"
            className="absolute inset-0 h-full w-full object-cover"
          />
          <div className="absolute inset-0 bg-[#0E1512]/75" />
          <div className="absolute inset-0 bg-gradient-to-t from-[#0E1512] via-transparent to-[#0E1512]/40" />

          <Reveal className="relative z-10 mx-auto flex max-w-3xl flex-col items-center text-center" from="scale">
            <h2 className="font-display mb-6 text-5xl font-semibold leading-[1] text-white md:text-7xl">
              Your Sri Lankan story starts here.
            </h2>
            <p className="mb-10 text-lg text-white/80 md:text-xl">
              Tell Serendib AI what you love, and let intelligent agents help shape the journey.
            </p>
            <div className="flex w-full flex-col gap-4 sm:w-auto sm:flex-row">
              <button
                type="button"
                className="btn-shine relative overflow-hidden rounded-full bg-orange-500 px-8 py-4 text-base font-semibold text-white shadow-lg shadow-orange-500/30 transition-all duration-300 hover:-translate-y-0.5 hover:bg-orange-600"
              >
                Start planning
              </button>
              <Link
                to="/register"
                className="flex items-center justify-center rounded-full border border-white/30 bg-white/10 px-8 py-4 text-base font-semibold text-white backdrop-blur-sm transition-all duration-300 hover:bg-white/20"
              >
                Create account
              </Link>
            </div>
          </Reveal>
        </section>
      </main>

      {/* ============================================================ */}
      {/* FOOTER                                                        */}
      {/* ============================================================ */}
      <footer className="w-full bg-[#0E1512] pb-8 pt-16 text-white">
        <div className="w-full px-[var(--page-x)]">
          <div className="mb-14 grid gap-10 md:grid-cols-[1.3fr_repeat(4,1fr)]">
            <div>
              <span className="mb-4 flex items-center gap-2.5">
                <span className="grid h-9 w-9 place-items-center rounded-lg bg-gradient-to-br from-orange-400 to-orange-600">
                  <Sparkles size={18} className="text-white" />
                </span>
                <span className="font-display text-2xl font-bold">
                  Serendib <span className="text-orange-500">AI</span>
                </span>
              </span>
              <p className="max-w-xs text-sm leading-relaxed text-white/60">
                Intelligent travel planning for discovering Sri Lanka your way.
              </p>
              <div className="mt-6 flex max-w-xs items-center gap-2 rounded-full border border-white/15 bg-white/5 p-1.5 pl-4">
                <input
                  type="email"
                  aria-label="Email address"
                  placeholder="Your email"
                  className="min-w-0 flex-1 bg-transparent text-sm text-white outline-none placeholder:text-white/40"
                />
                <button
                  type="button"
                  className="rounded-full bg-orange-500 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-orange-600"
                >
                  Subscribe
                </button>
              </div>
            </div>

            {FOOTER_COLS.map((col) => (
              <div key={col.title}>
                <h4 className="mb-4 font-semibold text-white">{col.title}</h4>
                <ul className="space-y-3 text-sm text-white/60">
                  {col.links.map((l) => (
                    <li key={l}>
                      <NavAnchor to="#" className="transition-colors hover:text-orange-400">
                        {l}
                      </NavAnchor>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>

          <div className="flex flex-col items-center justify-between gap-4 border-t border-white/10 pt-8 text-center text-xs text-white/50 md:flex-row md:text-left">
            <p>© 2026 Serendib AI. All rights reserved.</p>
            <p>Built for intelligent travel across Sri Lanka.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default Home;