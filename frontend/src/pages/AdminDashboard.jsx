import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, Users, Map, Bot, Activity, Settings, 
  LogOut, Bell, Menu, X, Search, MoreVertical 
} from 'lucide-react';
import { authService } from '../services/authService';

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('Overview');
  const [adminUser, setAdminUser] = useState(null);

  useEffect(() => {
    const user = authService.getCurrentUser();
    if (!user || user.role !== 'Admin') {
      navigate('/login');
    } else {
      setAdminUser(user);
    }
  }, [navigate]);

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  const navItems = [
    { name: 'Overview', icon: LayoutDashboard },
    { name: 'Users', icon: Users },
    { name: 'Trips', icon: Map },
    { name: 'AI Agents', icon: Bot },
    { name: 'System Activity', icon: Activity },
    { name: 'Settings', icon: Settings },
  ];

  const adminName = adminUser?.name || 'Admin';

  return (
    <div className="min-h-screen bg-[#FBF3EA] text-[#1C1917] font-sans flex overflow-hidden">
      
      {/* Mobile Sidebar Overlay */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-[#1C1917]/20 backdrop-blur-sm z-40 lg:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed lg:static inset-y-0 left-0 z-50
        w-64 bg-[#FFFCF8] border-r border-[#EAE2D6] flex flex-col
        transition-transform duration-300 ease-in-out
        ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div className="h-20 flex items-center justify-between px-6 border-b border-[#EAE2D6]">
          <Link to="/admin/dashboard" className="text-xl font-bold text-orange-600 tracking-tight flex items-center gap-2">
            <div className="w-7 h-7 bg-orange-500 rounded flex items-center justify-center">
              <span className="text-white font-bold text-sm">S</span>
            </div>
            Admin
          </Link>
          <button className="lg:hidden text-[#78716C]" onClick={() => setIsSidebarOpen(false)}>
            <X size={20} />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto py-6 px-4 space-y-1">
          {navItems.map((item) => (
            <button
              key={item.name}
              onClick={() => {
                setActiveTab(item.name);
                setIsSidebarOpen(false);
              }}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors ${
                activeTab === item.name 
                ? 'bg-orange-50 text-orange-600' 
                : 'text-[#57534E] hover:bg-[#FBF3EA] hover:text-[#1C1917]'
              }`}
            >
              <item.icon size={18} className={activeTab === item.name ? 'text-orange-500' : 'text-[#78716C]'} />
              {item.name}
            </button>
          ))}
        </div>

        <div className="p-4 border-t border-[#EAE2D6]">
          <div className="flex items-center gap-3 px-4 py-3 mb-2">
            <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center text-white text-xs font-bold shadow-[0_0_10px_rgba(249,115,22,0.3)]">
              {adminName.charAt(0)}
            </div>
            <div className="flex-1 overflow-hidden">
              <p className="text-sm font-semibold truncate text-[#1C1917]">{adminName}</p>
              <p className="text-[10px] text-[#78716C]">Administrator</p>
            </div>
          </div>
          <button 
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium text-red-600 hover:bg-red-50 transition-colors"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Top Header */}
        <header className="h-20 bg-[#FFFCF8] border-b border-[#EAE2D6] px-6 flex items-center justify-between sticky top-0 z-30">
          <div className="flex items-center gap-4">
            <button 
              className="lg:hidden p-2 -ml-2 text-[#57534E] hover:bg-[#FBF3EA] rounded-lg"
              onClick={() => setIsSidebarOpen(true)}
            >
              <Menu size={24} />
            </button>
            <div>
              <h1 className="text-lg md:text-xl font-bold text-[#1C1917]">Admin Dashboard</h1>
              <p className="hidden md:block text-xs text-[#78716C]">Monitor users, trips and system activity.</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center relative">
              <Search size={16} className="absolute left-3 text-[#78716C]" />
              <input 
                type="text" 
                placeholder="Search..." 
                className="pl-9 pr-4 py-2 bg-[#FBF3EA] border border-[#EAE2D6] rounded-full text-sm focus:outline-none focus:border-orange-300 focus:ring-1 focus:ring-orange-300 w-48 lg:w-64"
              />
            </div>
            <button className="p-2 text-[#78716C] hover:text-orange-500 hover:bg-orange-50 rounded-full transition-all relative">
              <Bell size={20} />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border border-white"></span>
            </button>
            <div className="w-9 h-9 bg-orange-100 border border-orange-200 rounded-full flex items-center justify-center text-orange-600 font-bold">
              {adminName.charAt(0)}
            </div>
          </div>
        </header>

        {/* Scrollable Dashboard Content */}
        <div className="flex-1 overflow-auto p-6 space-y-8">
          
          {/* Overview Cards */}
          <section className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6">
            <div className="bg-white border border-[#EAE2D6] p-6 rounded-2xl shadow-sm">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <p className="text-sm font-medium text-[#78716C]">Total Users</p>
                  <p className="text-3xl font-bold text-[#1C1917] mt-1">1,248</p>
                </div>
                <div className="p-2 bg-blue-50 text-blue-600 rounded-lg"><Users size={20} /></div>
              </div>
              <p className="text-xs text-green-600 font-medium">+12% from last month</p>
            </div>
            
            <div className="bg-white border border-[#EAE2D6] p-6 rounded-2xl shadow-sm">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <p className="text-sm font-medium text-[#78716C]">Active Users</p>
                  <p className="text-3xl font-bold text-[#1C1917] mt-1">824</p>
                </div>
                <div className="p-2 bg-green-50 text-green-600 rounded-lg"><Activity size={20} /></div>
              </div>
              <p className="text-xs text-[#78716C]">Current active sessions</p>
            </div>

            <div className="bg-white border border-[#EAE2D6] p-6 rounded-2xl shadow-sm">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <p className="text-sm font-medium text-[#78716C]">Trips Generated</p>
                  <p className="text-3xl font-bold text-[#1C1917] mt-1">3,540</p>
                </div>
                <div className="p-2 bg-orange-50 text-orange-600 rounded-lg"><Map size={20} /></div>
              </div>
              <p className="text-xs text-green-600 font-medium">+24 this week</p>
            </div>

            <div className="bg-white border border-[#EAE2D6] p-6 rounded-2xl shadow-sm">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <p className="text-sm font-medium text-[#78716C]">AI Requests</p>
                  <p className="text-3xl font-bold text-[#1C1917] mt-1">12,480</p>
                </div>
                <div className="p-2 bg-purple-50 text-purple-600 rounded-lg"><Bot size={20} /></div>
              </div>
              <p className="text-xs text-[#78716C]">Across all agents</p>
            </div>
          </section>

          <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
            
            {/* Left Column (Wider) */}
            <div className="xl:col-span-2 space-y-8">
              
              {/* User Management Preview */}
              <section className="bg-white border border-[#EAE2D6] rounded-2xl shadow-sm overflow-hidden">
                <div className="p-6 border-b border-[#EAE2D6] flex justify-between items-center">
                  <h2 className="text-lg font-bold text-[#1C1917]">Recent Users</h2>
                  <button className="text-sm font-medium text-orange-600 hover:text-orange-700">View All</button>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm whitespace-nowrap">
                    <thead className="bg-[#FBF3EA] text-[#78716C]">
                      <tr>
                        <th className="px-6 py-3 font-medium">Name</th>
                        <th className="px-6 py-3 font-medium">Email</th>
                        <th className="px-6 py-3 font-medium">Country</th>
                        <th className="px-6 py-3 font-medium">Role</th>
                        <th className="px-6 py-3 font-medium">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#EAE2D6]">
                      <tr className="hover:bg-[#FBF3EA]/50 transition-colors">
                        <td className="px-6 py-4 font-medium text-[#1C1917]">John Smith</td>
                        <td className="px-6 py-4 text-[#57534E]">john@example.com</td>
                        <td className="px-6 py-4 text-[#57534E]">Sri Lanka</td>
                        <td className="px-6 py-4 text-[#57534E]">Traveler</td>
                        <td className="px-6 py-4">
                          <span className="px-2.5 py-1 text-xs font-medium bg-green-100 text-green-700 rounded-full border border-green-200">Active</span>
                        </td>
                      </tr>
                      <tr className="hover:bg-[#FBF3EA]/50 transition-colors">
                        <td className="px-6 py-4 font-medium text-[#1C1917]">Sarah Johnson</td>
                        <td className="px-6 py-4 text-[#57534E]">sarah.j@example.com</td>
                        <td className="px-6 py-4 text-[#57534E]">UK</td>
                        <td className="px-6 py-4 text-[#57534E]">Traveler</td>
                        <td className="px-6 py-4">
                          <span className="px-2.5 py-1 text-xs font-medium bg-green-100 text-green-700 rounded-full border border-green-200">Active</span>
                        </td>
                      </tr>
                      <tr className="hover:bg-[#FBF3EA]/50 transition-colors">
                        <td className="px-6 py-4 font-medium text-[#1C1917]">Michael Doe</td>
                        <td className="px-6 py-4 text-[#57534E]">michael@example.com</td>
                        <td className="px-6 py-4 text-[#57534E]">USA</td>
                        <td className="px-6 py-4 text-[#57534E]">Traveler</td>
                        <td className="px-6 py-4">
                          <span className="px-2.5 py-1 text-xs font-medium bg-gray-100 text-[#57534E] rounded-full border border-gray-200">Inactive</span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </section>

              {/* Trip Overview */}
              <section className="bg-white border border-[#EAE2D6] rounded-2xl shadow-sm overflow-hidden">
                <div className="p-6 border-b border-[#EAE2D6] flex justify-between items-center">
                  <h2 className="text-lg font-bold text-[#1C1917]">Recent Trips</h2>
                  <button className="text-sm font-medium text-orange-600 hover:text-orange-700">View All</button>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm whitespace-nowrap">
                    <thead className="bg-[#FBF3EA] text-[#78716C]">
                      <tr>
                        <th className="px-6 py-3 font-medium">Trip Name</th>
                        <th className="px-6 py-3 font-medium">User</th>
                        <th className="px-6 py-3 font-medium">Days</th>
                        <th className="px-6 py-3 font-medium">Budget</th>
                        <th className="px-6 py-3 font-medium">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#EAE2D6]">
                      <tr className="hover:bg-[#FBF3EA]/50 transition-colors">
                        <td className="px-6 py-4 font-medium text-[#1C1917]">Cultural Triangle Tour</td>
                        <td className="px-6 py-4 text-[#57534E]">John Smith</td>
                        <td className="px-6 py-4 text-[#57534E]">7 Days</td>
                        <td className="px-6 py-4 text-[#57534E]">LKR 150,000</td>
                        <td className="px-6 py-4 text-[#57534E]">Planned</td>
                      </tr>
                      <tr className="hover:bg-[#FBF3EA]/50 transition-colors">
                        <td className="px-6 py-4 font-medium text-[#1C1917]">South Coast Beach Escape</td>
                        <td className="px-6 py-4 text-[#57534E]">Sarah Johnson</td>
                        <td className="px-6 py-4 text-[#57534E]">4 Days</td>
                        <td className="px-6 py-4 text-[#57534E]">LKR 80,000</td>
                        <td className="px-6 py-4 text-[#57534E]">Saved</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </section>

            </div>

            {/* Right Column */}
            <div className="space-y-8">
              
              {/* AI Agent Status */}
              <section className="bg-white border border-[#EAE2D6] rounded-2xl p-6 shadow-sm">
                <h2 className="text-lg font-bold text-[#1C1917] mb-6">AI Agent Status</h2>
                <div className="space-y-4">
                  {[
                    { name: 'User Profile Agent', status: 'Online' },
                    { name: 'Destination Agent', status: 'Online' },
                    { name: 'Food Agent', status: 'Online' },
                    { name: 'Smart Trip Planner', status: 'Online' },
                    { name: 'Weather Integration', status: 'Connected' },
                    { name: 'Route Service', status: 'Connected' },
                  ].map((agent, i) => (
                    <div key={i} className="flex justify-between items-center pb-3 border-b border-[#EAE2D6] last:border-0 last:pb-0">
                      <div className="flex items-center gap-3">
                        <Bot size={16} className="text-[#78716C]" />
                        <span className="text-sm font-medium text-[#1C1917]">{agent.name}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_5px_rgba(34,197,94,0.5)]"></div>
                        <span className="text-xs text-[#57534E]">{agent.status}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              {/* System Activity */}
              <section className="bg-white border border-[#EAE2D6] rounded-2xl p-6 shadow-sm">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-lg font-bold text-[#1C1917]">System Activity</h2>
                  <button className="text-[#78716C] hover:text-[#1C1917]"><MoreVertical size={16} /></button>
                </div>
                <div className="space-y-5">
                  {[
                    { title: 'User registered', time: '10 mins ago', type: 'user' },
                    { title: 'Trip generated', time: '24 mins ago', type: 'trip' },
                    { title: 'User logged in', time: '1 hour ago', type: 'user' },
                    { title: 'Trip re-planned', time: '2 hours ago', type: 'trip' },
                  ].map((activity, i) => (
                    <div key={i} className="flex gap-4">
                      <div className="relative mt-1">
                        <div className="w-2.5 h-2.5 rounded-full bg-orange-400"></div>
                        {i !== 3 && <div className="absolute top-3 left-1/2 -ml-[1px] w-[2px] h-10 bg-[#EAE2D6]"></div>}
                      </div>
                      <div>
                        <p className="text-sm font-medium text-[#1C1917]">{activity.title}</p>
                        <p className="text-xs text-[#78716C] mt-0.5">{activity.time}</p>
                      </div>
                    </div>
                  ))}
                </div>
                <button className="w-full mt-6 py-2 text-sm font-medium text-[#57534E] bg-[#FBF3EA] rounded-xl hover:bg-[#EAE2D6] transition-colors">
                  View Full Log
                </button>
              </section>

            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
