import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ChevronLeft, Calendar, Map, Info, Wallet, Home, Navigation, AlertTriangle, Cloud, MapPin, DollarSign, Check, Activity, Sun, Utensils } from 'lucide-react';
import { tripService } from '../services/tripService';

export default function TripWorkspace() {
  const { tripId } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');
  const [trip, setTrip] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [isCancelling, setIsCancelling] = useState(false);

  useEffect(() => {
    const fetchTrip = async () => {
      try {
        setIsLoading(true);
        const data = await tripService.getTrip(tripId);
        if (data && data.trip_id) {
          setTrip(data);
        } else if (data && data.data) {
          setTrip(data.data);
        } else {
          setError("Trip not found");
        }
      } catch (e) {
        console.error("Failed to fetch trip", e);
        setError("Trip unavailable");
      } finally {
        setIsLoading(false);
      }
    };
    fetchTrip();
  }, [tripId]);

  const handleCancelTrip = async () => {
    try {
      setIsCancelling(true);
      await tripService.cancelTrip(tripId);
      setShowCancelModal(false);
      navigate('/my-trips?tab=CANCELLED');
    } catch (e) {
      console.error("Failed to cancel trip", e);
      // Optional: Add a toast notification for error
    } finally {
      setIsCancelling(false);
    }
  };

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
        <p className="text-[#78716C] mb-8 text-center max-w-md">We couldn't load the details for this trip.</p>
        <Link to="/dashboard" className="bg-orange-500 text-white px-6 py-3 rounded-xl font-medium hover:bg-orange-600 transition-colors">
          Return to Dashboard
        </Link>
      </div>
    );
  }

  // Derived data — handle both new (_plan suffix) and legacy field names
  const profile = trip.profile || {};
  const dests = trip.destinations || [];
  
  // Schedule: try schedule_plan first, then schedule (legacy)
  const schedulePlan = trip.schedule_plan || trip.schedule || {};
  const schedule = schedulePlan?.itinerary || [];
  
  // Budget
  const budget = trip.budget_plan || trip.budget || {};
  
  // Safety
  const safety = trip.safety_plan || trip.safety || {};
  
  // Context (weather/crowd)
  const context = trip.context_plan || trip.context || {};
  
  // Accommodation — support both new and old structures
  const accPlan = trip.accommodation_plan || trip.accommodation || {};
  const accommodations = (
    // New structure: accommodation_plan.accommodation_plan[].hotel_options[] where is_selected
    accPlan?.accommodation_plan?.flatMap?.(da =>
      (da.hotel_options || []).filter(h => h.is_selected)
    ) ||
    // Fallback: any hotel with is_selected from any hotel_options
    accPlan?.accommodation_plan?.flatMap?.(da =>
      da.hotel_options || []
    ) ||
    []
  );
  
  // Food options
  const foodOptions = trip.food_options || trip.food || [];
  
  // Route
  const route = trip.route_plan || trip.route || {};
  
  // Build ordered route stops from route_summary or fallback
  const routeDestinations = (() => {
    if (route?.route_summary?.start_location || route?.route_summary?.destinations?.length) {
      const stops = [];
      if (route.route_summary.start_location) stops.push(route.route_summary.start_location);
      if (route.route_summary.destinations) stops.push(...route.route_summary.destinations);
      return stops.filter(Boolean);
    }
    if (profile.starting_location || profile.must_visit_destinations?.length) {
      const stops = [];
      if (profile.starting_location) stops.push(profile.starting_location);
      if (profile.must_visit_destinations) stops.push(...profile.must_visit_destinations);
      return stops.filter(Boolean);
    }
    return dests.map(d => d.city || d.destination).filter(Boolean);
  })();
  
  const routeSummary = routeDestinations.join(' → ') || 'Sri Lanka';
  const duration = profile.duration_days || schedule.length || 0;

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-2xl p-6 border border-stone-200">
              <h3 className="font-bold text-lg mb-4 flex items-center gap-2"><MapPin className="text-orange-500"/> Route Summary</h3>
              <div className="space-y-4">
                {routeDestinations.map((destName, i) => {
                  const destObj = dests.find(d => (d.city === destName || d.destination === destName));
                  // Count attractions from both the raw destination data and the itinerary
                  const rawAttrCount = destObj?.attractions?.length || 0;
                  const itineraryAttrCount = schedule.filter(day =>
                    day.city === destName &&
                    day.activities?.some(a => a.type === 'attraction')
                  ).reduce((sum, day) => sum + (day.activities?.filter(a => a.type === 'attraction').length || 0), 0);
                  const attrCount = rawAttrCount || itineraryAttrCount;
                  return (
                    <div key={i} className="flex gap-4 items-start">
                      <div className="mt-1 w-3 h-3 rounded-full bg-orange-400"></div>
                      <div>
                        <p className="font-bold text-[#1C1917]">{destName}</p>
                        <p className="text-sm text-[#78716C] capitalize">
                          {attrCount > 0 ? `${attrCount} Attraction${attrCount > 1 ? 's' : ''}` : 'Explore & leisure'}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
            
            <div className="space-y-6">
              <div className="bg-white rounded-2xl p-6 border border-stone-200">
                <h3 className="font-bold text-lg mb-4 flex items-center gap-2"><DollarSign className="text-green-600"/> Budget Status</h3>
                <p className="text-3xl font-bold">{budget.estimated_total_cost_lkr?.toLocaleString() || 0} LKR</p>
                <p className={`text-sm mt-2 font-medium ${budget.within_budget ? 'text-green-600' : 'text-red-500'}`}>
                  {budget.within_budget ? 'Within your budget constraints' : `Exceeds budget by ${budget.over_budget_amount?.toLocaleString()} LKR`}
                </p>
                {!budget.within_budget && budget.savings_opportunities?.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-stone-100">
                    <p className="text-sm font-bold text-[#1C1917] mb-3">Savings Options</p>
                    <ul className="space-y-3">
                      {budget.savings_opportunities.map((saving, i) => (
                        <li key={i} className="text-sm bg-orange-50 p-3 rounded-lg border border-orange-100">
                          <span className="font-bold text-orange-800 block mb-1">Option {i + 1}: {saving.alternative_option}</span>
                          <span className="text-[#57534E] block mb-1">{saving.description}</span>
                          <span className="text-green-700 font-bold">Estimated saving: {saving.potential_saving_lkr?.toLocaleString()} LKR</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
              
              <div className="bg-white rounded-2xl p-6 border border-stone-200">
                <h3 className="font-bold text-lg mb-4 flex items-center gap-2"><Cloud className="text-blue-500"/> Weather</h3>
                <div className="space-y-4">
                  {context.weather_predictions?.map((w, i) => (
                    <div key={i} className="flex flex-col text-sm border-b border-stone-100 pb-3 last:border-0 last:pb-0">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-bold text-[#1C1917]">
                          {w.date ? `${new Date(w.date).toLocaleDateString('en-US', { month: 'long', day: 'numeric' })} • ` : ''}{w.location}
                        </span>
                        <span className="text-[#78716C] font-medium">{w.weather_condition} • {w.temperature}°C</span>
                      </div>
                      {w.recommendations && w.recommendations.length > 0 && (
                        <p className="text-[#78716C] text-xs mt-1">Tip: {w.recommendations[0]}</p>
                      )}
                    </div>
                  ))}
                  {(!context.weather_predictions || context.weather_predictions.length === 0) && (
                    <p className="text-sm text-[#78716C] italic">Weather predictions unavailable.</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        );
      case 'itinerary':
        return (
          <div className="space-y-6">
            {schedule.map((day, i) => (
              <div key={i} className="bg-white rounded-2xl p-6 border border-stone-200">
                <div className="border-b border-stone-100 pb-4 mb-4 flex justify-between items-center">
                  <h3 className="text-xl font-bold font-serif text-[#1C1917]">Day {day.day}</h3>
                  <span className="text-orange-600 font-medium bg-orange-50 px-3 py-1 rounded-full text-sm">
                    {day.city}
                  </span>
                </div>
                <div className="space-y-4">
                  {day.activities?.map((act, j) => (
                    <div key={j} className="grid grid-cols-[100px_1fr] gap-4">
                      <span className="text-sm font-bold text-[#78716C]">{act.time}</span>
                      <div>
                        <p className="text-[#1C1917] font-medium flex items-center gap-2">
                          {act.name}
                          <span className="text-xs font-normal px-2 py-0.5 rounded-full bg-stone-100 text-stone-500 capitalize">{act.type}</span>
                        </p>
                        {act.description && <p className="text-sm text-[#78716C] mt-1">{act.description}</p>}
                      </div>
                    </div>
                  ))}
                  {day.accommodation?.name && (
                    <div className="grid grid-cols-[100px_1fr] gap-4 pt-4 border-t border-stone-50">
                      <span className="text-sm font-bold text-[#78716C]">Stay</span>
                      <p className="text-orange-600 font-medium">{day.accommodation.name}</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        );
      case 'route':
        return (
          <div className="bg-white rounded-2xl p-6 border border-stone-200">
            <h3 className="font-bold text-lg mb-6">Generated Route Map</h3>
            {route.route_summary && (
              <div className="mb-6 p-4 bg-orange-50 rounded-xl border border-orange-100">
                <p className="font-bold text-orange-900 mb-1">Trip Totals</p>
                <p className="text-sm text-orange-800">
                  Total Distance: {Math.round(route.route_summary.total_distance_km)} km • 
                  Estimated Travel Time: {Math.floor(route.route_summary.total_estimated_duration_minutes / 60)}h {Math.round(route.route_summary.total_estimated_duration_minutes % 60)}m
                </p>
              </div>
            )}

            <div className="space-y-4">
              {route.legs?.map((leg, i) => (
                <div key={i} className="flex gap-4 p-4 border border-stone-100 rounded-xl bg-stone-50">
                  <Navigation className="text-orange-500 mt-1" size={20} />
                  <div>
                    <p className="font-bold">{leg.from_location} to {leg.to_location}</p>
                    {leg.road_route && (
                      <p className="text-sm text-[#78716C] capitalize">
                        {leg.road_route.mode || 'Drive'} • {Math.round(leg.road_route.distance_km)} km • 
                        {Math.floor(leg.road_route.estimated_duration_minutes / 60)} hrs {Math.round(leg.road_route.estimated_duration_minutes % 60)} mins
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        );
      case 'budget':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl p-6 border border-stone-200 flex justify-between items-center">
              <div>
                <p className="text-[#78716C] mb-1">Total Estimated Cost</p>
                <p className="text-4xl font-bold text-[#1C1917]">{budget.estimated_total_cost_lkr?.toLocaleString() || 0} LKR</p>
              </div>
              <div className="text-right">
                <p className="text-[#78716C] mb-1">Within Profile Budget</p>
                <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-bold ${budget.within_budget ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                  {budget.within_budget ? <Check size={16}/> : <AlertTriangle size={16}/>}
                  {budget.within_budget ? 'Yes' : 'No'}
                </span>
              </div>
            </div>
            
            <div className="bg-white rounded-2xl p-6 border border-stone-200">
              <h3 className="font-bold text-lg mb-4">Cost Breakdown</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center p-3 hover:bg-stone-50 rounded-lg">
                  <span className="font-medium">Accommodation</span>
                  <span className="font-bold">{(budget.cost_breakdown?.accommodation_lkr || 0).toLocaleString()} LKR</span>
                </div>
                <div className="flex justify-between items-center p-3 hover:bg-stone-50 rounded-lg">
                  <div>
                    <span className="font-medium">Transport</span>
                    {budget.recommended_transport?.recommended_mode && budget.recommended_transport.recommended_mode !== 'unknown' && (
                      <span className="ml-2 text-xs text-[#78716C] bg-stone-100 px-2 py-0.5 rounded-full capitalize">
                        {budget.recommended_transport.recommended_mode}
                      </span>
                    )}
                  </div>
                  <span className="font-bold">
                    {(budget.cost_breakdown?.transport_lkr || 0) > 0
                      ? `${(budget.cost_breakdown.transport_lkr).toLocaleString()} LKR`
                      : 'Calculating...'}
                  </span>
                </div>
                <div className="flex justify-between items-center p-3 hover:bg-stone-50 rounded-lg">
                  <span className="font-medium">Food</span>
                  <span className="font-bold">{(budget.cost_breakdown?.food_lkr || 0).toLocaleString()} LKR</span>
                </div>
                <div className="flex justify-between items-center p-3 hover:bg-stone-50 rounded-lg">
                  <span className="font-medium">Attractions</span>
                  <span className="font-bold">
                    {(budget.cost_breakdown?.attractions_lkr || 0) > 0
                      ? `${(budget.cost_breakdown.attractions_lkr).toLocaleString()} LKR`
                      : 'Free / Included'}
                  </span>
                </div>
                <div className="flex justify-between items-center p-3 hover:bg-stone-50 rounded-lg border-t border-stone-100 mt-2 pt-4">
                  <span className="font-medium text-[#78716C]">Contingency (10%)</span>
                  <span className="font-bold text-[#78716C]">{(budget.cost_breakdown?.contingency_lkr || 0).toLocaleString()} LKR</span>
                </div>
              </div>
            </div>
          </div>
        );
      case 'stay_food':
        return (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h3 className="text-xl font-bold mb-4 font-serif flex items-center gap-2"><Home size={24} className="text-orange-500" /> Accommodation</h3>
              <div className="space-y-4">
                {accommodations.map((acc, i) => {
                  const price = acc.estimated_price_per_night_lkr || acc.price_per_night || acc.price || acc.price_information?.estimated_cost_per_night_lkr || acc.price_information?.estimated_price_per_night_lkr;
                  return (
                  <div key={i} className="bg-white rounded-2xl p-5 border border-orange-200 shadow-sm relative overflow-hidden">
                    <div className="absolute top-0 right-0 bg-orange-500 text-white text-xs font-bold px-3 py-1 rounded-bl-lg">SELECTED</div>
                    <p className="text-sm font-bold text-orange-600 mb-1">{acc.city}</p>
                    <h4 className="font-bold text-lg">{acc.name || acc.hotel_name}</h4>
                    {acc.recommendation_reasons && acc.recommendation_reasons.length > 0 && (
                      <p className="text-sm text-[#78716C] mt-2 mb-3">{acc.recommendation_reasons[0]}</p>
                    )}
                    {price && price > 0 ? (
                      <p className="font-bold">{price.toLocaleString()} LKR <span className="font-normal text-sm text-[#78716C]">/ night</span></p>
                    ) : (
                      <p className="text-sm font-medium text-[#78716C] italic mt-2">Estimated price unavailable</p>
                    )}
                  </div>
                )})}
                {accommodations.length === 0 && (
                  <p className="text-sm text-[#78716C] italic">No accommodations selected.</p>
                )}
              </div>
            </div>
            
            <div>
              <h3 className="text-xl font-bold mb-4 font-serif flex items-center gap-2"><Utensils size={24} className="text-orange-500" /> Dining Options</h3>
              <div className="space-y-4">
                {foodOptions.map((food, i) => (
                  <div key={i} className="bg-white rounded-2xl p-5 border border-stone-200">
                    <p className="text-sm font-bold text-orange-600 mb-1">{food.city}</p>
                    <h4 className="font-bold text-lg">{food.place_name || food.restaurant_name}</h4>
                    {food.estimated_cost_per_person_lkr && (
                      <p className="text-sm text-[#78716C] mt-1 capitalize">Est. {food.estimated_cost_per_person_lkr.toLocaleString()} LKR / person</p>
                    )}
                    {food.reasoning && (
                      <p className="text-sm text-[#78716C] mt-2 italic">"{food.reasoning}"</p>
                    )}
                  </div>
                ))}
                {foodOptions.length === 0 && (
                  <p className="text-sm text-[#78716C] italic">No dining options found.</p>
                )}
              </div>
            </div>
          </div>
        );
      case 'info':
        return (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl p-6 border border-stone-200">
              <h3 className="font-bold text-lg mb-4 flex items-center gap-2"><AlertTriangle className="text-orange-500"/> Regional Safety Risk</h3>
              <div className="flex items-center justify-between mb-4 pb-4 border-b border-stone-100">
                <span className="font-bold text-[#1C1917]">Overall Risk Level</span>
                <span className={`px-4 py-1 rounded-full text-xs font-bold capitalize ${
                  safety.risk_level === 'low' ? 'bg-green-100 text-green-700' :
                  safety.risk_level === 'medium' ? 'bg-orange-100 text-orange-700' : 'bg-red-100 text-red-700'
                }`}>{safety.risk_level || 'Unknown'}</span>
              </div>
              {safety.recommendations?.length > 0 && (
                <div className="mt-4">
                  <p className="font-bold text-sm mb-2 text-[#1C1917]">Safety Recommendations:</p>
                  <ul className="list-disc pl-5 space-y-2 text-sm text-[#78716C]">
                    {safety.recommendations.map((rec, i) => (
                      <li key={i}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
            
            {context.context_alerts?.length > 0 && (
              <div className="bg-orange-50 rounded-2xl p-6 border border-orange-200 text-orange-900">
                <h3 className="font-bold text-lg mb-3 flex items-center gap-2"><Info /> Travel Context Alerts</h3>
                <ul className="list-disc pl-5 space-y-2">
                  {context.context_alerts.map((alert, i) => (
                    <li key={i}>{alert.message || alert}</li>
                  ))}
                </ul>
              </div>
            )}
            
            {context.crowd_predictions?.length > 0 && (
              <div className="bg-white rounded-2xl p-6 border border-stone-200">
                <h3 className="font-bold text-lg mb-4 flex items-center gap-2"><Info className="text-blue-500"/> Crowd Predictions</h3>
                <div className="space-y-3">
                  {context.crowd_predictions.map((cp, i) => (
                    <div key={i} className="flex flex-col text-sm border-b border-stone-100 pb-3 last:border-0 last:pb-0">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-bold text-[#1C1917]">{cp.location}</span>
                        <span className={`font-bold capitalize ${
                          cp.crowd_level === 'LOW' ? 'text-green-600' : 
                          cp.crowd_level === 'MEDIUM' ? 'text-orange-500' : 'text-red-500'
                        }`}>{cp.crowd_level.replace('_', ' ').toLowerCase()} Crowd</span>
                      </div>
                      {cp.reasons && cp.reasons.length > 0 && (
                        <p className="text-[#57534E] text-xs mt-1 mb-1">
                          <span className="font-medium text-[#78716C]">Reason:</span> {cp.reasons.join(', ')}
                        </p>
                      )}
                      {cp.recommendations && cp.recommendations.length > 0 && (
                        <p className="text-[#57534E] text-xs">
                          <span className="font-medium text-[#78716C]">Best time:</span> {cp.recommendations[0]}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-[#FFFCF8] text-[#1C1917] font-sans selection:bg-orange-100 pb-20">
      
      {/* Workspace Header */}
      <header className="relative w-full h-[35vh] min-h-[300px] bg-[#0E1512] flex flex-col justify-between pt-6 px-4 md:px-8">
        <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1588668214407-6ea9a6d8c272?q=80&w=2071&auto=format&fit=crop')] bg-cover bg-center opacity-30 mix-blend-overlay"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-[#0E1512] via-transparent to-transparent"></div>
        
        <div className="relative z-10 flex justify-between items-center w-full max-w-7xl mx-auto">
          <Link to="/dashboard" className="text-white/80 hover:text-white flex items-center gap-2 transition-colors font-medium backdrop-blur-sm bg-black/20 px-4 py-2 rounded-full border border-white/10">
            <ChevronLeft size={18} /> Dashboard
          </Link>
          <span className={`text-sm font-bold px-3 py-1 rounded-full border backdrop-blur-md ${
            trip.status === 'CANCELLED' 
              ? 'bg-red-500/20 text-red-400 border-red-500/20' 
              : 'bg-orange-500/20 text-orange-400 border-orange-500/20'
          }`}>
            {trip.status}
          </span>
        </div>

        <div className="relative z-10 w-full max-w-7xl mx-auto pb-8">
          <div className="flex flex-wrap items-center gap-3 mb-3 text-stone-300 text-sm font-medium">
            <span className="flex items-center gap-1"><Calendar size={14} /> {trip.start_date || profile.start_date ? new Date(trip.start_date || profile.start_date).toLocaleDateString() : 'Dates TBD'}</span>
            <span>•</span>
            <span>{duration} Days</span>
            <span>•</span>
            <span className="capitalize">{profile.travel_type || 'Couple'}</span>
          </div>
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
            <div>
              <h1 className="text-4xl md:text-5xl font-bold text-white mb-2 font-serif tracking-tight">
                {trip.trip_name || 'Sri Lanka Escape'}
              </h1>
              <p className="text-lg text-stone-300 font-light max-w-2xl flex items-center gap-2">
                <MapPin size={16} className="text-orange-500" /> {routeSummary}
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-3">
              {trip.status !== 'CANCELLED' && (
                <>
                  <Link to="/plan-trip" className="px-5 py-2.5 rounded-full bg-white/10 hover:bg-white/20 text-white backdrop-blur-md border border-white/20 text-sm font-semibold transition-all">
                    Edit Plan
                  </Link>
                  <button className="px-5 py-2.5 rounded-full bg-white/10 hover:bg-white/20 text-white backdrop-blur-md border border-white/20 text-sm font-semibold transition-all">
                    Replan Trip
                  </button>
                  <button 
                    onClick={() => setShowCancelModal(true)}
                    className="px-5 py-2.5 rounded-full bg-red-500/20 hover:bg-red-500/40 text-red-100 backdrop-blur-md border border-red-500/30 text-sm font-semibold transition-all">
                    Cancel Trip
                  </button>
                </>
              )}
            </div>
          </div>
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
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        {renderTabContent()}
      </main>

      {/* Cancel Confirmation Modal */}
      {showCancelModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full shadow-xl">
            <h3 className="text-xl font-bold text-[#1C1917] mb-2 font-serif">Cancel Trip</h3>
            <p className="text-[#78716C] mb-6">Are you sure you want to cancel this trip? You will still be able to view the itinerary, but you won't be able to edit it.</p>
            <div className="flex gap-3 justify-end">
              <button 
                onClick={() => setShowCancelModal(false)}
                disabled={isCancelling}
                className="px-5 py-2.5 rounded-xl font-medium text-[#78716C] hover:bg-stone-100 transition-colors disabled:opacity-50"
              >
                Keep Trip
              </button>
              <button 
                onClick={handleCancelTrip}
                disabled={isCancelling}
                className="px-5 py-2.5 rounded-xl font-medium bg-red-500 text-white hover:bg-red-600 transition-colors disabled:opacity-50 flex items-center gap-2"
              >
                {isCancelling ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    Cancelling...
                  </>
                ) : (
                  'Yes, Cancel Trip'
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
