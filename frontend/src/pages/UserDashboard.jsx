import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Map, Calendar, Wallet, ArrowRight, Compass,
  LogOut, Sun,
  Navigation, Info, Utensils, Home as HomeIcon, MapPin, Search, Banknote,
  Sparkles, Droplets, Wind
} from 'lucide-react';
import { authService } from '../services/authService';
import { tripService } from '../services/tripService';
import { profileService } from '../services/profileService';
import toast from 'react-hot-toast';
import Overlay from '../components/Overlay';
import { SerendibNavbar } from '../components/navigation/SerendibNavbar';
import { IMG, wiki, fmtDateLong, upcomingEvents, SmartImg } from '../components/common/Shared';
import { useDynamicHero } from '../hooks/useDynamicHero';
import { useSriLankaWeather, useColomboClock, fmtTime, wmo } from '../hooks/useSriLankaWeather';
import { getCountries, getCurrencies } from '../data/countries';

const getDisplayCountry = (code) => {
  if (!code) return '';
  const countries = getCountries();
  const found = countries.find(c => c.code === code || c.code.toLowerCase() === code.toLowerCase() || c.name.toLowerCase() === code.toLowerCase());
  if (found) return found.name;
  
  // If not found in the list, try to title-case if it's all uppercase
  if (code === code.toUpperCase() && code.length > 2) {
    return code.charAt(0).toUpperCase() + code.slice(1).toLowerCase();
  }
  return code;
};

/* Small styles this page needs on top of the shared navbar styles       */
/* (SerendibNavbar already injects the fade-in / font-display / page-x   */
/* rules, so this only adds the hero zoom, the crossfade, the page's     */
/* subtle background wash, and the hover-glow utilities).                */
const DASHBOARD_STYLES = `
@keyframes dashKenburns { from { transform: scale(1); } to { transform: scale(1.05); } }
.dash-hero-img { animation: dashKenburns 14s ease-out forwards; }

@keyframes heroFadeIn { from { opacity: 0; } to { opacity: 1; } }
.hero-fade-in { animation: heroFadeIn 2s cubic-bezier(0.22, 1, 0.36, 1) forwards; }

@keyframes heroFadeOut { from { opacity: 1; } to { opacity: 0; } }
.hero-fade-out { animation: heroFadeOut 2s cubic-bezier(0.22, 1, 0.36, 1) forwards; }

/* Quick Access + trip/recommendation cards: a warm glow that blends the
   dashboard's two brand colors — orange (primary) and the hero's deep
   green (echo) — instead of a flat single-tone orange shadow. */
.glow-card, .glow-btn {
  position: relative;
  isolation: isolate;
  transition: transform .35s cubic-bezier(.22,1,.36,1), box-shadow .35s cubic-bezier(.22,1,.36,1),
              border-color .35s ease, background-color .35s ease;
}
.glow-card::before, .glow-btn::before {
  content: ""; position: absolute; inset: -1px; z-index: -1; border-radius: inherit;
  background: radial-gradient(120px 90px at 50% 0%, rgba(249,115,22,0.16), transparent 70%);
  opacity: 0; transition: opacity .35s ease;
}
.glow-card:hover, .glow-btn:hover {
  transform: translateY(-3px);
  border-color: rgba(249,115,22,0.35);
  background-color: rgba(255,247,237,0.6);
  box-shadow:
    0 20px 45px -20px rgba(249,115,22,0.5),
    0 10px 24px -14px rgba(6,78,59,0.18);
}
.glow-card:hover::before, .glow-btn:hover::before { opacity: 1; }
.glow-btn:active { transform: translateY(-1px); }

/* Icon roundel inside a Quick Access tile gets its own soft ring on hover */
.glow-card:hover .glow-icon, .glow-btn:hover .glow-icon {
  box-shadow: 0 0 0 6px rgba(251,146,60,0.16);
}

@media (prefers-reduced-motion: reduce) {
  .dash-hero-img { animation: none; }
  .hero-fade-in { animation: none; opacity: 1; }
  .hero-fade-out { animation: none; opacity: 0; }
  .glow-card, .glow-btn { transition: none; }
  .glow-card:hover, .glow-btn:hover { transform: none; }
}

@keyframes pulseDot { 0%, 100% { opacity: .55; transform: scale(1); } 50% { opacity: 1; transform: scale(1.35); } }
.pulse-dot { animation: pulseDot 2.2s ease-in-out infinite; }

.btn-shine { isolation: isolate; }
.btn-shine::after {
  content: ""; position: absolute; inset: 0; pointer-events: none; z-index: -1;
  background: linear-gradient(115deg, transparent 30%, rgba(255,255,255,.4) 50%, transparent 70%);
  transform: translateX(-120%); transition: transform .8s ease;
}
.btn-shine:hover::after { transform: translateX(120%); }
`;

