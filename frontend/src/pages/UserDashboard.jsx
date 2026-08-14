import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Bell, User, Map, Compass, Calendar, Wallet, ChevronRight, X, LogOut, Sun, CheckCircle } from 'lucide-react';
import { authService } from '../services/authService';
import toast from 'react-hot-toast';

export default function UserDashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const profileRef = useRef(null);

  useEffect(() => {
    const currentUser = authService.getCurrentUser();
    if (!currentUser) {
      navigate('/login');
    } else {
      setUser(currentUser);
    }
  }, [navigate]);

  useEffect(() => {
    function handleClickOutside(event) {
      if (profileRef.current && !profileRef.current.contains(event.target)) {
        setIsProfileOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  const userName = user?.full_name || user?.name || 'Traveler';
  const userEmail = user?.email || 'user@example.com';
  
  const lastLoginDate = user?.last_login || user?.updated_at || user?.created_at;
  const formattedLastLogin = lastLoginDate 
    ? new Date(lastLoginDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
    : 'Recently';

  return (
    <div className="min-h-screen bg-[#FFFCF8] text-[#1C1917] font-sans overflow-x-hidden">
      {/* Top Navigation */}
      <header className="sticky top-0 z-40 bg-[#FFFCF8]/90 backdrop-blur-md border-b border-[#EAE2D6] px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <Link to="/" className="text-2xl font-bold text-orange-600 tracking-tight flex items-center gap-2">
            <div className="w-8 h-8 bg-orange-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">S</span>
            </div>
            Serendib AI
          </Link>
          <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-[#57534E]">
            <Link to="/dashboard" className="text-orange-600">Dashboard</Link>
            <Link to="#" className="hover:text-orange-500 transition-colors">Plan My Trip</Link>
            <Link to="#" className="hover:text-orange-500 transition-colors">My Trips</Link>
            <Link to="#" className="hover:text-orange-500 transition-colors">Explore</Link>
          </nav>
        </div>
        <div className="flex items-center gap-4 relative">
          <button className="p-2 text-[#78716C] hover:text-orange-500 hover:bg-orange-50 rounded-full transition-all">
            <Bell size={20} />
          </button>
          
          <button 
            onClick={() => setIsProfileOpen(!isProfileOpen)}
            className="w-10 h-10 rounded-full bg-orange-100 border border-orange-200 flex items-center justify-center text-orange-600 hover:shadow-[0_0_15px_rgba(249,115,22,0.3)] transition-all overflow-hidden"
          >
            <User size={20} />
          </button>

          {/* Profile Popup */}
          {isProfileOpen && (
            <div 
              ref={profileRef}
              className="absolute top-14 right-0 w-80 bg-white rounded-2xl shadow-[0_10px_40px_rgba(28,25,23,0.1)] border border-[#EAE2D6] p-5 z-50 transform origin-top-right transition-all duration-200 scale-100 opacity-100"
            >
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-lg font-semibold text-[#1C1917]">Profile</h3>
                <button onClick={() => setIsProfileOpen(false)} className="text-[#78716C] hover:text-[#1C1917]">
                  <X size={20} />
                </button>
              </div>
              
              <div className="flex items-center gap-3 mb-6 p-3 bg-[#FBF3EA] rounded-xl border border-[#EAE2D6]">
                <div className="w-12 h-12 bg-orange-500 rounded-full flex items-center justify-center text-white text-xl font-bold shadow-[0_0_15px_rgba(249,115,22,0.3)]">
                  {userName.charAt(0)}
                </div>
                <div>
                  <p className="font-semibold text-[#1C1917]">{userName}</p>
                  <p className="text-xs text-[#78716C]">Last Login: {formattedLastLogin}</p>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-medium text-[#78716C] mb-1">Email Address</label>
                  <input 
                    type="email" 
                    value={userEmail}
                    disabled
                    className="w-full px-3 py-2 text-sm bg-[#FBF3EA] border border-[#EAE2D6] rounded-lg text-[#57534E] cursor-not-allowed"
                  />
                  <p className="text-[10px] text-[#78716C] mt-1">This email cannot be changed.</p>
                </div>
                <div>
                  <label className="block text-xs font-medium text-[#78716C] mb-1">Full Name</label>
                  <input 
                    type="text" 
                    defaultValue={userName}
                    className="w-full px-3 py-2 text-sm bg-white border border-[#EAE2D6] rounded-lg focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-[#78716C] mb-1">Country</label>
                  <input 
                    type="text" 
                    defaultValue="Sri Lanka"
                    className="w-full px-3 py-2 text-sm bg-white border border-[#EAE2D6] rounded-lg focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-[#78716C] mb-1">Preferred Currency</label>
                  <select className="w-full px-3 py-2 text-sm bg-white border border-[#EAE2D6] rounded-lg focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500">
                    <option>LKR</option>
                    <option>USD</option>
                    <option>EUR</option>
                  </select>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-[#EAE2D6] flex flex-col gap-2">
                <button 
                  onClick={() => {
                    toast.success('Profile updated');
                    setIsProfileOpen(false);
                  }}
                  className="w-full bg-orange-500 text-white font-medium text-sm py-2.5 rounded-lg hover:bg-orange-600 transition-colors"
                >
                  Save Changes
                </button>
                <button 
                  onClick={handleLogout}
                  className="w-full flex items-center justify-center gap-2 text-red-600 font-medium text-sm py-2.5 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <LogOut size={16} /> Logout
                </button>
              </div>
            </div>
          )}
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-10 space-y-12">
        {/* Welcome Section */}
        <section className="relative overflow-hidden rounded-3xl bg-[#FBF3EA] border border-[#EAE2D6] p-10 flex flex-col items-start justify-center shadow-sm">
          <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-orange-500/10 rounded-full blur-3xl mix-blend-multiply"></div>
          
          <div className="relative z-10">
            <h1 className="text-3xl md:text-4xl font-bold text-[#1C1917] mb-2">
              Welcome back, {userName}
            </h1>
            <p className="text-lg text-[#57534E] mb-8">
              Ready to plan your next Sri Lankan journey?
            </p>
            
            <div className="flex flex-wrap items-center gap-4">
              <button className="bg-orange-500 text-white px-6 py-3 rounded-xl font-semibold shadow-[0_5px_15px_rgba(249,115,22,0.3)] hover:bg-orange-600 hover:-translate-y-0.5 transition-all">
                Plan My Trip
              </button>
              <button className="bg-white text-[#1C1917] border border-[#EAE2D6] px-6 py-3 rounded-xl font-semibold hover:border-orange-500 hover:text-orange-600 transition-all">
                Explore Destinations
              </button>
            </div>
          </div>
        </section>

        {/* Quick Stats */}
        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white border border-[#EAE2D6] rounded-2xl p-6 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-orange-50 text-orange-600 rounded-xl flex items-center justify-center">
              <Map size={24} />
            </div>
            <div>
              <p className="text-sm font-medium text-[#78716C]">Saved Trips</p>
              <p className="text-2xl font-bold text-[#1C1917]">3</p>
            </div>
          </div>
          <div className="bg-white border border-[#EAE2D6] rounded-2xl p-6 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-orange-50 text-orange-600 rounded-xl flex items-center justify-center">
              <Calendar size={24} />
            </div>
            <div>
              <p className="text-sm font-medium text-[#78716C]">Upcoming Trips</p>
              <p className="text-2xl font-bold text-[#1C1917]">1</p>
            </div>
          </div>
          <div className="bg-white border border-[#EAE2D6] rounded-2xl p-6 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-orange-50 text-orange-600 rounded-xl flex items-center justify-center">
              <Compass size={24} />
            </div>
            <div>
              <p className="text-sm font-medium text-[#78716C]">Places Explored</p>
              <p className="text-2xl font-bold text-[#1C1917]">12</p>
            </div>
          </div>
          <div className="bg-white border border-[#EAE2D6] rounded-2xl p-6 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-orange-50 text-orange-600 rounded-xl flex items-center justify-center">
              <Wallet size={24} />
            </div>
            <div>
              <p className="text-sm font-medium text-[#78716C]">Travel Budget</p>
              <p className="text-xl font-bold text-[#1C1917]">LKR 150,000</p>
            </div>
          </div>
        </section>

        {/* Dashboard Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Content Column */}
          <div className="lg:col-span-2 space-y-8">
            {/* Smart Planning Card */}
            <section className="bg-white border border-[#EAE2D6] rounded-2xl p-8 shadow-sm">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-[#1C1917]">Plan Your Next Journey</h2>
              </div>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
                <div className="bg-[#FBF3EA] p-4 rounded-xl border border-[#EAE2D6]">
                  <p className="text-xs text-[#78716C] mb-1">Destination Preferences</p>
                  <p className="font-medium text-[#1C1917]">Beach, Culture, Nature</p>
                </div>
                <div className="bg-[#FBF3EA] p-4 rounded-xl border border-[#EAE2D6]">
                  <p className="text-xs text-[#78716C] mb-1">Travel Style</p>
                  <p className="font-medium text-[#1C1917]">Relaxed Paced</p>
                </div>
              </div>
              
              <button className="w-full sm:w-auto bg-orange-500 text-white px-8 py-3 rounded-xl font-semibold shadow-md hover:bg-orange-600 transition-colors flex items-center justify-center gap-2">
                Start Planning <ChevronRight size={18} />
              </button>
            </section>

            {/* Recent Trips */}
            <section>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-[#1C1917]">My Recent Trips</h2>
                <button className="text-sm font-medium text-orange-600 hover:text-orange-700">View All Trips</button>
              </div>
              
              <div className="space-y-4">
                {/* Trip Card 1 */}
                <div className="bg-white border border-[#EAE2D6] p-5 rounded-2xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 hover:shadow-md transition-shadow group">
                  <div>
                    <h3 className="font-bold text-lg text-[#1C1917] group-hover:text-orange-600 transition-colors">Sri Lanka Adventure</h3>
                    <p className="text-sm text-[#57534E] mt-1">6 Days • Colombo → Kandy → Ella</p>
                    <p className="text-xs text-[#78716C] mt-2 bg-[#FBF3EA] inline-block px-2 py-1 rounded border border-[#EAE2D6]">Budget: LKR 120,000</p>
                  </div>
                  <button className="px-4 py-2 text-sm font-semibold border border-orange-200 text-orange-600 rounded-lg hover:bg-orange-50 transition-colors">
                    View Trip
                  </button>
                </div>
                
                {/* Trip Card 2 */}
                <div className="bg-white border border-[#EAE2D6] p-5 rounded-2xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 hover:shadow-md transition-shadow group">
                  <div>
                    <h3 className="font-bold text-lg text-[#1C1917] group-hover:text-orange-600 transition-colors">South Coast Escape</h3>
                    <p className="text-sm text-[#57534E] mt-1">4 Days • Galle → Mirissa</p>
                    <p className="text-xs text-[#78716C] mt-2 bg-[#FBF3EA] inline-block px-2 py-1 rounded border border-[#EAE2D6]">Budget: LKR 75,000</p>
                  </div>
                  <button className="px-4 py-2 text-sm font-semibold border border-orange-200 text-orange-600 rounded-lg hover:bg-orange-50 transition-colors">
                    View Trip
                  </button>
                </div>
              </div>
            </section>
          </div>

          {/* Sidebar Column */}
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-[#1C1917]">Travel Context</h2>
            
            <div className="bg-white border border-[#EAE2D6] rounded-2xl p-5 flex items-center gap-4 shadow-sm">
              <div className="w-12 h-12 bg-[#FFF7ED] text-orange-500 rounded-full flex items-center justify-center">
                <Sun size={24} />
              </div>
              <div>
                <p className="text-sm font-medium text-[#78716C]">Weather</p>
                <p className="font-bold text-[#1C1917]">24°C <span className="text-sm font-normal text-[#57534E]">Colombo</span></p>
              </div>
            </div>

            <div className="bg-white border border-[#EAE2D6] rounded-2xl p-5 flex items-center gap-4 shadow-sm">
              <div className="w-12 h-12 bg-green-50 text-green-600 rounded-full flex items-center justify-center">
                <CheckCircle size={24} />
              </div>
              <div>
                <p className="text-sm font-medium text-[#78716C]">Budget Status</p>
                <p className="font-bold text-[#1C1917]">Within Plan</p>
              </div>
            </div>

            <div className="bg-white border border-[#EAE2D6] rounded-2xl p-5 shadow-sm">
              <div className="flex justify-between items-center mb-3">
                <p className="font-bold text-[#1C1917]">AI Recommendations</p>
                <span className="bg-orange-100 text-orange-600 text-xs font-bold px-2 py-0.5 rounded-full">3 New</span>
              </div>
              <p className="text-sm text-[#57534E]">Your personal AI agent has found 3 new hidden gems based on your preferences.</p>
              <button className="text-sm text-orange-600 font-semibold mt-3 hover:text-orange-700">View Suggestions &rarr;</button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
