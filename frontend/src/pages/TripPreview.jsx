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
    route_plan,
    budget_plan,
    safety_plan,
    context_plan,
    schedule_plan,
    // Legacy key support
    route,
    budget,
    safety,
    context,
    schedule
  } = tripData;

  // Normalize: prefer _plan suffix (new), fall back to legacy keys
  const routeData = route_plan || route || {};
  const budgetData = budget_plan || budget || {};
  const safetyData = safety_plan || safety || {};
  const contextData = context_plan || context || {};
  const scheduleData = schedule_plan || schedule || {};

  const duration = profile?.duration_days
    || scheduleData?.itinerary?.length
    || scheduleData?.schedule?.length
    || scheduleData?.days?.length
    || 0;

  const routeDestinations = (() => {
    if (routeData?.route_summary?.start_location || routeData?.route_summary?.destinations?.length) {
      const stops = [];
      if (routeData.route_summary.start_location) stops.push(routeData.route_summary.start_location);
      if (routeData.route_summary.destinations) stops.push(...routeData.route_summary.destinations);
      return stops.filter(Boolean);
    }
    if (destinations?.length) {
      return destinations.map(d => d.city || d.destination).filter(Boolean);
    }
    return [];
  })();

  const displayDestinations = routeDestinations.length > 0 ? routeDestinations : (destinations || []).map(d => ({ city: d.city || d.destination }));

  const totalCost = budgetData?.estimated_total_cost_lkr
    || budgetData?.estimated_total_cost
    || budgetData?.total_estimated_cost_lkr
    || budgetData?.total_cost
    || 0;
  const isWithinBudget = budgetData?.within_budget !== undefined ? budgetData.within_budget : true;

  const weatherAlerts = contextData?.context_alerts || contextData?.alerts || [];
  const weatherPredictions = contextData?.weather_predictions || [];

  // Build safety route segments from both new and old field names
  const safetySegments = safetyData?.route_segments || safetyData?.regional_assessments || [];

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
        
        {/* Route Preview — use routeDestinations for correct ordered stops */}
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-orange-100 flex items-center gap-4 overflow-x-auto whitespace-nowrap">
          {(routeDestinations.length > 0 ? routeDestinations : (destinations || []).map(d => d.city || d.destination)).filter(Boolean).map((cityName, i, arr) => (
            <div key={i} className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-orange-900 font-medium">
                <MapPin size={18} className="text-orange-500" />
                {cityName}
              </div>
              {i < arr.length - 1 && (
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
              <p className="text-[#57534E] text-sm">
                {weatherPredictions.length > 0
                  ? weatherPredictions.slice(0, 3).map(w => `${w.location}: ${w.weather_condition} ${Math.round(w.temperature)}°C`).join(' · ')
                  : 'Expect tropical weather across Sri Lanka.'}
              </p>
              {weatherAlerts.length > 0 && (
                <div className="mt-3 flex items-start gap-2 text-orange-700 bg-orange-50 p-3 rounded-lg text-sm">
                  <AlertCircle size={16} className="mt-0.5 flex-shrink-0" />
                  <span>{typeof weatherAlerts[0] === 'string' ? weatherAlerts[0] : weatherAlerts[0]?.message || ''}</span>
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
              {safetySegments.length > 0
                ? safetySegments.slice(0, 3).map((r, i) => (
                    <div key={i} className="border border-stone-100 p-4 rounded-xl">
                      <p className="font-bold text-[#1C1917] mb-1">{r.from || r.to || r.region || 'Route Segment'}</p>
                      <p className="text-sm text-[#78716C] capitalize">{r.risk_level || r.safety_score || 'Low'} Risk</p>
                    </div>
                  ))
                : (
                    <div className="md:col-span-3">
                      <p className="text-[#57534E]">
                        {safetyData?.risk_level
                          ? `Overall risk level: ${safetyData.risk_level}. ${safetyData?.safety_explanation || ''}`
                          : 'No regional alerts. Travel conditions are generally safe.'}
                      </p>
                    </div>
                  )
              }
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