export default function UserDashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(authService.getCurrentUser());
  const [activeOverlay, setActiveOverlay] = useState(null);
  
  // Profile form state
  const [formData, setFormData] = useState({
    full_name: user?.full_name || user?.name || '',
    country_code: user?.country_code || '',
    preferred_currency: user?.preferred_currency || ''
  });
  const [isSaving, setIsSaving] = useState(false);

  // Data state (prepared for future API)
  const [currentTrip, setCurrentTrip] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [isLoadingTrip, setIsLoadingTrip] = useState(true);
  const [isLoadingRecs, setIsLoadingRecs] = useState(true);

  useEffect(() => {
    const currentUser = authService.getCurrentUser();
    if (!currentUser) {
      navigate('/login');
      return;
    }

    const fetchProfileData = async () => {
      try {
        const profile = await profileService.getProfile();
        if (profile) {
          const updatedUser = { ...currentUser, ...profile };
          localStorage.setItem('user', JSON.stringify(updatedUser));
          setUser(updatedUser);
          setFormData({
            full_name: profile.full_name || profile.name || '',
            country_code: profile.country_code || '',
            preferred_currency: profile.preferred_currency || ''
          });
        }
      } catch (error) {
        console.error('Failed to fetch profile:', error);
      }
    };

    const fetchDashboardData = async () => {
      try {
        setIsLoadingTrip(true);
        const trip = await tripService.getCurrentTrip();
        setCurrentTrip(trip);
      } catch (error) {
        console.error('Failed to fetch trip:', error);
      } finally {
        setIsLoadingTrip(false);
      }

      try {
        setIsLoadingRecs(true);
        const recs = await tripService.getRecommendations();
        setRecommendations(recs);
      } catch (error) {
        console.error('Failed to fetch recommendations:', error);
      } finally {
        setIsLoadingRecs(false);
      }
    };

    fetchProfileData();
    fetchDashboardData();
  }, [navigate]);

  const handleLogout = () => {
    authService.logout();
    navigate('/');
  };

  const handleSaveChanges = async () => {
    try {
      setIsSaving(true);
      const updatedProfile = await profileService.updateProfile(formData);
      
      if (updatedProfile) {
        const newUser = { ...user, ...updatedProfile };
        localStorage.setItem('user', JSON.stringify(newUser));
        setUser(newUser);
        toast.success('Profile updated');
        closeOverlay(newUser);
      }
    } catch (error) {
      toast.error(error.message || 'Failed to update profile');
    } finally {
      setIsSaving(false);
    }
  };



  const userName = user?.full_name || user?.name || '';
  const userEmail = user?.email || '';

  const lastLoginDate = user?.last_login || user?.updated_at || user?.created_at;
  const formattedLastLogin = lastLoginDate
    ? new Date(lastLoginDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
    : new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });

  const closeOverlay = (latestUser = user) => {
    setActiveOverlay(null);
    // Reset form data on close to drop unsaved changes
    setFormData({
      full_name: latestUser?.full_name || latestUser?.name || '',
      country_code: latestUser?.country_code || '',
      preferred_currency: latestUser?.preferred_currency || ''
    });
  };

  const { current: heroSlide, previous: prevSlide, slides: heroSlides } = useDynamicHero();
  const weatherData = useSriLankaWeather(['Colombo', heroSlide.city]);
  const colomboWeather = weatherData['Colombo'];
  const activeWeather = weatherData[heroSlide.city] || colomboWeather;
  const now = useColomboClock();
  const formattedTime = fmtTime.format(now);
  const festivals = upcomingEvents(now);
  const WeatherIcon = activeWeather ? wmo(activeWeather.code).icon : Sun;

  const renderProfileContent = () => (
    <div className="space-y-6">
      <div className="flex items-center gap-4 mb-6 p-4 bg-[#FBF3EA] rounded-xl border border-[#EAE2D6]">
        <div className="w-14 h-14 bg-orange-500 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-[0_0_15px_rgba(249,115,22,0.3)]">
          {userName.charAt(0)}
        </div>
        <div>
          <p className="font-semibold text-[#1C1917] text-lg">{userName}</p>
          <p className="text-sm text-[#78716C]">Last Login: {formattedLastLogin}</p>
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-[#78716C] mb-1">Email Address</label>
          <input
            type="email"
            value={userEmail}
            disabled
            className="w-full px-4 py-3 text-sm bg-white border border-[#EAE2D6] rounded-xl text-[#57534E] cursor-not-allowed"
          />
          <p className="text-xs text-[#78716C] mt-1">This email cannot be changed.</p>
        </div>
        <div>
          <label className="block text-sm font-medium text-[#78716C] mb-1">Full Name</label>
          <input
            type="text"
            value={formData.full_name}
            onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
            className="w-full px-4 py-3 text-sm bg-white border border-[#EAE2D6] rounded-xl text-[#1C1917] focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition-all shadow-sm"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-[#78716C] mb-1">Country</label>
          <input
            type="text"
            value={getDisplayCountry(formData.country_code)}
            onChange={(e) => setFormData({ ...formData, country_code: e.target.value })}
            className="w-full px-4 py-3 text-sm bg-white border border-[#EAE2D6] rounded-xl text-[#1C1917] focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition-all shadow-sm"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-[#78716C] mb-1">Preferred Currency</label>
          <select
            value={formData.preferred_currency}
            onChange={(e) => setFormData({ ...formData, preferred_currency: e.target.value })}
            className="w-full px-4 py-3 text-sm bg-white border border-[#EAE2D6] rounded-xl text-[#1C1917] focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition-all shadow-sm"
          >
            {getCurrencies().map(c => (
              <option key={c.code} value={c.code}>{c.code}</option>
            ))}
            {/* Fallback in case user's currency is somehow not in the list */}
            {formData.preferred_currency && !getCurrencies().some(c => c.code === formData.preferred_currency) && (
              <option value={formData.preferred_currency}>{formData.preferred_currency}</option>
            )}
          </select>
        </div>
      </div>

      <div className="mt-8 pt-6 border-t border-[#EAE2D6] flex flex-col gap-3">
        <button
          onClick={handleSaveChanges}
          disabled={isSaving}
          className="w-full bg-orange-500 text-white font-medium py-3 rounded-xl hover:bg-orange-600 transition-colors shadow-sm disabled:opacity-50"
        >
          {isSaving ? 'Saving...' : 'Save Changes'}
        </button>
        <button
          onClick={handleLogout}
          className="w-full flex items-center justify-center gap-2 text-red-600 font-medium py-3 hover:bg-red-50 rounded-xl transition-colors"
        >
          <LogOut size={18} /> Logout
        </button>
      </div>
    </div>
  );

  return (
    <div className="relative min-h-screen bg-gradient-to-b from-[#FFFCF8] via-[#FFFCF8] to-[#FBF3EA] text-[#1C1917] font-sans overflow-x-hidden selection:bg-orange-100">
      <style>{DASHBOARD_STYLES}</style>

      {/* Very soft brand-colour wash behind the page — depth without noise */}
      <div aria-hidden className="pointer-events-none fixed inset-0 z-0 overflow-hidden">
        <div className="absolute -top-40 right-[-10%] h-[520px] w-[520px] rounded-full bg-orange-200/25 blur-[140px]" />
        <div className="absolute top-[38vh] -left-40 h-[420px] w-[420px] rounded-full bg-emerald-900/[0.05] blur-[140px]" />
      </div>

      {/* Top Navigation — identical component/behaviour to the Home page navbar */}
      <SerendibNavbar
        isAuth
        userName={userName}
        onOpenProfile={() => setActiveOverlay('profile')}
        onOpenCalendar={() => setActiveOverlay('calendar')}
      />

      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 pt-24 pb-8 md:pt-28 md:pb-12 space-y-12">

        {/* Welcome Section */}
        <section className="relative overflow-hidden rounded-3xl bg-[#0E1512] shadow-md grid grid-cols-1 md:grid-cols-[minmax(0,1fr)_minmax(300px,360px)] min-h-[400px]">

          {/* Dynamic hero image — true crossfade: the incoming photo (already
              confirmed loaded by useDynamicHero before it's ever shown) fades
              in on top of the still-fully-opaque outgoing one, so there is
              never a frame with no image underneath. SmartImg swaps in a
              themed gradient instead of a broken-image icon if a photo ever
              fails to load, so a network hiccup can't show an empty frame. */}
          {heroSlides.map((slide) => {
            const isCurrent = slide.img === heroSlide.img;
            const isPrev = prevSlide && slide.img === prevSlide.img;
            if (!isCurrent && !isPrev) return null;

            // On first paint (no prevSlide yet) just show the image — nothing to fade from.
            const fadeClass = isCurrent
              ? (prevSlide ? 'hero-fade-in' : 'opacity-100')
              : 'hero-fade-out';

            return (
              <div
                key={slide.img}
                className={`absolute inset-0 ${fadeClass} ${isCurrent ? 'z-10' : 'z-0'}`}
              >
                <SmartImg
                  src={slide.img}
                  alt="Sri Lanka landscape"
                  eager={isCurrent && !prevSlide}
                  className="dash-hero-img w-full h-full object-cover"
                  style={{ objectPosition: slide.align, filter: 'brightness(1.12) saturate(1.12) contrast(1.02)' }}
                />
              </div>
            );
          })}
          <div className="absolute inset-0 bg-gradient-to-r from-[#0E1512]/70 via-[#0E1512]/30 to-transparent z-20" />
          <div className="absolute inset-0 bg-gradient-to-t from-[#0E1512]/40 via-transparent to-transparent z-20" />
          <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-orange-500/25 rounded-full blur-[100px] pointer-events-none z-20" />

          <div className="relative z-30 p-8 md:p-12 flex flex-col justify-center">
            <p className="text-orange-400 font-semibold mb-2">{formattedTime} &middot; Colombo, Sri Lanka</p>
            <h1 className="text-3xl md:text-5xl font-bold text-white mb-3 tracking-tight font-serif drop-shadow-[0_2px_12px_rgba(0,0,0,0.35)]">
              Good {formattedTime.includes('AM') ? 'morning' : 'evening'}, {userName}
            </h1>
            <p className="text-lg md:text-xl text-stone-200 mb-8 font-light drop-shadow-[0_1px_8px_rgba(0,0,0,0.3)]">
              Ready to explore Sri Lanka?
            </p>

            <div className="flex flex-wrap items-center gap-4">
              <Link to="/plan-trip" className="glow-btn bg-orange-500 text-white px-8 py-3.5 rounded-xl font-semibold shadow-md hover:bg-orange-600 transition-all flex items-center gap-2">
                + Plan a New Trip
              </Link>
              <Link to="/explore" className="glow-btn bg-white/10 text-white border border-white/20 px-8 py-3.5 rounded-xl font-semibold hover:bg-white/20 transition-all backdrop-blur-sm">
                Explore Destinations
              </Link>
            </div>
          </div>

          <aside className="relative z-30 w-full border-t md:border-t-0 md:border-l border-white/10 p-6 flex flex-col gap-2.5 backdrop-blur-sm bg-black/10" aria-label="Quick tools">
            {/* Weather Card */}
            <div className="rounded-2xl border border-white/10 bg-[#141a17]/60 p-4 text-white backdrop-blur-xl">
              <div className="flex items-center justify-between text-[11px] font-semibold uppercase tracking-[0.16em] text-white/50">
                <span>Weather in {activeWeather ? heroSlide.city : 'Sri Lanka'}</span>
                <span className="flex items-center gap-1.5 normal-case tracking-normal text-emerald-300">
                  <span className="pulse-dot h-1.5 w-1.5 rounded-full bg-emerald-400" /> Live
                </span>
              </div>
              <div className="fade-in mt-3 flex items-end justify-between">
                <div className="flex items-center gap-3.5">
                  <WeatherIcon size={34} className="text-orange-300" strokeWidth={1.6} />
                  <div>
                    <p className="text-[32px] font-semibold leading-none">
                      {activeWeather?.temp ? Math.round(activeWeather.temp) : '--'}°C
                      {activeWeather && <span className="ml-2 text-xs font-normal text-white/60">feels {Math.round(activeWeather.feels)}°</span>}
                    </p>
                    <p className="mt-1.5 text-[13px] text-white/70">{activeWeather ? wmo(activeWeather.code).label : 'Weather unavailable'}</p>
                  </div>
                </div>
                <div className="space-y-1.5 text-right text-xs text-white/70">
                  <p className="flex items-center justify-end gap-1.5">
                    <Droplets size={13} /> {activeWeather?.humidity ? Math.round(activeWeather.humidity) : '--'}%
                  </p>
                  <p className="flex items-center justify-end gap-1.5">
                    <Wind size={13} /> {activeWeather?.wind ? Math.round(activeWeather.wind) : '--'} km/h
                  </p>
                </div>
              </div>
            </div>

            <Link
              to="/plan-trip"
              className="btn-shine relative flex items-center justify-center gap-2.5 overflow-hidden rounded-2xl bg-gradient-to-r from-orange-500 to-amber-500 px-4 py-4 text-[12px] font-bold uppercase tracking-[0.12em] text-white shadow-lg shadow-orange-500/25 transition-all duration-300 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-orange-500/35"
            >
              <Sparkles size={17} /> Build your itinerary
            </Link>

            <div className="grid grid-cols-2 gap-2.5">
              <button type="button" className="group flex items-center justify-center gap-2.5 rounded-2xl border border-white/10 bg-[#141a17]/60 px-4 py-3.5 text-[12px] font-bold uppercase tracking-[0.12em] text-white backdrop-blur-xl transition-all duration-300 hover:-translate-y-0.5 hover:border-orange-400/50 hover:bg-[#1b231f]/80">
                <Wallet size={17} className="text-orange-300" /> Trip budget
              </button>
              <button type="button" className="group flex items-center justify-center gap-2.5 rounded-2xl border border-white/10 bg-[#141a17]/60 px-4 py-3.5 text-[12px] font-bold uppercase tracking-[0.12em] text-white backdrop-blur-xl transition-all duration-300 hover:-translate-y-0.5 hover:border-orange-400/50 hover:bg-[#1b231f]/80">
                <Banknote size={17} className="text-orange-300" /> Currency
              </button>
            </div>

            {festivals[0] && (
              <button type="button" className="group flex items-center gap-3.5 rounded-2xl border border-white/10 bg-[#141a17]/60 p-4 text-left text-white backdrop-blur-xl transition-all duration-300 hover:-translate-y-0.5 hover:border-orange-400/50">
                <span className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-orange-500/20 text-orange-300">
                  <Calendar size={20} />
                </span>
                <span className="min-w-0 flex-1">
                  <span className="block text-[11px] font-semibold text-amber-300">Next festival</span>
                  <span className="block truncate text-[15px] font-semibold">{festivals[0].name}</span>
                  <span className="block text-[12px] text-white/60">
                    {festivals[0].label} · {festivals[0].days === 0 ? "today" : `in ${festivals[0].days} days`}
                  </span>
                </span>
                <ArrowRight size={16} className="text-white/50 transition-transform group-hover:translate-x-1" />
              </button>
            )}
          </aside>
        </section>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">

          {/* Main Content Column */}
          <div className="lg:col-span-8 space-y-8">

            {/* Upcoming / Current Trip Card */}
            <section>
              <div className="flex justify-between items-end mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-[#1C1917] tracking-tight">Your Journey</h2>
                  <p className="text-[#78716C] text-sm mt-1">Current and upcoming travel plans</p>
                </div>
                <Link to="/my-trips" className="text-sm font-medium text-orange-600 hover:text-orange-700 transition-colors hidden sm:block">
                  View All Trips &rarr;
                </Link>
              </div>

              {isLoadingTrip ? (
                <div className="bg-white border border-[#EAE2D6] rounded-3xl p-8 flex flex-col items-center justify-center min-h-[250px] animate-pulse shadow-sm">
                  <div className="w-12 h-12 border-4 border-[#EAE2D6] border-t-orange-500 rounded-full animate-spin mb-4"></div>
                  <p className="text-[#78716C]">Loading your journey...</p>
                </div>
              ) : currentTrip ? (
                <div className="glow-card bg-white border border-[#EAE2D6] rounded-3xl p-6 md:p-8 relative overflow-hidden group shadow-sm">
                  <div className="flex flex-col md:flex-row gap-8 relative z-10">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-4">
                        <span className="bg-orange-50 text-orange-600 text-xs font-bold px-3 py-1 rounded-full border border-orange-100">Upcoming</span>
                        <span className="text-sm font-medium text-[#57534E]">{currentTrip.days} Days • {currentTrip.travellerType}</span>
                      </div>
                      <h3 className="text-2xl md:text-3xl font-bold text-[#1C1917] mb-2">{currentTrip.title}</h3>
                      <p className="text-[#78716C] mb-6 flex items-center gap-2">
                        <Calendar size={16} /> {currentTrip.dates}
                      </p>

                      <div className="bg-[#FBF3EA] rounded-2xl p-4 mb-6 border border-[#EAE2D6]">
                        <p className="text-xs text-[#78716C] mb-2 font-medium uppercase tracking-wider">Route Summary</p>
                        <p className="text-[#1C1917] font-medium">{currentTrip.routeSummary}</p>
                      </div>

                      <div className="flex items-center gap-4">
                        <Link to={`/trip/${currentTrip.id}`} className="bg-white hover:bg-[#FBF3EA] border border-[#EAE2D6] text-[#1C1917] px-6 py-2.5 rounded-xl font-medium transition-all shadow-sm">
                          View Trip
                        </Link>
                        <Link to={`/plan-trip/${currentTrip.id}`} className="text-orange-600 font-medium hover:text-orange-700 transition-colors">
                          Continue Planning
                        </Link>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="bg-white border border-[#EAE2D6] rounded-3xl p-10 flex flex-col items-center justify-center text-center min-h-[250px] shadow-sm">
                  <div className="w-16 h-16 bg-[#FBF3EA] rounded-full flex items-center justify-center text-orange-400 mb-4">
                    <Map size={32} />
                  </div>
                  <h3 className="text-xl font-bold text-[#1C1917] mb-2">No upcoming journey yet</h3>
                  <p className="text-[#78716C] mb-6 max-w-md">Start planning your Sri Lankan adventure with our AI travel assistant.</p>
                  <Link to="/plan-trip" className="glow-btn bg-orange-500 text-white px-6 py-2.5 rounded-xl font-medium shadow-sm hover:bg-orange-600 transition-all">
                    Plan a Trip
                  </Link>
                </div>
              )}
            </section>

            {/* Recommended for You */}
            <section>
              <div className="flex justify-between items-end mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-[#1C1917] tracking-tight">Recommended for You</h2>
                  <p className="text-[#78716C] text-sm mt-1">Curated destinations based on your style</p>
                </div>
              </div>

              {isLoadingRecs ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {[1, 2].map(i => (
                    <div key={i} className="bg-white border border-[#EAE2D6] rounded-2xl h-[280px] animate-pulse shadow-sm"></div>
                  ))}
                </div>
              ) : recommendations.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {recommendations.map((rec, index) => (
                    <div key={index} className="glow-card bg-white border border-[#EAE2D6] rounded-2xl overflow-hidden group cursor-pointer flex flex-col shadow-sm">
                      <div className="h-40 bg-[#FBF3EA] overflow-hidden relative">
                        {rec.image && <img src={rec.image} alt={rec.name} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />}
                        {rec.matchScore && (
                          <div className="absolute top-3 right-3 bg-white/90 backdrop-blur-md px-2.5 py-1 rounded-lg border border-[#EAE2D6] flex items-center gap-1.5 shadow-sm">
                            <span className="w-1.5 h-1.5 bg-orange-500 rounded-full"></span>
                            <span className="text-xs font-bold text-[#1C1917]">{rec.matchScore}% Match</span>
                          </div>
                        )}
                      </div>
                      <div className="p-5 flex-1 flex flex-col">
                        <div className="flex justify-between items-start mb-2">
                          <h3 className="text-lg font-bold text-[#1C1917]">{rec.name}</h3>
                          <span className="text-xs font-medium text-[#78716C] bg-[#FBF3EA] px-2 py-1 rounded-md">{rec.category}</span>
                        </div>
                        <p className="text-sm text-[#57534E] mt-auto line-clamp-2">{rec.reason}</p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="bg-white border border-[#EAE2D6] rounded-2xl p-8 text-center flex flex-col items-center justify-center shadow-sm">
                  <div className="w-14 h-14 bg-[#FBF3EA] rounded-full flex items-center justify-center text-[#78716C] mb-4">
                    <Search size={24} />
                  </div>
                  <h3 className="text-lg font-bold text-[#1C1917] mb-2">No recommendations yet</h3>
                  <p className="text-[#78716C]">Complete your profile to get personalized recommendations.</p>
                </div>
              )}
            </section>
          </div>

          {/* Sidebar / Quick Access Column */}
          <div className="lg:col-span-4 space-y-6">
            <h2 className="text-xl font-bold text-[#1C1917] mb-2">Quick Access</h2>

            <div className="grid grid-cols-2 gap-4">
              <button onClick={() => setActiveOverlay('budget')} className="glow-btn bg-white border border-[#EAE2D6] p-4 rounded-2xl flex flex-col items-center justify-center gap-3 group">
                <div className="glow-icon w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
                  <Wallet size={22} />
                </div>
                <span className="text-sm font-medium text-[#57534E] group-hover:text-orange-700">Budget</span>
              </button>

              <button onClick={() => setActiveOverlay('weather')} className="glow-btn bg-white border border-[#EAE2D6] p-4 rounded-2xl flex flex-col items-center justify-center gap-3 group">
                <div className="glow-icon w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
                  <Sun size={22} />
                </div>
                <span className="text-sm font-medium text-[#57534E] group-hover:text-orange-700">Weather</span>
              </button>

              <button onClick={() => setActiveOverlay('route')} className="glow-btn bg-white border border-[#EAE2D6] p-4 rounded-2xl flex flex-col items-center justify-center gap-3 group">
                <div className="glow-icon w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
                  <Navigation size={22} />
                </div>
                <span className="text-sm font-medium text-[#57534E] group-hover:text-orange-700">Route</span>
              </button>

              <button onClick={() => setActiveOverlay('travel-info')} className="glow-btn bg-white border border-[#EAE2D6] p-4 rounded-2xl flex flex-col items-center justify-center gap-3 group">
                <div className="glow-icon w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
                  <Info size={22} />
                </div>
                <span className="text-sm font-medium text-[#57534E] group-hover:text-orange-700">Travel Info</span>
              </button>

              <button onClick={() => setActiveOverlay('food')} className="glow-btn bg-white border border-[#EAE2D6] p-4 rounded-2xl flex flex-col items-center justify-center gap-3 group">
                <div className="glow-icon w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
                  <Utensils size={22} />
                </div>
                <span className="text-sm font-medium text-[#57534E] group-hover:text-orange-700">Food</span>
              </button>

              <button onClick={() => setActiveOverlay('accommodation')} className="glow-btn bg-white border border-[#EAE2D6] p-4 rounded-2xl flex flex-col items-center justify-center gap-3 group">
                <div className="glow-icon w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
                  <HomeIcon size={22} />
                </div>
                <span className="text-sm font-medium text-[#57534E] group-hover:text-orange-700">Stays</span>
              </button>

              <button onClick={() => setActiveOverlay('calendar')} className="glow-btn bg-white border border-[#EAE2D6] p-4 rounded-2xl flex flex-col items-center justify-center gap-3 group relative">
                {festivals.length > 0 && (
                  <span className="absolute top-3 right-3 h-2 w-2 rounded-full bg-orange-500" />
                )}
                <div className="glow-icon w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
                  <Calendar size={22} />
                </div>
                <span className="text-sm font-medium text-[#57534E] group-hover:text-orange-700">Calendar</span>
              </button>

              <button onClick={() => setActiveOverlay('currency')} className="glow-btn bg-white border border-[#EAE2D6] p-4 rounded-2xl flex flex-col items-center justify-center gap-3 group">
                <div className="glow-icon w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
                  <Banknote size={22} />
                </div>
                <span className="text-sm font-medium text-[#57534E] group-hover:text-orange-700">Currency</span>
              </button>
            </div>

            {/* Visit Sri Lanka promo card */}
            <a
              href="#explore"
              onClick={(e) => e.preventDefault()}
              className="glow-card group relative block h-40 overflow-hidden rounded-2xl border border-[#EAE2D6] shadow-sm"
            >
              <img
                src={wiki(IMG.sigiriyaRock, 700)}
                alt="Sigiriya Rock Fortress, Sri Lanka"
                className="absolute inset-0 h-full w-full object-cover transition-transform duration-700 group-hover:scale-110"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-emerald-950/90 via-emerald-950/30 to-transparent" />
              <div className="relative z-10 flex h-full flex-col justify-end p-5 text-white">
                <span className="mb-1 inline-flex w-fit items-center gap-1.5 rounded-full bg-white/15 px-2.5 py-1 text-[11px] font-semibold backdrop-blur">
                  <Compass size={12} className="text-orange-300" /> Sri Lanka Tourism
                </span>
                <p className="font-serif text-xl font-bold leading-tight">Visit Sri Lanka</p>
                <p className="mt-1 flex items-center gap-1 text-[13px] text-white/75">
                  Discover the official guide <ArrowRight size={13} className="transition-transform group-hover:translate-x-1" />
                </p>
              </div>
            </a>
          </div>
        </div>
      </main>

      {/* OVERLAYS — all open centered with a fade + scale animation */}

      {/* Profile Drawer */}
      <Overlay isOpen={activeOverlay === 'profile'} onClose={closeOverlay} title="Traveller Profile" type="wide-modal">
        {renderProfileContent()}
      </Overlay>

      {/* Budget Modal */}
      <Overlay isOpen={activeOverlay === 'budget'} onClose={closeOverlay} title="Current Trip Budget">
        <div className="space-y-6">
          <div className="bg-white p-5 rounded-xl border border-[#EAE2D6] text-center shadow-sm">
            <p className="text-[#78716C] text-sm mb-1">Total Estimated Budget</p>
            <p className="text-3xl font-bold text-[#1C1917]">LKR 0.00</p>
          </div>
          <div className="flex flex-col items-center justify-center py-8 text-[#78716C]">
            <Wallet size={40} className="mb-4 opacity-30 text-[#1C1917]" />
            <p>Connect a trip to see budget details.</p>
          </div>
        </div>
      </Overlay>

      {/* Weather Modal — shows the same live Colombo reading as the hero card */}
      <Overlay isOpen={activeOverlay === 'weather'} onClose={closeOverlay} title="Local Weather">
        <div className="space-y-5">
          <div className="flex items-center justify-between rounded-2xl border border-[#EAE2D6] bg-[#FBF3EA] p-5">
            <div className="flex items-center gap-4">
              <WeatherIcon size={40} className="text-orange-500" strokeWidth={1.6} />
              <div>
                <p className="text-3xl font-bold text-[#1C1917]">
                  {colomboWeather?.temp ? Math.round(colomboWeather.temp) : '--'}&deg;C
                </p>
                <p className="text-sm text-[#78716C]">{colomboWeather ? wmo(colomboWeather.code).label : 'Loading…'}</p>
              </div>
            </div>
            <span className="flex items-center gap-1.5 rounded-full bg-emerald-100 px-2.5 py-1 text-[11px] font-semibold text-emerald-700">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" /> Live · Colombo
            </span>
          </div>
          <div className="grid grid-cols-2 gap-3 text-center">
            <div className="rounded-xl border border-[#EAE2D6] p-4">
              <p className="text-xs text-[#78716C]">Feels like</p>
              <p className="text-lg font-semibold text-[#1C1917]">{colomboWeather?.feels ? Math.round(colomboWeather.feels) : '--'}&deg;</p>
            </div>
            <div className="rounded-xl border border-[#EAE2D6] p-4">
              <p className="text-xs text-[#78716C]">Humidity</p>
              <p className="text-lg font-semibold text-[#1C1917]">{colomboWeather?.humidity ? Math.round(colomboWeather.humidity) : '--'}%</p>
            </div>
          </div>
          <p className="text-center text-xs text-[#78716C]">Once your trip route is planned, forecasts for each stop will appear here.</p>
        </div>
      </Overlay>

      {/* Route Modal */}
      <Overlay isOpen={activeOverlay === 'route'} onClose={closeOverlay} title="Route Overview">
        <div className="flex flex-col items-center justify-center py-12 text-[#78716C]">
          <MapPin size={40} className="mb-4 opacity-30 text-[#1C1917]" />
          <p>No active route found.</p>
        </div>
      </Overlay>

      {/* Travel Info Modal */}
      <Overlay isOpen={activeOverlay === 'travel-info'} onClose={closeOverlay} title="Travel & Safety Info">
        <div className="space-y-4">
          <div className="p-4 bg-orange-50 border border-orange-100 rounded-xl">
            <h4 className="font-bold text-orange-700 flex items-center gap-2 mb-2"><Info size={16} /> Emergency Contacts</h4>
            <ul className="text-sm text-orange-900/80 space-y-2">
              <li>Tourist Police: 1912</li>
              <li>Ambulance: 1990</li>
              <li>Police Emergency: 119</li>
            </ul>
          </div>
          <p className="text-sm text-[#78716C] text-center mt-4">More contextual information will appear based on your destination.</p>
        </div>
      </Overlay>

      {/* Food Modal */}
      <Overlay isOpen={activeOverlay === 'food'} onClose={closeOverlay} title="Food & Dining">
        <div className="flex flex-col items-center justify-center py-12 text-[#78716C]">
          <Utensils size={40} className="mb-4 opacity-30 text-[#1C1917]" />
          <p>Food recommendations will appear here.</p>
        </div>
      </Overlay>

      {/* Accommodation Modal */}
      <Overlay isOpen={activeOverlay === 'accommodation'} onClose={closeOverlay} title="Accommodations">
        <div className="flex flex-col items-center justify-center py-12 text-[#78716C]">
          <HomeIcon size={40} className="mb-4 opacity-30 text-[#1C1917]" />
          <p>Your booked stays will appear here.</p>
        </div>
      </Overlay>

      {/* Calendar Modal — upcoming Sri Lankan festivals */}
      <Overlay isOpen={activeOverlay === 'calendar'} onClose={closeOverlay} title="Calendar" type="calendar">
        <div className="space-y-4">
          <p className="text-xs font-semibold uppercase tracking-wider text-[#78716C]">{fmtDateLong.format(now)}</p>
          {festivals.length > 0 ? (
            <ul className="space-y-3">
              {festivals.map((f) => (
                <li key={f.name} className="glow-card flex items-center gap-4 rounded-2xl border border-[#EAE2D6] p-4">
                  <div className="grid h-12 w-12 shrink-0 place-items-center rounded-xl bg-orange-50 text-orange-500">
                    <Calendar size={20} />
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="truncate font-semibold text-[#1C1917]">{f.name}</p>
                    <p className="text-xs text-[#78716C]">{f.label} &middot; {f.days === 0 ? 'today' : `in ${f.days} days`}</p>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <div className="flex flex-col items-center justify-center py-10 text-[#78716C]">
              <Calendar size={36} className="mb-3 opacity-30" />
              <p>No upcoming festivals scheduled.</p>
            </div>
          )}
        </div>
      </Overlay>

      {/* Currency Modal */}
      <Overlay isOpen={activeOverlay === 'currency'} onClose={closeOverlay} title="Currency">
        <div className="flex flex-col items-center justify-center py-12 text-[#78716C]">
          <Banknote size={40} className="mb-4 opacity-30 text-[#1C1917]" />
          <p>Live exchange rates will appear here once connected.</p>
        </div>
      </Overlay>

    </div>
  );
}