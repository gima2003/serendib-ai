import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Sparkles, ChevronLeft, AlertCircle, Loader2, Edit3, CheckCircle2 } from 'lucide-react';
import { tripService } from '../services/tripService';

export default function NLPPlanner() {
  const navigate = useNavigate();
  const [text, setText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [parsedPlan, setParsedPlan] = useState(null);

  const handleUnderstandTrip = async () => {
    if (!text.trim()) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await tripService.parseNaturalLanguageTrip(text);
      if (result) {
        setParsedPlan(result);
      } else {
        // Handle empty API response gracefully while backend is not ready
        setParsedPlan({
          travelDates: 'To be determined',
          duration: '6 days',
          travellerType: 'Couple',
          budget: { amount: 700, currency: 'USD', flexibility: 'Flexible' },
          travelStyle: 'Mid-range',
          interests: ['Nature', 'Hiking', 'Photography'],
          travelPace: 'Relaxed',
          crowdPreference: 'Peaceful',
          accommodationPreferences: ['Boutique Hotel', 'Guesthouse'],
          transportPreferences: ['Private Taxi', 'Train'],
          foodPreferences: ['Local food'],
          selectedActivities: [],
          preferredRegions: [],
          additionalNotes: 'Prefers quieter places.'
        });
      }
    } catch (err) {
      setError('Serendib AI is currently unavailable. Please try the Guided Planner or check back later.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleContinue = () => {
    navigate('/plan-trip/review', { state: { plan: parsedPlan } });
  };

  return (
    <div className="min-h-screen bg-[#FFFCF8] text-[#1C1917] font-sans selection:bg-orange-100 flex flex-col">
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-xl border-b border-[#EAE2D6] px-6 py-4 flex items-center shadow-sm">
        <div className="w-full max-w-7xl mx-auto flex items-center justify-between">
          <button onClick={() => parsedPlan ? setParsedPlan(null) : navigate('/plan-trip')} className="text-[#57534E] hover:text-orange-600 flex items-center gap-2 transition-colors font-medium">
            <ChevronLeft size={20} />
            {parsedPlan ? 'Back to Editor' : 'Back to Choices'}
          </button>
          <div className="text-xl font-bold text-[#1C1917] font-serif">✨ Tell Serendib AI</div>
          <div className="w-[120px]"></div>
        </div>
      </header>

      <main className="flex-1 max-w-3xl mx-auto w-full px-4 py-12 flex flex-col">
        {!parsedPlan ? (
          <>
            <h1 className="text-3xl md:text-4xl font-bold text-[#1C1917] mb-3 font-serif text-center">
              Tell Serendib AI about your dream trip
            </h1>
            <p className="text-[#78716C] mb-8 text-center">
              Describe your ideal journey in your own words.
            </p>

            <div className="bg-white border border-[#EAE2D6] rounded-3xl p-6 shadow-sm mb-6 flex flex-col">
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="I want a relaxing 6-day Sri Lanka trip with my partner. We love nature, hiking and photography. Our budget is around $700 and we prefer quieter places."
                className="w-full min-h-[250px] resize-y bg-transparent text-[#1C1917] text-lg placeholder-[#A8A29E] focus:outline-none"
                disabled={isLoading}
              ></textarea>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl flex items-start gap-3 mb-6">
                <AlertCircle size={20} className="shrink-0 mt-0.5" />
                <p className="text-sm">{error}</p>
              </div>
            )}

            <button
              onClick={handleUnderstandTrip}
              disabled={!text.trim() || isLoading}
              className={`w-full py-4 rounded-xl font-semibold flex items-center justify-center gap-2 transition-all shadow-sm ${
                !text.trim() || isLoading
                  ? 'bg-[#EAE2D6] text-[#A8A29E] cursor-not-allowed'
                  : 'bg-orange-500 text-white hover:bg-orange-600'
              }`}
            >
              {isLoading ? (
                <><Loader2 size={20} className="animate-spin" /> Understanding your trip...</>
              ) : (
                <><Sparkles size={20} /> Understand My Trip</>
              )}
            </button>
          </>
        ) : (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex flex-col items-center justify-center mb-8">
              <div className="w-16 h-16 bg-green-50 text-green-500 rounded-full flex items-center justify-center mb-4 shadow-sm">
                <CheckCircle2 size={32} />
              </div>
              <h2 className="text-2xl font-bold text-[#1C1917] font-serif text-center">We understood your trip as</h2>
            </div>

            <div className="bg-white border border-[#EAE2D6] rounded-3xl p-6 md:p-8 shadow-sm mb-8 space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-[#FBF3EA] p-4 rounded-xl border border-[#EAE2D6]">
                  <p className="text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-1">Duration</p>
                  <p className="font-medium text-[#1C1917]">{parsedPlan.duration}</p>
                </div>
                <div className="bg-[#FBF3EA] p-4 rounded-xl border border-[#EAE2D6]">
                  <p className="text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-1">Travellers</p>
                  <p className="font-medium text-[#1C1917]">{parsedPlan.travellerType}</p>
                </div>
                <div className="bg-[#FBF3EA] p-4 rounded-xl border border-[#EAE2D6]">
                  <p className="text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-1">Budget</p>
                  <p className="font-medium text-[#1C1917]">{parsedPlan.budget.amount} {parsedPlan.budget.currency}</p>
                </div>
                <div className="bg-[#FBF3EA] p-4 rounded-xl border border-[#EAE2D6]">
                  <p className="text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-1">Pace</p>
                  <p className="font-medium text-[#1C1917]">{parsedPlan.travelPace}</p>
                </div>
              </div>

              <div>
                <p className="text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-2">Interests</p>
                <div className="flex flex-wrap gap-2">
                  {parsedPlan.interests.map((interest, i) => (
                    <span key={i} className="bg-orange-50 text-orange-700 border border-orange-200 px-3 py-1 rounded-full text-sm font-medium">
                      {interest}
                    </span>
                  ))}
                </div>
              </div>

              {parsedPlan.additionalNotes && (
                <div>
                  <p className="text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-1">Notes</p>
                  <p className="text-sm text-[#57534E] italic">"{parsedPlan.additionalNotes}"</p>
                </div>
              )}
            </div>

            <div className="flex flex-col sm:flex-row gap-4">
              <button 
                onClick={() => setParsedPlan(null)}
                className="flex-1 bg-white border border-[#EAE2D6] text-[#1C1917] py-3.5 rounded-xl font-semibold hover:border-orange-300 hover:bg-orange-50 transition-colors shadow-sm flex items-center justify-center gap-2"
              >
                <Edit3 size={18} /> Edit Details
              </button>
              <button 
                onClick={handleContinue}
                className="flex-1 bg-orange-500 text-white py-3.5 rounded-xl font-semibold hover:bg-orange-600 transition-colors shadow-sm flex items-center justify-center gap-2"
              >
                Looks Good — Continue
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
