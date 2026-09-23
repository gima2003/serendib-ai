import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ChevronLeft, Calendar, Map, Info, Wallet, Home, Navigation, AlertTriangle, Edit2, Share } from 'lucide-react';
import { tripService } from '../services/tripService';

export default function TripWorkspace() {
  const { tripId } = useParams();
  const [activeTab, setActiveTab] = useState('overview');
  const [trip, setTrip] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTrip = async () => {
      try {
        setIsLoading(true);
        // Will call backend when ready
        const data = await tripService.getTrip(tripId);
        if (data) {
          setTrip(data);
        } else {
          // Temporarily mock an empty shell state when API returns null (development)
          // We don't hardcode fake logic, just a clean empty state structure.
          setTrip(null);
        }
      } catch (e) {
        setError("Failed to load trip data.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchTrip();
  }, [tripId]);

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Info },
    { id: 'itinerary', label: 'Itinerary', icon: Calendar },
    { id: 'route', label: 'Route', icon: Navigation },
    { id: 'budget', label: 'Budget', icon: Wallet },
    { id: 'stay_food', label: 'Stay & Food', icon: Home },
    { id: 'info', label: 'Travel Info', icon: AlertTriangle },
  ];

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#FFFCF8] flex items-center justify-center">
        <div className="animate-spin w-10 h-10 border-4 border-[#EAE2D6] border-t-orange-500 rounded-full"></div>
      </div>
    );
  }

  if (error || !trip) {
    return (
      <div className="min-h-screen bg-[#FFFCF8] flex flex-col items-center justify-center p-6">
        <div className="w-16 h-16 bg-[#FBF3EA] text-orange-500 rounded-full flex items-center justify-center mb-6">
          <Map size={32} />
        </div>
        <h2 className="text-2xl font-bold text-[#1C1917] mb-2 font-serif">Trip Not Found</h2>
        <p className="text-[#78716C] mb-8 text-center max-w-md">We couldn't load the details for this trip. It may not be ready yet or the service is unavailable.</p>
        <Link to="/dashboard" className="bg-orange-500 text-white px-6 py-3 rounded-xl font-medium hover:bg-orange-600 transition-colors">
          Return to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#FFFCF8] text-[#1C1917] font-sans selection:bg-orange-100 pb-20">
      
      {/* Workspace Header */}
      <header className="relative w-full h-[40vh] min-h-[300px] max-h-[500px] bg-[#0E1512] flex flex-col justify-between pt-6 px-4 md:px-8">
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1588668214407-6ea9a6d8c272?q=80&w=2071&auto=format&fit=crop')] bg-cover bg-center opacity-40 mix-blend-overlay"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-[#0E1512] via-transparent to-transparent"></div>
        
        <div className="relative z-10 flex justify-between items-center w-full max-w-7xl mx-auto">
          <Link to="/dashboard" className="text-white/80 hover:text-white flex items-center gap-2 transition-colors font-medium backdrop-blur-sm bg-black/20 px-4 py-2 rounded-full border border-white/10">
            <ChevronLeft size={18} />
            Dashboard
          </Link>
          <div className="flex gap-3">
            <button className="text-white/80 hover:text-white bg-black/20 p-2.5 rounded-full border border-white/10 transition-colors">
              <Share size={18} />
            </button>
            <button className="text-white/80 hover:text-white bg-black/20 p-2.5 rounded-full border border-white/10 transition-colors">
              <Edit2 size={18} />
            </button>
          </div>
        </div>

        <div className="relative z-10 w-full max-w-7xl mx-auto pb-8">
          <div className="flex flex-wrap items-center gap-3 mb-4">
            <span className="bg-orange-500/20 text-orange-400 text-sm font-bold px-3 py-1 rounded-full border border-orange-500/20 backdrop-blur-md">
              {trip?.duration || 'Duration'}
            </span>
            <span className="text-stone-300 font-medium flex items-center gap-1">
              <Calendar size={14} /> {trip?.dates || 'Dates'}
            </span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-2 font-serif tracking-tight">
            {trip?.title || 'Your Sri Lankan Journey'}
          </h1>
          <p className="text-lg text-stone-300 font-light max-w-2xl">
            {trip?.routeSummary || 'Route details will appear here once generated.'}
          </p>
        </div>
      </header>

      {/* Tabs */}
      <div className="sticky top-0 z-40 bg-white border-b border-[#EAE2D6] shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="flex space-x-1 sm:space-x-8 overflow-x-auto hide-scrollbar">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`whitespace-nowrap py-4 px-3 sm:px-1 border-b-2 font-medium text-sm flex items-center gap-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-orange-500 text-orange-600'
                    : 'border-transparent text-[#78716C] hover:text-[#1C1917] hover:border-[#EAE2D6]'
                }`}
              >
                <tab.icon size={16} />
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8 md:py-12">
        {/* Placeholder rendering since we have no real data yet */}
        <div className="bg-white border border-[#EAE2D6] rounded-3xl p-12 flex flex-col items-center justify-center text-center shadow-sm">
          <Info size={40} className="text-[#A8A29E] mb-4" />
          <h3 className="text-xl font-bold text-[#1C1917] mb-2">No {tabs.find(t=>t.id === activeTab)?.label} Data Available</h3>
          <p className="text-[#78716C] max-w-md">
            This section will display real {tabs.find(t=>t.id === activeTab)?.label.toLowerCase()} content once the backend integration is complete.
          </p>
        </div>
      </main>
    </div>
  );
}
