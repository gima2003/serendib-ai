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

  // Agent 1 state
  const [profile, setProfile] = useState(null);
  const [profileReady, setProfileReady] = useState(false);
  const [clarification, setClarification] = useState(null);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [permissionGiven, setPermissionGiven] = useState(null);
  const [chatInput, setChatInput] = useState('');

  const handleUnderstandTrip = async () => {
    if (!text.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await tripService.parseNaturalLanguageTrip(text);

      // Store the profile returned by Agent 1.
      setParsedPlan(response.profile);

      // Check whether Agent 1 considers the profile complete.
      if (response.status === 'ready') {
        setProfileReady(true);
        setClarification(null);
      } else {
        setProfileReady(false);
        setClarification(response.assistant);
      }

    } catch (err) {
      console.error(err);

      setError(
        'Serendib AI is currently unavailable. Please try again later.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleClarificationPermission = async (userResponse) => {
    if (!parsedPlan) return;

    try {
      setIsLoading(true);
      setError(null);

      const response =
        await tripService.requestClarificationPermission(
          userResponse,
          parsedPlan,
          {
            ready: profileReady,
            missing_context: clarification?.current_context
              ? [clarification.current_context]
              : [],
          }
        );

      if (response.status === 'needs_clarification') {
        setPermissionGiven(true);
        setClarification(response.assistant);
        setIsChatOpen(true);
      } else if (response.status === 'ready') {
        setPermissionGiven(false);
        setClarification(null);
        setProfileReady(true);
        setIsChatOpen(false);
      } else {
        setPermissionGiven(null);
        setClarification(response.assistant);
      }

    } catch (err) {
      console.error(err);
      setError(
        'Unable to process your response. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleClarificationAnswer = async () => {
    if (!chatInput.trim() || !clarification?.current_context || !parsedPlan) {
      return;
    }

    try {
      setIsLoading(true);
      setError(null);

      const response = await tripService.submitClarificationAnswer(
        chatInput,
        clarification.current_context,
        parsedPlan
      );

      // Update the profile with Agent 1's latest version.
      setParsedPlan(response.profile);

      if (response.status === 'ready') {
        // All required information has been collected.
        setProfileReady(true);
        setClarification(null);
        setIsChatOpen(false);
        setPermissionGiven(null);
      } else if (response.status === 'needs_clarification') {
        // Agent 1 still needs more information.
        setProfileReady(false);
        setClarification(response.assistant);
      }

      setChatInput('');
    } catch (err) {
      console.error(err);
      setError(
        'Unable to process your answer. Please try again.'
      );
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
          <button onClick={() => {
                if (parsedPlan) {
                  setParsedPlan(null);
                  setProfileReady(false);
                  setClarification(null);
                  setPermissionGiven(null);
                  setIsChatOpen(false);
                } else {
                  navigate('/plan-trip');
                }
              }} className="text-[#57534E] hover:text-orange-600 flex items-center gap-2 transition-colors font-medium">
            <ChevronLeft size={20} />
            {parsedPlan ? 'Back to Editor' : 'Back to Choices'}
          </button>
          <div className="text-xl font-bold text-[#1C1917] font-serif">✨ Tell Serendib AI</div>
          <div className="w-[120px]"></div>
        </div>
      </header>

      <main className="flex-1 max-w-3xl mx-auto w-full px-4 py-12 flex flex-col">
        {!parsedPlan || !profileReady ? (
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
                  <p className="font-medium text-[#1C1917]">{parsedPlan.duration_days
                    ? `${parsedPlan.duration_days} days`
                    : 'Not specified'}</p>
                </div>
                <div className="bg-[#FBF3EA] p-4 rounded-xl border border-[#EAE2D6]">
                  <p className="text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-1">Travellers</p>
                  <p className="font-medium text-[#1C1917]">{parsedPlan.traveller_count
                    ? `${parsedPlan.traveller_count} · ${parsedPlan.travel_type || ''}`
                    : 'Not specified'}</p>
                </div>
                <div className="bg-[#FBF3EA] p-4 rounded-xl border border-[#EAE2D6]">
                  <p className="text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-1">Budget</p>
                  <p className="font-medium text-[#1C1917]">{parsedPlan.budget
                    ? `${parsedPlan.budget.amount} ${parsedPlan.budget.currency}`
                    : 'Not specified'}</p>
                </div>
                <div className="bg-[#FBF3EA] p-4 rounded-xl border border-[#EAE2D6]">
                  <p className="text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-1">Pace</p>
                  <p className="font-medium text-[#1C1917]">{parsedPlan.travel_pace || 'Not specified'}</p>
                </div>
              </div>

              <div>
                <p className="text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-2">Interests</p>
                <div className="flex flex-wrap gap-2">
                  {parsedPlan.interests.map((interest, i) => (
                    <span key={i} className="bg-orange-50 text-orange-700 border border-orange-200 px-3 py-1 rounded-full text-sm font-medium">
                      {interest.name}
                    </span>
                  ))}
                </div>
              </div>

              {parsedPlan.additional_requests?.length > 0 && (
                <div>
                  <p className="text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-1">Notes</p>
                  <p className="text-sm text-[#57534E] italic">"{parsedPlan.additional_requests.join(', ')}"</p>
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
      {clarification && !profileReady && (
        <button
          onClick={() => setIsChatOpen(true)}
          className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-orange-500 text-white shadow-lg hover:bg-orange-600 transition-all flex items-center justify-center z-50"
          aria-label="Open Serendib AI assistant"
        >
          <Sparkles size={24} />
        </button>
      )}
      {isChatOpen && clarification && !profileReady && (
        <div className="fixed bottom-24 right-6 w-[360px] max-w-[calc(100vw-2rem)] bg-white border border-[#EAE2D6] rounded-2xl shadow-xl z-50 overflow-hidden">

          <div className="bg-[#FBF3EA] border-b border-[#EAE2D6] px-4 py-3 flex items-center justify-between">
            <div>
              <p className="font-semibold text-[#1C1917]">
                Serendib AI
              </p>
              <p className="text-xs text-[#78716C]">
                Personalizing your trip
              </p>
            </div>

            <button
              onClick={() => setIsChatOpen(false)}
              className="text-[#78716C] hover:text-[#1C1917]"
            >
              ×
            </button>
          </div>

          <div className="p-4">
            <div className="bg-[#F5F5F4] rounded-xl p-3 mb-4">
              <p className="text-sm text-[#44403C]">
                {clarification.message}
              </p>
            </div>

            {permissionGiven === null && (
              <div className="flex gap-2">
                <button
                  onClick={() => handleClarificationPermission('yes')}
                  disabled={isLoading}
                  className="flex-1 bg-orange-500 text-white py-2 rounded-lg font-medium hover:bg-orange-600 disabled:opacity-50"
                >
                  Yes
                </button>

                <button
                  onClick={() => handleClarificationPermission('no')}
                  disabled={isLoading}
                  className="flex-1 border border-[#EAE2D6] py-2 rounded-lg font-medium hover:bg-[#FBF3EA] disabled:opacity-50"
                >
                  No
                </button>
              </div>
            )}
            {permissionGiven === true && clarification?.current_context && (
              <div className="flex gap-2">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      handleClarificationAnswer();
                    }
                  }}
                  placeholder="Type your answer..."
                  disabled={isLoading}
                  className="flex-1 border border-[#EAE2D6] rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-200"
                />

                <button
                  onClick={handleClarificationAnswer}
                  disabled={!chatInput.trim() || isLoading}
                  className="bg-orange-500 text-white px-4 py-2 rounded-lg font-medium hover:bg-orange-600 disabled:opacity-50"
                >
                  Send
                </button>
              </div>
            )}

          </div>
        </div>
      )}
    </div>
  );
}
