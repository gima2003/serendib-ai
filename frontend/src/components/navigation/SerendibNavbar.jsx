import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import {
  Sparkles,
  Menu,
  X,
  ChevronDown,
  Search,
  Heart,
  Map as MapIcon,
  Globe,
  LogIn,
  UserPlus,
  Check,
  Calendar,
  CalendarDays,
} from "lucide-react";
import { NavAnchor, BASE_MENUS, TRIPS_MENU, QUICK_CITIES, LANGUAGES, upcomingEvents, fmtDateLong } from "../common/Shared";

/* ================================================================== */
/*  SerendibNavbar — the one navigation bar used across the whole site. */
/*  Home.jsx renders <SerendibNavbar isAuth={false} />.                 */
/*  Signed-in pages (dashboard, trip planner, etc.) render               */
/*  <SerendibNavbar isAuth userName={...} onOpenProfile={...} />.        */
/*                                                                       */
/*  Everything here — mega menus, mobile sheet, search, EN selector —    */
/*  is self-contained: mount it once per page and it just works.        */
/* ================================================================== */

/* Small styles the navbar needs wherever it's mounted. Safe to duplicate: */
/* identical rules simply overwrite each other if Home.jsx also has them. */
const NAV_STYLES = `
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

.font-display { font-family: 'Cormorant Garamond', Georgia, 'Times New Roman', serif; }
:root { --page-x: clamp(1.25rem, 3.2vw, 5rem); }

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

a:focus-visible, button:focus-visible, input:focus-visible { outline: 2px solid #F97316; outline-offset: 2px; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.fade-in { animation: fadeIn .5s ease both; }

@keyframes fadeUp { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: none; } }
.fade-up { opacity: 0; animation: fadeUp .8s cubic-bezier(.22,1,.36,1) forwards; }

@keyframes menuIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.menu-in { animation: menuIn .28s ease both; }

@keyframes pulseDot { 0%, 100% { opacity: .55; transform: scale(1); } 50% { opacity: 1; transform: scale(1.35); } }
.pulse-dot { animation: pulseDot 2.2s ease-in-out infinite; }

.btn-shine { isolation: isolate; }
.btn-shine::after {
  content: ""; position: absolute; inset: 0; pointer-events: none; z-index: -1;
  background: linear-gradient(115deg, transparent 30%, rgba(255,255,255,.4) 50%, transparent 70%);
  transform: translateX(-120%); transition: transform .8s ease;
}
.btn-shine:hover::after { transform: translateX(120%); }

@media (prefers-reduced-motion: reduce) {
  .fade-in, .fade-up, .menu-in, .pulse-dot { animation: none; opacity: 1; }
}
`;

/* ------------------------------------------------------------------ */
/*  EN / language selector                                             */
/* ------------------------------------------------------------------ */

