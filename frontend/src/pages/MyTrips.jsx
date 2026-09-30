import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Calendar, MapPin, ChevronRight, ChevronLeft, Plane, Loader2 } from 'lucide-react';
import { tripService } from '../services/tripService';
import { authService } from '../services/authService';
import { SerendibNavbar } from '../components/navigation/SerendibNavbar';

export default function MyTrips() {
  const [trips, setTrips] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const location = useLocation();
  
  // Read tab from URL query params
  const searchParams = new URLSearchParams(location.search);
  const initialTab = searchParams.get('tab') ? searchParams.get('tab').toUpperCase() : 'ALL';
  const [filter, setFilter] = useState(initialTab); // ALL, UPCOMING, SAVED, COMPLETED

  // Update filter if URL changes
  useEffect(() => {
    const tab = searchParams.get('tab');
    if (tab) {
      setFilter(tab.toUpperCase());
    }
  }, [location.search]);

  useEffect(() => {
    const fetchTrips = async () => {
      try {
        const response = await tripService.getAllTrips();
        if (Array.isArray(response)) {
          setTrips(response);
        } else if (response && response.data) {
          setTrips(response.data);
        }
      } catch (error) {
        console.error("Failed to fetch trips", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchTrips();
  }, []);

  const filteredTrips = trips.filter(t => {
    if (filter === 'ALL') return true;
    if (filter === 'SAVED') return t.saved === true;
    return t.status?.toUpperCase() === filter.toUpperCase();
  });

  return (
    <div className="min-h-screen bg-[#FFFCF8] font-sans">
      <SerendibNavbar isAuth={authService.isAuthenticated()} userName={authService.getCurrentUser()?.full_name || 'Traveller'} />

      <main className="max-w-6xl mx-auto px-6 pt-32 pb-24">
        <Link to="/dashboard" className="inline-flex items-center gap-2 text-[#78716C] hover:text-[#1C1917] transition-colors mb-6 font-medium">
          <ChevronLeft size={18} /> Back to Dashboard
        </Link>
        <h1 className="text-4xl font-serif font-bold text-[#1C1917] mb-8">My Trips</h1>

        <div className="flex gap-4 border-b border-stone-200 mb-8 pb-4 overflow-x-auto">
          {['ALL', 'UPCOMING', 'SAVED', 'COMPLETED', 'CANCELLED'].map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors whitespace-nowrap ${
                filter === f ? 'bg-[#1C1917] text-white' : 'text-[#78716C] hover:bg-stone-100'
              }`}
            >
              {f.charAt(0) + f.slice(1).toLowerCase()}
            </button>
          ))}
        </div>

        {isLoading ? (
          <div className="flex justify-center items-center py-20">
            <Loader2 className="animate-spin text-orange-500" size={40} />
          </div>
        ) : filteredTrips.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-3xl border border-stone-100">
            <Plane size={48} className="mx-auto text-stone-300 mb-4" />
            <h2 className="text-xl font-bold text-[#1C1917] mb-2">No trips found</h2>
            <p className="text-[#78716C] mb-6">You haven't planned any trips in this category yet.</p>
            <Link to="/plan-trip" className="bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-xl font-bold transition-colors">
              Start Planning
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredTrips.map(trip => {
              const profile = trip.profile || {};
              const dests = trip.destinations || [];
              const routePlan = trip.route_plan || trip.route || {};
              const routeSummary = routePlan.route_summary 
                ? [routePlan.route_summary.start_location, ...routePlan.route_summary.destinations].filter(Boolean).join(' → ')
                : dests.map(d => d.city || d.destination).join(' → ');
              const duration = profile.duration_days || trip.schedule?.schedule?.length || trip.schedule?.days?.length || 0;
              
              const formatShortDate = (dateStr) => {
                if (!dateStr) return null;
                try {
                  const d = new Date(dateStr);
                  if (isNaN(d)) return null;
                  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                } catch { return null; }
              };
              
              const formatLongDate = (dateStr) => {
                if (!dateStr) return null;
                try {
                  const d = new Date(dateStr);
                  if (isNaN(d)) return null;
                  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
                } catch { return null; }
              };
              
              let dateDisplay = 'Dates TBD';
              const sDate = formatShortDate(profile.start_date || trip.start_date);
              const eDate = formatShortDate(profile.end_date || trip.end_date);
              if (sDate && eDate) {
                dateDisplay = `${sDate} – ${eDate}`;
              } else if (sDate) {
                dateDisplay = sDate;
              }

              const isCancelled = trip.status === 'CANCELLED';

              return (
                <div key={trip.trip_id} className={`bg-white border border-[#EAE2D6] rounded-3xl overflow-hidden transition-shadow group ${isCancelled ? 'opacity-80' : 'hover:shadow-lg'}`}>
                  <div className="h-40 bg-stone-100 relative">
                    <img 
                      src={`https://source.unsplash.com/800x600/?srilanka,${dests[0]?.city || 'nature'}`}
                      alt="Trip Cover"
                      className={`w-full h-full object-cover ${isCancelled ? 'grayscale opacity-60' : ''}`}
                      onError={(e) => { e.target.src = 'https://images.unsplash.com/photo-1546708973-b339540b5162?q=80&w=2070&auto=format&fit=crop'; }}
                    />
                    <div className={`absolute top-4 left-4 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-bold ${isCancelled ? 'text-red-600' : 'text-orange-600'}`}>
                      {trip.status}
                    </div>
                  </div>
                  <div className="p-6">
                    <h3 className="text-xl font-bold text-[#1C1917] mb-2 truncate">{trip.trip_name || 'Sri Lanka Escape'}</h3>
                    
                    {isCancelled && trip.cancelled_at ? (
                      <div className="text-sm text-red-600 font-medium mb-4">
                        Cancelled on {formatLongDate(trip.cancelled_at)}
                      </div>
                    ) : (
                      <div className="flex items-center gap-2 text-sm text-[#78716C] mb-4">
                        <Calendar size={16} />
                        {dateDisplay}
                        <span>•</span>
                        {duration} Days
                      </div>
                    )}
                    
                    <div className="flex items-start gap-2 text-sm text-[#78716C] mb-6">
                      <MapPin size={16} className="mt-1 flex-shrink-0" />
                      <p className="line-clamp-2">{routeSummary || 'Sri Lanka'}</p>
                    </div>

                    <div className="flex items-center gap-3">
                      <Link 
                        to={`/trip/${trip.trip_id}`}
                        className="flex-1 bg-[#1C1917] hover:bg-[#292524] text-white text-center py-2.5 rounded-xl font-medium transition-colors"
                      >
                        View Trip
                      </Link>
                      {!isCancelled && (
                        <Link 
                          to={`/plan-trip/${trip.trip_id}`}
                          className="p-2.5 bg-stone-100 hover:bg-stone-200 text-[#57534E] rounded-xl transition-colors"
                        >
                          <ChevronRight size={20} />
                        </Link>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>
    </div>
  );
}
