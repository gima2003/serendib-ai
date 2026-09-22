import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Map, Calendar, Wallet, ArrowRight, Compass,
  LogOut, Sun,
  Navigation, Info, Utensils, Home as HomeIcon, MapPin, Search, Banknote
} from 'lucide-react';
import { authService } from '../services/authService';
import { tripService } from '../services/tripService';
import toast from 'react-hot-toast';
import Overlay from '../components/Overlay';
import { SerendibNavbar } from '../components/navigation/SerendibNavbar';
import { IMG, wiki, fmtDateLong, upcomingEvents } from '../components/common/Shared';
import { useDynamicHero } from '../hooks/useDynamicHero';
import { useSriLankaWeather, useColomboClock, fmtTime, fmtDate, wmo } from '../hooks/useSriLankaWeather';

/* Small styles this page needs on top of the shared navbar styles       */
/* (SerendibNavbar already injects the fade-in / font-display / page-x   */
/* rules, so this only adds the hero zoom and the hover-glow utilities). */
const DASHBOARD_STYLES = `
@keyframes dashKenburns { from { transform: scale(1); } to { transform: scale(1.08); } }
.dash-hero-img { animation: dashKenburns 9s ease-out forwards; }

.glow-card, .glow-btn {
  transition: transform .3s cubic-bezier(.22,1,.36,1), box-shadow .3s ease, border-color .3s ease, background-color .3s ease;
}
.glow-card:hover, .glow-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 18px 40px -18px rgba(249,115,22,0.45);
  border-color: rgba(249,115,22,0.35);
}
.glow-btn:active { transform: translateY(-1px); }

@media (prefers-reduced-motion: reduce) {
  .dash-hero-img { animation: none; }
  .glow-card, .glow-btn { transition: none; }
  .glow-card:hover, .glow-btn:hover { transform: none; }
}
`;

