import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Loader2 } from 'lucide-react';

import AuthLayout from '../components/AuthLayout';
import FormInput from '../components/FormInput';
import PasswordInput from '../components/PasswordInput';
import { authService } from '../services/authService';

export default function Login() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.email || !formData.password) {
      toast.error('Please fill in all fields.');
      return;
    }

    if (formData.email === 'serendibadmin@gmail.com' && formData.password === 'Serendib@1234') {
      toast.success('✓ Welcome to Admin Dashboard!');
      localStorage.setItem('user', JSON.stringify({
        name: 'Admin User',
        email: 'serendibadmin@gmail.com',
        role: 'Admin',
        country: 'Sri Lanka'
      }));
      navigate('/admin/dashboard');
      return;
    }

    setIsLoading(true);
    try {
      await authService.login(formData.email, formData.password);
      toast.success('✓ Welcome back to Serendib AI!');
      // Navigate to dashboard after successful login
      navigate('/dashboard');
    } catch (err) {
      toast.error(`✕ ${err.message || 'Invalid email or password.'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthLayout 
      title="Welcome Back" 
      subtitle="Continue your journey with Serendib AI."
    >
      <form onSubmit={handleSubmit} className="flex flex-col w-full">
        <FormInput 
          id="email"
          label="Email Address"
          type="email"
          placeholder="you@example.com"
          value={formData.email}
          onChange={handleChange}
          disabled={isLoading}
        />
        
        <PasswordInput 
          id="password"
          label="Password"
          placeholder="••••••••"
          value={formData.password}
          onChange={handleChange}
          disabled={isLoading}
        />

        <div className="flex items-center justify-between mb-8 mt-2">
          <label className="flex items-center gap-2 cursor-pointer group">
            <div className="relative flex items-center justify-center w-4 h-4 rounded border border-[#EAE2D6] bg-[#FBF3EA]/50 group-hover:border-orange-400 transition-colors">
              <input type="checkbox" className="opacity-0 absolute inset-0 cursor-pointer" />
            </div>
            <span className="text-xs text-[#78716C] group-hover:text-[#1C1917] transition-colors">Remember me</span>
          </label>
          <button type="button" className="text-xs text-orange-600 hover:text-orange-500 font-medium transition-colors">
            Forgot Password?
          </button>
        </div>

        <button 
          type="submit" 
          disabled={isLoading}
          className="w-full rounded-full bg-orange-500 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-orange-500/25 hover:bg-orange-600 hover:scale-[1.02] transition-all disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center gap-2"
        >
          {isLoading && <Loader2 size={16} className="animate-spin" />}
          {isLoading ? 'Signing In...' : 'Sign In'}
        </button>

        <div className="mt-8 text-center text-sm text-[#78716C]">
          Don't have an account?{' '}
          <Link 
            to="/register" 
            className="text-orange-600 hover:text-orange-500 font-medium transition-colors"
          >
            Create Account
          </Link>
        </div>
      </form>
    </AuthLayout>
  );
}
