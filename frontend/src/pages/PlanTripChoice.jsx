import { Link } from 'react-router-dom';
import { Sparkles, Compass, ChevronLeft } from 'lucide-react';

export default function PlanTripChoice() {
  return (
    <div className="min-h-screen bg-[#FFFCF8] text-[#1C1917] font-sans selection:bg-orange-100 flex flex-col">
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-xl border-b border-[#EAE2D6] px-6 py-4 flex items-center shadow-sm">
        <div className="w-full max-w-7xl mx-auto flex items-center justify-between">
          <Link to="/dashboard" className="text-[#57534E] hover:text-orange-600 flex items-center gap-2 transition-colors font-medium">
            <ChevronLeft size={20} />
            Back to Dashboard
          </Link>
          <div className="text-xl font-bold text-[#1C1917] font-serif">Serendib AI Planner</div>
          <div className="w-[120px]"></div> {/* Spacer for center alignment */}
        </div>
      </header>

      <main className="flex-1 max-w-5xl mx-auto w-full px-4 py-16 flex flex-col items-center justify-center">
        <h1 className="text-4xl md:text-5xl font-bold text-[#1C1917] mb-4 text-center font-serif">
          How would you like to plan?
        </h1>
        <p className="text-lg text-[#78716C] mb-12 text-center max-w-2xl">
          Choose between our AI-powered natural language planner or build your journey step by step.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-4xl">
          
          {/* Tell Serendib AI */}
          <div className="bg-white border border-[#EAE2D6] rounded-3xl p-8 shadow-sm hover:shadow-xl hover:border-orange-300 hover:-translate-y-1 transition-all flex flex-col group h-full">
            <div className="w-16 h-16 bg-orange-50 rounded-2xl flex items-center justify-center text-orange-500 mb-6 group-hover:scale-110 transition-transform shadow-sm">
              <Sparkles size={32} />
            </div>
            <h2 className="text-2xl font-bold text-[#1C1917] mb-3">✨ Tell Serendib AI</h2>
            <p className="text-[#57534E] mb-8 flex-1">
              Describe your ideal Sri Lanka trip naturally and let Serendib AI understand your travel needs and build the perfect journey.
            </p>
            <Link to="/plan-trip/nlp" className="w-full bg-orange-500 text-white text-center py-3.5 rounded-xl font-semibold shadow-sm hover:bg-orange-600 transition-colors">
              Tell Serendib AI
            </Link>
          </div>

          {/* Guided Planner */}
          <div className="bg-white border border-[#EAE2D6] rounded-3xl p-8 shadow-sm hover:shadow-xl hover:border-orange-300 hover:-translate-y-1 transition-all flex flex-col group h-full">
            <div className="w-16 h-16 bg-[#FBF3EA] rounded-2xl flex items-center justify-center text-orange-600 mb-6 group-hover:scale-110 transition-transform shadow-sm">
              <Compass size={32} />
            </div>
            <h2 className="text-2xl font-bold text-[#1C1917] mb-3">🧭 Guided Planner</h2>
            <p className="text-[#57534E] mb-8 flex-1">
              Build your journey step by step with complete control over your preferences, budget, accommodation, and activities.
            </p>
            <Link to="/plan-trip/guided" className="w-full bg-white border border-[#EAE2D6] text-[#1C1917] text-center py-3.5 rounded-xl font-semibold hover:border-orange-300 hover:bg-orange-50 transition-colors shadow-sm">
              Start Guided Planning
            </Link>
          </div>

        </div>
      </main>
    </div>
  );
}