function LanguageSelect({ solid, wrapClass }) {
  const [open, setOpen] = useState(false);
  const [lang, setLang] = useState(LANGUAGES[0]);
  const ref = useRef(null);

  useEffect(() => {
    if (!open) return;
    const onDoc = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    const onKey = (e) => e.key === "Escape" && setOpen(false);
    document.addEventListener("mousedown", onDoc);
    window.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onDoc);
      window.removeEventListener("keydown", onKey);
    };
  }, [open]);

  return (
    <div ref={ref} className={`relative ${wrapClass}`}>
      <button
        type="button"
        aria-haspopup="true"
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
        className={`flex h-10 items-center gap-1.5 rounded-full border px-3.5 text-[13px] font-semibold transition-all duration-300 ${
          solid
            ? "border-stone-200 text-stone-700 hover:border-orange-300 hover:bg-orange-50"
            : "border-white/30 text-white hover:bg-white/15"
        }`}
      >
        <Globe size={16} /> {lang.code}
        <ChevronDown size={12} className={`transition-transform duration-300 ${open ? "rotate-180" : ""}`} />
      </button>
      {open && (
        <div className="menu-in absolute right-0 top-[calc(100%+8px)] z-50 w-52 overflow-hidden rounded-2xl border border-stone-200/70 bg-white p-1.5 shadow-[0_20px_50px_-15px_rgba(14,21,18,0.35)]">
          {LANGUAGES.map((l) => (
            <button
              key={l.code}
              type="button"
              onClick={() => {
                setLang(l);
                setOpen(false);
              }}
              className="flex w-full items-center justify-between gap-2 rounded-xl px-3 py-2.5 text-left text-[13.5px] font-medium text-stone-700 transition-colors hover:bg-orange-50 hover:text-orange-600"
            >
              {l.label}
              {l.code === lang.code && <Check size={15} className="text-orange-500" />}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Calendar quick-view — signed-in only. Reuses the same              */
/*  upcomingEvents()/fmtDateLong() the dashboard's Calendar overlay     */
/*  uses, so the two never disagree.                                   */
/* ------------------------------------------------------------------ */

function CalendarQuickView({ solid, onOpenFull }) {
  const [open, setOpen] = useState(false);
  const [now, setNow] = useState(() => new Date());
  const ref = useRef(null);

  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 60000);
    return () => clearInterval(id);
  }, []);

  useEffect(() => {
    if (!open) return;
    const onDoc = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    const onKey = (e) => e.key === "Escape" && setOpen(false);
    document.addEventListener("mousedown", onDoc);
    window.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onDoc);
      window.removeEventListener("keydown", onKey);
    };
  }, [open]);

  const festivals = upcomingEvents(now).slice(0, 3);

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        aria-haspopup="true"
        aria-expanded={open}
        aria-label="Calendar"
        onClick={() => setOpen((v) => !v)}
        className={`relative grid h-10 w-10 place-items-center rounded-full border transition-all duration-300 ${
          solid
            ? "border-stone-200 text-stone-700 hover:border-orange-300 hover:bg-orange-50 hover:text-orange-600"
            : "border-white/30 text-white hover:bg-white/15"
        }`}
      >
        <Calendar size={17} />
        {festivals.length > 0 && (
          <span className="pulse-dot absolute -right-0.5 -top-0.5 h-2 w-2 rounded-full bg-orange-500" />
        )}
      </button>
      {open && (
        <div className="menu-in absolute right-0 top-[calc(100%+8px)] z-50 w-72 overflow-hidden rounded-2xl border border-stone-200/70 bg-white p-4 shadow-[0_20px_50px_-15px_rgba(14,21,18,0.35)]">
          <p className="mb-3 text-[11px] font-semibold uppercase tracking-[0.18em] text-stone-400">
            {fmtDateLong.format(now)}
          </p>
          {festivals.length > 0 ? (
            <ul className="space-y-2">
              {festivals.map((f) => (
                <li key={f.name} className="flex items-center gap-3 rounded-xl p-2 transition-colors hover:bg-orange-50">
                  <span className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-orange-50 text-orange-500">
                    <CalendarDays size={16} />
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="block truncate text-[13.5px] font-semibold text-stone-900">{f.name}</span>
                    <span className="block text-[12px] text-stone-500">
                      {f.label} · {f.days === 0 ? "today" : `in ${f.days} days`}
                    </span>
                  </span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="py-3 text-center text-[13px] text-stone-500">No upcoming festivals scheduled.</p>
          )}
          <button
            type="button"
            onClick={() => {
              setOpen(false);
              onOpenFull?.();
            }}
            className="mt-3 w-full rounded-xl border-t border-stone-100 pt-3 text-center text-[13px] font-bold uppercase tracking-wider text-emerald-900 transition-colors hover:text-orange-600"
          >
            View full calendar
          </button>
        </div>
      )}
    </div>
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
/*  Navbar                                                              */
/* ------------------------------------------------------------------ */

export function SerendibNavbar({ isAuth = false, userName = "Traveller", onOpenProfile, onOpenCalendar }) {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(null); // { key, left, width, caret }
  const [animatePos, setAnimatePos] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [mobileSection, setMobileSection] = useState(null);
  const [searchOpen, setSearchOpen] = useState(false);
  const closeTimer = useRef(null);
  const barRef = useRef(null);

  const MENUS = isAuth ? [...BASE_MENUS, TRIPS_MENU] : BASE_MENUS;

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
  const solid = scrolled || open || mobileOpen || isAuth;

  const iconBtn = `grid h-10 w-10 place-items-center rounded-full border transition-all duration-300 ${
    solid
      ? "border-stone-200 text-stone-700 hover:border-orange-300 hover:bg-orange-50 hover:text-orange-600"
      : "border-white/30 text-white hover:bg-white/15"
  }`;

  const initial = (userName || "T").trim().charAt(0).toUpperCase();

  return (
    <>
      <style>{NAV_STYLES}</style>

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

        {/* Utility bar (hidden once signed in — the dashboard has its own context) */}
        {!isAuth && (
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
        )}

        {/* Main bar */}
        <div
          className={`flex w-full items-center justify-between gap-6 px-[var(--page-x)] transition-[padding] duration-300 ${
            scrolled || isAuth ? "py-3" : "py-4"
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
            <button type="button" aria-label="Search" onClick={() => setSearchOpen(true)} className={iconBtn}>
              <Search size={17} />
            </button>
            <button type="button" aria-label="Saved places" className={`${iconBtn} nav-2xl-grid`}>
              <Heart size={17} />
            </button>
            <button type="button" aria-label="Map" className={`${iconBtn} nav-2xl-grid`}>
              <MapIcon size={17} />
            </button>

            <LanguageSelect solid={solid} wrapClass="nav-xl-flex" />

            {isAuth && <CalendarQuickView solid={solid} onOpenFull={onOpenCalendar} />}

            <span aria-hidden className={`mx-2 h-6 w-px ${solid ? "bg-stone-200" : "bg-white/25"}`} />

            {isAuth ? (
              <button
                type="button"
                onClick={onOpenProfile}
                aria-label="Open profile"
                className="group flex items-center gap-2.5 rounded-full border border-stone-200 py-1.5 pl-1.5 pr-4 text-sm font-semibold text-stone-800 transition-all duration-300 hover:-translate-y-0.5 hover:border-orange-300 hover:bg-orange-50 hover:shadow-[0_10px_25px_-12px_rgba(249,115,22,0.5)]"
              >
                <span className="grid h-8 w-8 place-items-center rounded-full bg-gradient-to-br from-orange-400 to-orange-600 text-[13px] font-bold text-white shadow-sm">
                  {initial}
                </span>
                <span className="max-w-[110px] truncate">{userName}</span>
              </button>
            ) : (
              <>
                <Link
                  to="/login"
                  className={`inline-flex items-center gap-2 whitespace-nowrap rounded-full px-4 py-2.5 text-sm font-semibold transition-all duration-300 ${
                    solid ? "text-stone-800 hover:bg-stone-100" : "text-white hover:bg-white/15"
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
              </>
            )}
          </div>

          {/* Mobile toggle */}
          <div className="nav-m-flex items-center gap-2">
            <button type="button" aria-label="Search" onClick={() => setSearchOpen(true)} className={iconBtn}>
              <Search size={17} />
            </button>
            {isAuth && <CalendarQuickView solid={solid} onOpenFull={onOpenCalendar} />}
            {isAuth && (
              <button type="button" aria-label="Open profile" onClick={onOpenProfile} className={iconBtn}>
                <span className="grid h-6 w-6 place-items-center rounded-full bg-gradient-to-br from-orange-400 to-orange-600 text-[11px] font-bold text-white">
                  {initial}
                </span>
              </button>
            )}
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

            <div className="my-4 flex items-center justify-between border-t border-stone-100 pt-4">
              <span className="text-[13px] font-semibold uppercase tracking-wider text-stone-500">Language</span>
              <LanguageSelect solid wrapClass="" />
            </div>

            {isAuth ? (
              <button
                type="button"
                onClick={onOpenProfile}
                className="flex w-full items-center justify-center gap-2 rounded-full bg-gradient-to-r from-orange-500 to-amber-500 py-3 text-[15px] font-semibold text-white"
              >
                <span className="grid h-6 w-6 place-items-center rounded-full bg-white/25 text-[12px] font-bold">{initial}</span>
                View Profile
              </button>
            ) : (
              <div className="grid grid-cols-2 gap-3">
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
            )}
          </div>
        )}
      </header>

      <SearchModal open={searchOpen} onClose={() => setSearchOpen(false)} />
    </>
  );
}

export default SerendibNavbar;