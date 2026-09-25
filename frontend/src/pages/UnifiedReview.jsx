import { useLocation, useNavigate, Link } from 'react-router-dom';
import { ChevronLeft, Edit2, Sparkles } from 'lucide-react';

const Section = ({ title, onEdit, children }) => (
  <div className="bg-white border border-[#EAE2D6] rounded-3xl p-6 md:p-8 shadow-sm mb-6 relative group">
    <div className="flex items-center justify-between mb-4">
      <h3 className="text-lg font-bold text-[#1C1917]">{title}</h3>
      <button onClick={onEdit} className="text-[#78716C] hover:text-orange-500 transition-colors p-1 opacity-0 group-hover:opacity-100 focus:opacity-100 flex items-center gap-1 text-sm">
        <Edit2 size={14} /> Edit
      </button>
    </div>
    <div>{children}</div>
  </div>
);

export default function UnifiedReview() {
  const location = useLocation();
  const navigate = useNavigate();
  const profileState = location.state?.profileState;

  if (!profileState) {
    return (
      <div className="min-h-screen bg-[#FFFCF8] flex items-center justify-center flex-col gap-4">
        <p className="text-[#57534E]">No trip profile found.</p>

        <Link
          to="/plan-trip"
          className="text-orange-500 font-medium"
        >
          Start Planning
        </Link>
      </div>
    );
  }

  const profile = profileState.traveller_profile;
  const planningPreferences = profileState.planning_preferences;

  if (!planningPreferences) {
    return (
      <div className="min-h-screen bg-[#FFFCF8] flex items-center justify-center flex-col gap-4">
        <p className="text-[#57534E]">No trip plan found.</p>
        <Link to="/plan-trip" className="text-orange-500 font-medium">Start Planning</Link>
      </div>
    );
  }

  const handleGenerate = async () => {
    navigate('/plan-trip/generating', { state: { profileState } });
  };

  return (
    <div className="min-h-screen bg-[#FFFCF8] text-[#1C1917] font-sans selection:bg-orange-100 flex flex-col">
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-xl border-b border-[#EAE2D6] px-6 py-4 flex items-center shadow-sm">
        <div className="w-full max-w-7xl mx-auto flex items-center justify-between">
          <button onClick={() => navigate(-1)} className="text-[#57534E] hover:text-orange-600 flex items-center gap-2 transition-colors font-medium">
            <ChevronLeft size={20} />
            Back
          </button>
          <div className="text-xl font-bold text-[#1C1917] font-serif">Review Your Trip</div>
          <div className="w-[120px]"></div>
        </div>
      </header>

      <main className="flex-1 max-w-4xl mx-auto w-full px-4 py-12 flex flex-col">
        <h1 className="text-3xl font-bold text-[#1C1917] mb-8 font-serif">Trip Summary</h1>

        <Section title="Trip Details" onEdit={() => navigate(-1)}>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">

            <div>
              <p className="text-xs text-[#78716C] uppercase tracking-wider mb-1">
                Duration
              </p>

              <p className="font-medium">
                {profile.duration_days
                  ? `${profile.duration_days} days`
                  : 'Not specified'}
              </p>
            </div>

            <div>
              <p className="text-xs text-[#78716C] uppercase tracking-wider mb-1">
                Starting Location
              </p>

              <p className="font-medium">
                {profile.starting_location || 'Not specified'}
              </p>
            </div>

            <div>
              <p className="text-xs text-[#78716C] uppercase tracking-wider mb-1">
                Travellers
              </p>

              <p className="font-medium">
                {profile.traveller_count || 'Not specified'}
              </p>
            </div>

            <div>
              <p className="text-xs text-[#78716C] uppercase tracking-wider mb-1">
                Traveller Type
              </p>

              <p className="font-medium capitalize">
                {profile.travel_type || 'Not specified'}
              </p>
            </div>

          </div>
        </Section>

        <Section title="Preferences" onEdit={() => navigate(-1)}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            <div>
              <p className="text-xs text-[#78716C] uppercase tracking-wider mb-2">
                Interests
              </p>

              <div className="flex flex-wrap gap-2">
                {profile.interests?.map((interest, i) => (
                  <span
                    key={i}
                    className="bg-[#FBF3EA] text-[#57534E] border border-[#EAE2D6] px-3 py-1 rounded-full text-sm font-medium"
                  >
                    {interest.name}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <p className="text-xs text-[#78716C] uppercase tracking-wider mb-2">
                Travel Pace
              </p>

              <p className="font-medium capitalize">
                {profile.travel_pace || 'Not specified'}
              </p>
            </div>

            <div>
              <p className="text-xs text-[#78716C] uppercase tracking-wider mb-2">
                Crowd Preference
              </p>

              <p className="font-medium capitalize">
                {profile.crowd_preference || 'Not specified'}
              </p>
            </div>

            <div>
              <p className="text-xs text-[#78716C] uppercase tracking-wider mb-2">
                Preferred Regions
              </p>

              <p className="font-medium">
                {profile.preferred_destinations?.join(', ') || 'Any'}
              </p>
            </div>

          </div>
        </Section>

        <Section title="Budget & Style" onEdit={() => navigate(-1)}>
          <div className="grid grid-cols-2 gap-4">

            <div>
              <p className="text-xs text-[#78716C] uppercase tracking-wider mb-1">
                Budget
              </p>

              <p className="font-medium">
                {profile.budget?.amount
                  ? `${profile.budget.amount} ${profile.budget.currency || ''}`
                  : 'Not specified'}

                {profile.budget?.flexibility && (
                  <span className="text-sm text-[#78716C] font-normal">
                    {' '}({profile.budget.flexibility})
                  </span>
                )}
              </p>
            </div>

            <div>
              <p className="text-xs text-[#78716C] uppercase tracking-wider mb-1">
                Travel Style
              </p>

              <p className="font-medium capitalize">
                {planningPreferences?.travel_style || 'Not specified'}
              </p>
            </div>

          </div>
        </Section>

        <Section
          title="Accommodation & Transport"
          onEdit={() => navigate(-1)}
        >
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            <div>
              <p className="text-xs text-[#78716C] uppercase tracking-wider mb-2">
                Stays
              </p>

              <p className="font-medium">
                {planningPreferences?.accommodation_preferences?.join(', ') || 'Any'}
              </p>
            </div>

            <div>
              <p className="text-xs text-[#78716C] uppercase tracking-wider mb-2">
                Transport
              </p>

              <p className="font-medium">
                {planningPreferences?.transport_preferences?.join(', ') || 'Any'}
              </p>
            </div>

          </div>
        </Section>

        <div className="sticky bottom-8 mt-12 w-full max-w-md mx-auto">
          <button 
            onClick={handleGenerate}
            className="w-full bg-orange-500 text-white py-4 rounded-xl font-bold hover:bg-orange-600 transition-all shadow-lg hover:shadow-xl hover:-translate-y-1 flex items-center justify-center gap-2 text-lg"
          >
            <Sparkles size={22} /> GENERATE MY TRIP
          </button>
        </div>
      </main>
    </div>
  );
}