export default function UserDashboard() {
  const navigate = useNavigate();
  // eslint-disable-next-line no-unused-vars
  const [user, setUser] = useState(authService.getCurrentUser());

  // Overlays state
  const [activeOverlay, setActiveOverlay] = useState(null);

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

    fetchDashboardData();
  }, [navigate]);

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  const userName = user?.full_name || user?.name || 'Traveller';
  const userEmail = user?.email || 'user@example.com';

  const lastLoginDate = user?.last_login || user?.updated_at || user?.created_at;
  const formattedLastLogin = lastLoginDate
    ? new Date(lastLoginDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
    : 'Recently';

  const closeOverlay = () => setActiveOverlay(null);

  const heroSlide = useDynamicHero();
  const weatherData = useSriLankaWeather(['Colombo']);
  const colomboWeather = weatherData['Colombo'];
  const now = useColomboClock();
  const formattedTime = fmtTime.format(now);
  const formattedDate = fmtDate.format(now);
  const festivals = upcomingEvents(now);
  const WeatherIcon = colomboWeather ? wmo(colomboWeather.code).icon : Sun;

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
            defaultValue={userName}
            className="w-full px-4 py-3 text-sm bg-white border border-[#EAE2D6] rounded-xl text-[#1C1917] focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition-all shadow-sm"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-[#78716C] mb-1">Country</label>
          <input
            type="text"
            defaultValue="Sri Lanka"
            className="w-full px-4 py-3 text-sm bg-white border border-[#EAE2D6] rounded-xl text-[#1C1917] focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition-all shadow-sm"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-[#78716C] mb-1">Preferred Currency</label>
          <select className="w-full px-4 py-3 text-sm bg-white border border-[#EAE2D6] rounded-xl text-[#1C1917] focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition-all shadow-sm">
            <option>LKR</option>
            <option>USD</option>
            <option>EUR</option>
          </select>
        </div>
      </div>

      <div className="mt-8 pt-6 border-t border-[#EAE2D6] flex flex-col gap-3">
        <button
          onClick={() => {
            toast.success('Profile updated');
            closeOverlay();
          }}
          className="w-full bg-orange-500 text-white font-medium py-3 rounded-xl hover:bg-orange-600 transition-colors shadow-sm"
        >
          Save Changes
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
    <div className="min-h-screen bg-[#FFFCF8] text-[#1C1917] font-sans overflow-x-hidden selection:bg-orange-100">
      <style>{DASHBOARD_STYLES}</style>

      {/* Top Navigation — identical component/behaviour to the Home page navbar */}
      <SerendibNavbar
        isAuth
        userName={userName}
        onOpenProfile={() => setActiveOverlay('profile')}
        onOpenCalendar={() => setActiveOverlay('calendar')}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 pt-24 pb-8 md:pt-28 md:pb-12 space-y-12">

        {/* Welcome Section */}
        <section className="relative overflow-hidden rounded-3xl bg-[#0E1512] shadow-md flex flex-col md:flex-row min-h-[400px]">

          {/* Dynamic, brighter hero image — softer warm-green overlay instead of a heavy black one */}
          <div key={heroSlide.img} className="fade-in absolute inset-0">
            <img
              src={heroSlide.img}
              alt="Sri Lanka Landscape"
              className="dash-hero-img w-full h-full object-cover"
              style={{ objectPosition: heroSlide.align, filter: 'brightness(1.12) saturate(1.12) contrast(1.02)' }}
            />
          </div>
          <div className="absolute inset-0 bg-gradient-to-r from-emerald-950/80 via-emerald-950/35 to-transparent" />
          <div className="absolute inset-0 bg-gradient-to-t from-emerald-950/55 via-transparent to-transparent" />
          <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-orange-500/25 rounded-full blur-[100px] pointer-events-none" />

          <div className="relative z-10 p-8 md:p-12 max-w-2xl flex-1 flex flex-col justify-center">
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

          <div className="relative z-10 w-full md:w-72 border-t md:border-t-0 md:border-l border-white/10 p-8 flex flex-col justify-between backdrop-blur-sm bg-black/10">
            <div>
               <p className="text-white/60 text-xs font-bold uppercase tracking-wider mb-4 flex items-center gap-1.5">
                 <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" /> Live &middot; Today in Colombo
               </p>
               <div className="flex items-center gap-3">
                  <WeatherIcon size={34} className="text-orange-300" strokeWidth={1.6} />
                  <div className="text-white">
                     <span className="text-4xl font-light">{colomboWeather?.temp ? Math.round(colomboWeather.temp) : '--'}</span>
                     <span className="text-xl align-top">&deg;C</span>
                  </div>
                  <div className="text-white/80 text-sm">
                     <p>Feels like {colomboWeather?.feels ? Math.round(colomboWeather.feels) : '--'}&deg;</p>
                     <p>Humidity {colomboWeather?.humidity ? Math.round(colomboWeather.humidity) : '--'}%</p>
                  </div>
               </div>
            </div>

            <div className="mt-8">
               <p className="text-white/60 text-xs font-bold uppercase tracking-wider mb-2">Date</p>
               <p className="text-white font-medium">{formattedDate}</p>
            </div>
          </div>
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
                <div className="w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
                  <Wallet size={22} />
                </div>
                <span className="text-sm font-medium text-[#57534E] group-hover:text-orange-700">Budget</span>
              </button>

              <button onClick={() => setActiveOverlay('weather')} className="glow-btn bg-white border border-[#EAE2D6] p-4 rounded-2xl flex flex-col items-center justify-center gap-3 group">
                <div className="w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
                  <Sun size={22} />
                </div>
                <span className="text-sm font-medium text-[#57534E] group-hover:text-orange-700">Weather</span>
              </button>

              <button onClick={() => setActiveOverlay('route')} className="glow-btn bg-white border border-[#EAE2D6] p-4 rounded-2xl flex flex-col items-center justify-center gap-3 group">
                <div className="w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
                  <Navigation size={22} />
                </div>
                <span className="text-sm font-medium text-[#57534E] group-hover:text-orange-700">Route</span>
              </button>

              <button onClick={() => setActiveOverlay('travel-info')} className="glow-btn bg-white border border-[#EAE2D6] p-4 rounded-2xl flex flex-col items-center justify-center gap-3 group">
                <div className="w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
                  <Info size={22} />
                </div>
                <span className="text-sm font-medium text-[#57534E] group-hover:text-orange-700">Travel Info</span>
              </button>

              <button onClick={() => setActiveOverlay('food')} className="glow-btn bg-white border border-[#EAE2D6] p-4 rounded-2xl flex flex-col items-center justify-center gap-3 group">
                <div className="w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
                  <Utensils size={22} />
                </div>
                <span className="text-sm font-medium text-[#57534E] group-hover:text-orange-700">Food</span>
              </button>

              <button onClick={() => setActiveOverlay('accommodation')} className="glow-btn bg-white border border-[#EAE2D6] p-4 rounded-2xl flex flex-col items-center justify-center gap-3 group">
                <div className="w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
                  <HomeIcon size={22} />
                </div>
                <span className="text-sm font-medium text-[#57534E] group-hover:text-orange-700">Stays</span>
              </button>

              <button onClick={() => setActiveOverlay('calendar')} className="glow-btn bg-white border border-[#EAE2D6] p-4 rounded-2xl flex flex-col items-center justify-center gap-3 group relative">
                {festivals.length > 0 && (
                  <span className="absolute top-3 right-3 h-2 w-2 rounded-full bg-orange-500" />
                )}
                <div className="w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
                  <Calendar size={22} />
                </div>
                <span className="text-sm font-medium text-[#57534E] group-hover:text-orange-700">Calendar</span>
              </button>

              <button onClick={() => setActiveOverlay('currency')} className="glow-btn bg-white border border-[#EAE2D6] p-4 rounded-2xl flex flex-col items-center justify-center gap-3 group">
                <div className="w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center group-hover:bg-orange-500 group-hover:text-white group-hover:scale-110 transition-all shadow-sm">
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