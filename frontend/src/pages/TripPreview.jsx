import { useState } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { Cloud, MapPin, ShieldAlert, DollarSign, Calendar, ChevronLeft, Check, AlertCircle } from 'lucide-react';
import { tripService } from '../services/tripService';

export default function TripPreview() {
  const location = useLocation();
  const navigate = useNavigate();
  const tripData = location.state?.tripData;
  const [isSaving, setIsSaving] = useState(false);
  const [isSaved, setIsSaved] = useState(false);

  if (!tripData) {
    return (
      <div className="min-h-screen bg-[#FFFCF8] flex items-center justify-center flex-col gap-4">
        <p className="text-[#57534E]">No trip generated yet.</p>
        <Link to="/plan-trip" className="text-orange-500 font-medium hover:underline">
          Return to Planner
        </Link>
      </div>
    );
  }

  const {
    profile,
    destinations,
    route,
    budget,
    safety,
    context,
    schedule
  } = tripData;

  const duration = profile?.duration_days || schedule?.schedule?.length || schedule?.days?.length || 0;
  const firstCity = destinations?.[0]?.city || destinations?.[0]?.destination || 'Sri Lanka';
  const lastCity = destinations?.[destinations.length - 1]?.city || destinations?.[destinations.length - 1]?.destination || '';

  const totalCost = budget?.estimated_total_cost || budget?.total_estimated_cost_lkr || budget?.total_cost || budget?.estimated_total_cost_lkr || 0;
  const isWithinBudget = budget?.within_budget !== undefined ? budget.within_budget : true;

  const weatherAlerts = context?.context_alerts || context?.alerts || [];
  const crowdPredictions = context?.crowd_predictions || [];

  const handleSaveTrip = async () => {
    setIsSaving(true);
    try {
      await tripService.saveTrip(tripData);
      setIsSaved(true);
      // Wait a moment before redirecting so user sees the success state
      setTimeout(() => {
        navigate('/my-trips');
      }, 1500);
    } catch (error) {
      console.error("Failed to save trip", error);
      alert("Failed to save trip. Please try again.");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FFFCF8] text-[#1C1917] font-sans pb-24">
      {/* Header */}
      <div className="bg-[#0E1512] text-white pt-20 pb-16 px-6 relative overflow-hidden rounded-b-3xl">
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1546708973-b339540b5162?q=80&w=2070&auto=format&fit=crop')] bg-cover bg-center opacity-20"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-[#0E1512] to-transparent"></div>
        
        <div className="max-w-4xl mx-auto relative z-10 flex flex-col gap-6">
          <button 
            onClick={() => navigate('/plan-trip')} 
            className="w-fit flex items-center gap-2 text-white/70 hover:text-white transition-colors text-sm font-medium"
          >
            <ChevronLeft size={18} /> Cancel
          </button>
          
          <div>
            <h1 className="text-4xl md:text-5xl font-bold font-serif mb-3">Sri Lanka Escape</h1>
            <p className="text-orange-400 text-lg flex items-center gap-3">
              <Calendar size={20} /> 
              {duration} Days • {profile?.travel_type || 'Couple'}
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 -mt-8 relative z-20 space-y-8">
        
        {/* Route Preview */}
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-orange-100 flex items-center gap-4 overflow-x-auto whitespace-nowrap">
          {destinations?.map((dest, i) => (
            <div key={i} className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-orange-900 font-medium">
                <MapPin size={18} className="text-orange-500" />
                {dest.city || dest.destination}
              </div>
              {i < destinations.length - 1 && (
                <div className="w-8 h-[2px] bg-orange-200"></div>
              )}
            </div>
          ))}
        </div>

        {/* Summary Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          {/* Budget */}
          <div className="bg-white rounded-2xl p-6 shadow-sm border border-stone-100 flex flex-col">
            <div className="flex items-center gap-3 mb-4 text-[#57534E]">
              <div className="w-10 h-10 rounded-full bg-green-50 flex items-center justify-center text-green-600">
                <DollarSign size={20} />
              </div>
              <h2 className="font-bold text-lg text-[#1C1917]">Budget</h2>
            </div>
            <div className="flex justify-between items-end mt-auto">
              <div>
                <p className="text-sm text-[#78716C] mb-1">Estimated Cost</p>
                <p className="text-2xl font-bold text-[#1C1917]">{totalCost.toLocaleString()} LKR</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-[#78716C] mb-1">Within Budget?</p>
                <p className={`font-semibold ${isWithinBudget ? 'text-green-600' : 'text-red-500'}`}>
                  {isWithinBudget ? 'Yes' : 'No'}
                </p>
              </div>
            </div>
          </div>

          {/* Weather */}
          <div className="bg-white rounded-2xl p-6 shadow-sm border border-stone-100 flex flex-col">
            <div className="flex items-center gap-3 mb-4 text-[#57534E]">
              <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center text-blue-500">
                <Cloud size={20} />
              </div>
              <h2 className="font-bold text-lg text-[#1C1917]">Weather Context</h2>
            </div>
            <div className="mt-auto">
              <p className="text-[#57534E]">
                {context?.weather_forecast?.map(w => `${w.location}: ${w.condition} (${w.temperature})`).join(', ') || 'Expect tropical weather.'}
              </p>
              {weatherAlerts.length > 0 && (
                <div className="mt-3 flex items-start gap-2 text-orange-700 bg-orange-50 p-3 rounded-lg text-sm">
                  <AlertCircle size={16} className="mt-0.5 flex-shrink-0" />
                  <span>{weatherAlerts[0]}</span>
                </div>
              )}
            </div>
          </div>

          {/* Safety */}
          <div className="bg-white rounded-2xl p-6 shadow-sm border border-stone-100 flex flex-col md:col-span-2">
            <div className="flex items-center gap-3 mb-4 text-[#57534E]">
              <div className="w-10 h-10 rounded-full bg-stone-100 flex items-center justify-center text-stone-600">
                <ShieldAlert size={20} />
              </div>
              <h2 className="font-bold text-lg text-[#1C1917]">Safety Overview</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {safety?.regional_assessments?.slice(0, 3).map((r, i) => (
                <div key={i} className="border border-stone-100 p-4 rounded-xl">
                  <p className="font-bold text-[#1C1917] mb-1">{r.region}</p>
                  <p className="text-sm text-[#78716C] capitalize">{r.risk_level} Risk</p>
                </div>
              )) || (
                <p className="text-[#57534E]">No regional alerts.</p>
              )}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col md:flex-row gap-4 pt-6">
          <button 
            onClick={handleSaveTrip}
            disabled={isSaving || isSaved}
            className={`flex-1 text-white py-4 rounded-xl font-bold transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-2 disabled:opacity-70 ${isSaved ? 'bg-green-600' : 'bg-orange-500 hover:bg-orange-600'}`}
          >
            {isSaved ? <><Check size={20} /> SAVED ✓</> : isSaving ? 'SAVING...' : <><Check size={20} /> SAVE TRIP</>}
          </button>
          
          <button 
            onClick={() => navigate('/plan-trip')}
            className="flex-1 bg-white hover:bg-stone-50 text-[#57534E] py-4 rounded-xl font-bold transition-all border border-stone-200"
          >
            EDIT PLAN
          </button>
        </div>

      </div>
    </div>
  );
}
