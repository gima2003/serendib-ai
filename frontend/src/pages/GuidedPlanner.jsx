import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, ChevronRight, Check } from 'lucide-react';
import SearchableDropdown from '../components/SearchableDropdown';

const StepIndicator = ({ currentStep, totalSteps }) => (
  <div className="w-full mb-12">
    <div className="flex items-center justify-between relative">
      <div className="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-[#EAE2D6] rounded-full z-0"></div>
      <div 
        className="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-orange-500 rounded-full z-0 transition-all duration-500" 
        style={{ width: `${((currentStep - 1) / totalSteps) * 100}%` }}
      ></div>
      
      {[1, 2, 3, 4, 5].map((step) => {
        const isActive = step === currentStep;
        const isCompleted = step < currentStep;
        return (
          <div key={step} className="relative z-10 flex flex-col items-center gap-2">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm transition-colors ${
              isActive ? 'bg-orange-500 text-white shadow-md' : 
              isCompleted ? 'bg-orange-100 text-orange-600' : 
              'bg-white border-2 border-[#EAE2D6] text-[#A8A29E]'
            }`}>
              {isCompleted ? <Check size={18} /> : step}
            </div>
            <span className={`text-xs font-semibold hidden md:block ${isActive ? 'text-[#1C1917]' : 'text-[#A8A29E]'}`}>
              {step === 1 && 'Details'}
              {step === 2 && 'Preferences'}
              {step === 3 && 'Budget'}
              {step === 4 && 'Food & Acts'}
              {step === 5 && 'Review'}
            </span>
          </div>
        );
      })}
    </div>
  </div>
);

const SelectionChip = ({ selected, onClick, children }) => (
  <button
    onClick={onClick}
    className={`px-4 py-2.5 rounded-full text-sm font-medium border transition-all ${
      selected 
        ? 'bg-orange-50 border-orange-400 text-orange-700 shadow-sm' 
        : 'bg-white border-[#EAE2D6] text-[#57534E] hover:border-orange-300 hover:bg-[#FBF3EA]'
    }`}
  >
    {children}
  </button>
);

export default function GuidedPlanner() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const totalSteps = 4;

  const [plan, setPlan] = useState({
    origin: '',
    startDate: '',
    endDate: '',
    travellerCount: 2,
    travellerType: 'Couple',
    interests: [],
    travelPace: 'Balanced',
    crowdPreference: 'Balanced',
    preferredRegions: [],
    additionalNotes: '',
    budget: { amount: '', currency: 'USD', flexibility: 'Moderate' },
    travelStyle: 'Mid-range',
    accommodationPreferences: [],
    transportPreferences: [],
    dietaryPreference: 'No restriction',
    foodPreferences: [],
    selectedActivities: []
  });

  const updatePlan = (key, value) => {
    setPlan(prev => ({ ...prev, [key]: value }));
  };

  const updateBudget = (key, value) => {
    setPlan(prev => ({ ...prev, budget: { ...prev.budget, [key]: value } }));
  };

  const toggleArrayItem = (key, item) => {
    setPlan(prev => {
      const array = prev[key];
      if (array.includes(item)) {
        return { ...prev, [key]: array.filter(i => i !== item) };
      } else {
        return { ...prev, [key]: [...array, item] };
      }
    });
  };

  const nextStep = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(curr => curr + 1);
    } else {
      const reviewPlan = {
        ...plan,
        duration: plan.startDate && plan.endDate ? `${Math.ceil((new Date(plan.endDate) - new Date(plan.startDate)) / (1000 * 60 * 60 * 24))} days` : 'Not specified',
        travelDates: `${plan.startDate} to ${plan.endDate}`
      };
      navigate('/plan-trip/review', { state: { plan: reviewPlan } });
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(curr => curr - 1);
    } else {
      navigate('/plan-trip');
    }
  };

  const renderStepContent = () => {
    switch(currentStep) {
      case 1:
        return (
          <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-300">
            <div>
              <h2 className="text-2xl font-bold text-[#1C1917] font-serif mb-2">Trip Details</h2>
              <p className="text-[#78716C]">Let's start with the basics of your journey.</p>
            </div>
            
            <div className="bg-white border border-[#EAE2D6] rounded-3xl p-6 md:p-8 shadow-sm space-y-6">
              <div>
                <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-2">Where are you travelling from?</label>
                <input 
                  type="text" 
                  value={plan.origin}
                  onChange={(e) => updatePlan('origin', e.target.value)}
                  placeholder="e.g. London, UK" 
                  className="w-full bg-[#FBF3EA]/50 border border-[#EAE2D6] focus:border-orange-400 rounded-xl px-4 py-3 text-[#1C1917] transition-colors outline-none"
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-2">Start Date</label>
                  <input 
                    type="date" 
                    value={plan.startDate}
                    onChange={(e) => updatePlan('startDate', e.target.value)}
                    className="w-full bg-[#FBF3EA]/50 border border-[#EAE2D6] focus:border-orange-400 rounded-xl px-4 py-3 text-[#1C1917] transition-colors outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-2">End Date</label>
                  <input 
                    type="date" 
                    value={plan.endDate}
                    onChange={(e) => updatePlan('endDate', e.target.value)}
                    className="w-full bg-[#FBF3EA]/50 border border-[#EAE2D6] focus:border-orange-400 rounded-xl px-4 py-3 text-[#1C1917] transition-colors outline-none"
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-2">Number of Travellers</label>
                  <input 
                    type="number" 
                    min="1"
                    value={plan.travellerCount}
                    onChange={(e) => updatePlan('travellerCount', parseInt(e.target.value) || 1)}
                    className="w-full bg-[#FBF3EA]/50 border border-[#EAE2D6] focus:border-orange-400 rounded-xl px-4 py-3 text-[#1C1917] transition-colors outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-2">Travelling As</label>
                  <select 
                    value={plan.travellerType}
                    onChange={(e) => updatePlan('travellerType', e.target.value)}
                    className="w-full bg-[#FBF3EA]/50 border border-[#EAE2D6] focus:border-orange-400 rounded-xl px-4 py-3 text-[#1C1917] transition-colors outline-none"
                  >
                    <option>Solo</option>
                    <option>Couple</option>
                    <option>Family</option>
                    <option>Friends / Group</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        );
      case 2:
        return (
          <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-300">
            <div>
              <h2 className="text-2xl font-bold text-[#1C1917] font-serif mb-2">Traveller Preferences</h2>
              <p className="text-[#78716C]">What kind of experiences are you looking for?</p>
            </div>
            
            <div className="bg-white border border-[#EAE2D6] rounded-3xl p-6 md:p-8 shadow-sm space-y-8">
              <div>
                <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-3">Interests</label>
                <div className="flex flex-wrap gap-3">
                  {['Nature', 'Hiking', 'Photography', 'Beach', 'Wildlife', 'Culture', 'Food', 'Adventure', 'Shopping'].map(interest => (
                    <SelectionChip 
                      key={interest} 
                      selected={plan.interests.includes(interest)} 
                      onClick={() => toggleArrayItem('interests', interest)}
                    >
                      {interest}
                    </SelectionChip>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-3">Travel Pace</label>
                  <div className="flex flex-col gap-2">
                    {['Relaxed', 'Balanced', 'Fast-paced'].map(pace => (
                      <label key={pace} className="flex items-center gap-3 p-3 border border-[#EAE2D6] rounded-xl cursor-pointer hover:bg-[#FBF3EA]">
                        <input 
                          type="radio" 
                          name="pace" 
                          checked={plan.travelPace === pace}
                          onChange={() => updatePlan('travelPace', pace)}
                          className="text-orange-500 focus:ring-orange-500"
                        />
                        <span className="text-[#57534E] text-sm font-medium">{pace}</span>
                      </label>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-3">Crowd Preference</label>
                  <div className="flex flex-col gap-2">
                    {['Peaceful / quieter places', 'Balanced', 'Popular attractions'].map(crowd => (
                      <label key={crowd} className="flex items-center gap-3 p-3 border border-[#EAE2D6] rounded-xl cursor-pointer hover:bg-[#FBF3EA]">
                        <input 
                          type="radio" 
                          name="crowd" 
                          checked={plan.crowdPreference === crowd}
                          onChange={() => updatePlan('crowdPreference', crowd)}
                          className="text-orange-500 focus:ring-orange-500"
                        />
                        <span className="text-[#57534E] text-sm font-medium">{crowd}</span>
                      </label>
                    ))}
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-3">Preferred Regions (Optional)</label>
                <div className="flex flex-wrap gap-3">
                  {['Colombo', 'Kandy', 'Ella', 'Nuwara Eliya', 'Sigiriya', 'Galle', 'Mirissa', 'Arugam Bay'].map(region => (
                    <SelectionChip 
                      key={region} 
                      selected={plan.preferredRegions.includes(region)} 
                      onClick={() => toggleArrayItem('preferredRegions', region)}
                    >
                      {region}
                    </SelectionChip>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-2">Anything else we should know?</label>
                <textarea
                  value={plan.additionalNotes}
                  onChange={(e) => updatePlan('additionalNotes', e.target.value)}
                  placeholder="I would really like a scenic train journey and prefer less crowded places."
                  className="w-full min-h-[100px] resize-y bg-[#FBF3EA]/50 border border-[#EAE2D6] focus:border-orange-400 rounded-xl px-4 py-3 text-[#1C1917] transition-colors outline-none text-sm"
                ></textarea>
              </div>
            </div>
          </div>
        );
      case 3:
        return (
          <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-300">
            <div>
              <h2 className="text-2xl font-bold text-[#1C1917] font-serif mb-2">Budget & Travel Style</h2>
              <p className="text-[#78716C]">Define how you want to travel and stay.</p>
            </div>
            
            <div className="bg-white border border-[#EAE2D6] rounded-3xl p-6 md:p-8 shadow-sm space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <SearchableDropdown
                    id="currency"
                    label="Currency"
                    value={plan.budget.currency}
                    onChange={(val) => updateBudget('currency', val)}
                    options={[
                      { code: 'USD', label: 'USD - US Dollar' },
                      { code: 'EUR', label: 'EUR - Euro' },
                      { code: 'GBP', label: 'GBP - British Pound' },
                      { code: 'AUD', label: 'AUD - Australian Dollar' },
                      { code: 'LKR', label: 'LKR - Sri Lankan Rupee' }
                    ]}
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-1.5">Estimated Budget</label>
                  <input 
                    type="number" 
                    value={plan.budget.amount}
                    onChange={(e) => updateBudget('amount', e.target.value)}
                    placeholder="e.g. 1500" 
                    className="w-full bg-[#FBF3EA]/50 border border-[#EAE2D6] focus:border-orange-400 rounded-xl px-4 py-3 text-[#1C1917] transition-colors outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-3">Budget Flexibility</label>
                <div className="flex flex-wrap gap-3">
                  {['Strict', 'Moderate', 'Flexible'].map(flex => (
                    <SelectionChip 
                      key={flex} 
                      selected={plan.budget.flexibility === flex} 
                      onClick={() => updateBudget('flexibility', flex)}
                    >
                      {flex}
                    </SelectionChip>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-3">Travel Style</label>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {[
                    { style: 'Budget', desc: 'Hostels, local food & public transport' },
                    { style: 'Mid-range', desc: 'Guesthouses, restaurants & tuk-tuks' },
                    { style: 'Luxury', desc: 'Boutique hotels, fine dining & private transfers' }
                  ].map(ts => (
                    <div 
                      key={ts.style}
                      onClick={() => updatePlan('travelStyle', ts.style)}
                      className={`p-4 rounded-xl border cursor-pointer transition-all ${
                        plan.travelStyle === ts.style 
                          ? 'bg-orange-50 border-orange-400 shadow-sm' 
                          : 'bg-white border-[#EAE2D6] hover:border-orange-300 hover:bg-[#FBF3EA]'
                      }`}
                    >
                      <h4 className={`font-bold mb-1 ${plan.travelStyle === ts.style ? 'text-orange-700' : 'text-[#1C1917]'}`}>{ts.style}</h4>
                      <p className={`text-xs ${plan.travelStyle === ts.style ? 'text-orange-600/80' : 'text-[#78716C]'}`}>{ts.desc}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-3">Accommodation Preferences</label>
                <div className="flex flex-wrap gap-3">
                  {['Hostel / Dorm', 'Guesthouse', '3-star Hotel', 'Boutique Hotel', 'Luxury Resort'].map(acc => (
                    <SelectionChip 
                      key={acc} 
                      selected={plan.accommodationPreferences.includes(acc)} 
                      onClick={() => toggleArrayItem('accommodationPreferences', acc)}
                    >
                      {acc}
                    </SelectionChip>
                  ))}
                </div>
              </div>
              
              <div>
                <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-3">Preferred Transport</label>
                <div className="flex flex-wrap gap-3">
                  {['Public Bus', 'Tuk-tuk', 'Train', 'Private Taxi', 'Private Car + Driver'].map(trans => (
                    <SelectionChip 
                      key={trans} 
                      selected={plan.transportPreferences.includes(trans)} 
                      onClick={() => toggleArrayItem('transportPreferences', trans)}
                    >
                      {trans}
                    </SelectionChip>
                  ))}
                </div>
              </div>
            </div>
          </div>
        );
      case 4:
        return (
          <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-300">
            <div>
              <h2 className="text-2xl font-bold text-[#1C1917] font-serif mb-2">Food & Activities</h2>
              <p className="text-[#78716C]">Select dietary needs and optional must-do activities.</p>
            </div>
            
            <div className="bg-white border border-[#EAE2D6] rounded-3xl p-6 md:p-8 shadow-sm space-y-8">
              <div>
                <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-3">Dietary Preference</label>
                <div className="flex flex-wrap gap-3">
                  {['No restriction', 'Vegetarian', 'Vegan', 'Halal'].map(diet => (
                    <SelectionChip 
                      key={diet} 
                      selected={plan.dietaryPreference === diet} 
                      onClick={() => updatePlan('dietaryPreference', diet)}
                    >
                      {diet}
                    </SelectionChip>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-3">Food Interests</label>
                <div className="flex flex-wrap gap-3">
                  {['Sri Lankan food', 'Street food', 'Seafood', 'Cafe experiences', 'Fine dining', 'International cuisine'].map(food => (
                    <SelectionChip 
                      key={food} 
                      selected={plan.foodPreferences.includes(food)} 
                      onClick={() => toggleArrayItem('foodPreferences', food)}
                    >
                      {food}
                    </SelectionChip>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-[#78716C] uppercase tracking-wider mb-3">Must-Include Activities (Optional)</label>
                <p className="text-xs text-[#78716C] mb-4 -mt-2">Serendib AI will recommend more activities based on your profile, but you can pin must-dos here.</p>
                <div className="flex flex-wrap gap-3">
                  {['Sigiriya Rock Fortress', 'Yala Safari', 'Whale Watching Mirissa', 'Temple of the Tooth', 'Ella Rock', 'Nine Arches Bridge', 'Surf Lesson'].map(activity => (
                    <SelectionChip 
                      key={activity} 
                      selected={plan.selectedActivities.includes(activity)} 
                      onClick={() => toggleArrayItem('selectedActivities', activity)}
                    >
                      {activity}
                    </SelectionChip>
                  ))}
                </div>
              </div>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-[#FFFCF8] text-[#1C1917] font-sans selection:bg-orange-100 flex flex-col pb-24">
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-xl border-b border-[#EAE2D6] px-6 py-4 flex items-center shadow-sm">
        <div className="w-full max-w-7xl mx-auto flex items-center justify-between">
          <button onClick={prevStep} className="text-[#57534E] hover:text-orange-600 flex items-center gap-2 transition-colors font-medium">
            <ChevronLeft size={20} />
            {currentStep === 1 ? 'Cancel' : 'Back'}
          </button>
          <div className="text-xl font-bold text-[#1C1917] font-serif">🧭 Guided Planner</div>
          <div className="w-[120px]"></div>
        </div>
      </header>

      <main className="flex-1 max-w-3xl mx-auto w-full px-4 py-8 flex flex-col">
        <StepIndicator currentStep={currentStep} totalSteps={totalSteps} />
        {renderStepContent()}
      </main>

      <div className="fixed bottom-0 left-0 w-full bg-white border-t border-[#EAE2D6] p-4 shadow-[0_-4px_20px_rgba(0,0,0,0.05)] z-40">
        <div className="max-w-3xl mx-auto flex justify-between items-center">
          <button 
            onClick={prevStep}
            className="text-[#57534E] font-medium px-4 py-2 hover:text-orange-600 transition-colors"
          >
            {currentStep === 1 ? 'Cancel' : 'Previous Step'}
          </button>
          <button 
            onClick={nextStep}
            className="bg-orange-500 text-white px-8 py-3 rounded-xl font-bold hover:bg-orange-600 transition-all shadow-sm flex items-center gap-2"
          >
            {currentStep === totalSteps ? 'Review Trip' : 'Continue'} 
            {currentStep < totalSteps && <ChevronRight size={18} />}
          </button>
        </div>
      </div>
    </div>
  );
}
