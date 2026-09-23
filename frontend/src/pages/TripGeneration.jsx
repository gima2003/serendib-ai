import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Loader2, Sparkles, Map, Building2, Car, CalendarCheck } from 'lucide-react';
import { tripService } from '../services/tripService';

export default function TripGeneration() {
  const location = useLocation();
  const navigate = useNavigate();
  const plan = location.state?.plan;
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    { icon: Sparkles, text: "Understanding your preferences" },
    { icon: Map, text: "Finding perfect destinations" },
    { icon: CalendarCheck, text: "Matching unique experiences" },
    { icon: Building2, text: "Finding stays & food" },
    { icon: Car, text: "Optimizing your route" },
  ];

  useEffect(() => {
    if (!plan) {
      navigate('/plan-trip');
      return;
    }

    // Simulate conceptual phases purely for visual engagement, 
    // NOT faking actual backend completion signals.
    const interval = setInterval(() => {
      setCurrentStep(prev => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 2000);

    const generate = async () => {
      try {
        const result = await tripService.generateTrip(plan);
        // Ensure minimum wait time for visual experience
        setTimeout(() => {
          navigate(`/trip/${result.id}`);
        }, 3000);
      } catch (err) {
        console.error("Failed to generate trip", err);
        // Ideally navigate to an error page, but for now just go back
        navigate('/plan-trip/review', { state: { plan } });
      }
    };

    generate();

    return () => clearInterval(interval);
  }, [plan, navigate, steps.length]);

  return (
    <div className="min-h-screen bg-[#0E1512] text-white font-sans flex flex-col items-center justify-center relative overflow-hidden">
      {/* Background imagery */}
      <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1546708973-b339540b5162?q=80&w=2070&auto=format&fit=crop')] bg-cover bg-center opacity-20 mix-blend-overlay"></div>
      <div className="absolute inset-0 bg-gradient-to-t from-[#0E1512] via-[#0E1512]/80 to-transparent"></div>

      <div className="relative z-10 max-w-md w-full px-6 flex flex-col items-center">
        <div className="w-20 h-20 bg-orange-500 rounded-3xl flex items-center justify-center text-white mb-8 shadow-[0_0_40px_rgba(249,115,22,0.4)] animate-pulse">
          <Sparkles size={40} />
        </div>
        
        <h1 className="text-3xl font-bold font-serif text-center mb-12">
          Serendib AI is building your Sri Lankan journey...
        </h1>

        <div className="w-full space-y-6">
          {steps.map((step, index) => {
            const isActive = index === currentStep;
            const isPast = index < currentStep;
            
            return (
              <div 
                key={index}
                className={`flex items-center gap-4 transition-all duration-700 ${
                  isActive ? 'opacity-100 scale-105 transform' : 
                  isPast ? 'opacity-40' : 'opacity-20 translate-y-4 transform'
                }`}
              >
                <div className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-colors ${
                  isActive ? 'border-orange-500 text-orange-500 bg-orange-500/10' : 
                  isPast ? 'border-green-500 text-green-500' : 'border-[#57534E] text-[#57534E]'
                }`}>
                  {isActive ? <Loader2 size={18} className="animate-spin" /> : <step.icon size={18} />}
                </div>
                <span className={`font-medium ${isActive ? 'text-white' : 'text-[#78716C]'}`}>
                  {step.text}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
