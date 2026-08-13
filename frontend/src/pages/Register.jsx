import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Loader2, CheckCircle2, Circle } from 'lucide-react';

import AuthLayout from '../components/AuthLayout';
import FormInput from '../components/FormInput';
import PasswordInput from '../components/PasswordInput';
import SearchableDropdown from '../components/SearchableDropdown';
import { authService } from '../services/authService';
import { getCountries, getCurrencies } from '../data/countries';

export default function Register() {
  const navigate = useNavigate();

  const [countriesList, setCountriesList] = useState([]);
  const [currenciesList, setCurrenciesList] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [agreed, setAgreed] = useState(false);

  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    country_code: '',
    preferred_currency: '',
    password: '',
    confirm_password: ''
  });

  useEffect(() => {
    setCountriesList(getCountries());
    setCurrenciesList(getCurrencies());
  }, []);

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));
    // Clear error for field
    if (errors[id]) {
      setErrors(prev => ({ ...prev, [id]: null }));
    }
  };

  const handleCountryChange = (code) => {
    setFormData(prev => ({ ...prev, country_code: code }));
    if (errors.country_code) {
      setErrors(prev => ({ ...prev, country_code: null }));
    }

    // Auto suggest currency
    const selectedCountry = countriesList.find(c => c.code === code);
    if (selectedCountry && selectedCountry.currency) {
      setFormData(prev => ({ ...prev, preferred_currency: selectedCountry.currency }));
      if (errors.preferred_currency) {
        setErrors(prev => ({ ...prev, preferred_currency: null }));
      }
    }
  };

  const handleCurrencyChange = (code) => {
    setFormData(prev => ({ ...prev, preferred_currency: code }));
    if (errors.preferred_currency) {
      setErrors(prev => ({ ...prev, preferred_currency: null }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.full_name) newErrors.full_name = 'Full name is required';
    if (!formData.email) newErrors.email = 'Email is required';
    else if (!/^\S+@\S+\.\S+$/.test(formData.email)) newErrors.email = 'Invalid email address';

    if (!formData.country_code) newErrors.country_code = 'Please select a country';
    if (!formData.preferred_currency) newErrors.preferred_currency = 'Please select a currency';

    if (!formData.password) newErrors.password = 'Password is required';
    else {
      if (formData.password.length < 8) newErrors.password = 'Minimum 8 characters';
      else if (!/[A-Z]/.test(formData.password)) newErrors.password = 'Needs uppercase letter';
      else if (!/[a-z]/.test(formData.password)) newErrors.password = 'Needs lowercase letter';
      else if (!/\d/.test(formData.password)) newErrors.password = 'Needs number';
      else if (!/[!@#$%^&*(),.?":{}|<>]/.test(formData.password)) newErrors.password = 'Needs special character';
    }

    if (!formData.confirm_password) newErrors.confirm_password = 'Confirm your password';
    else if (formData.password !== formData.confirm_password) newErrors.confirm_password = 'Passwords do not match';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validate()) return;

    if (!agreed) {
      toast.error('You must agree to the Terms & Privacy Policy.');
      return;
    }

    setIsLoading(true);
    try {
      await authService.register(formData);
      toast.success('✓ Account created successfully!');
      navigate('/login');
    } catch (err) {
      // Show duplicate email error nicely
      if (err.message && err.message.toLowerCase().includes('email')) {
        toast.error('✕ An account with this email already exists.');
        setErrors(prev => ({ ...prev, email: 'Email already exists' }));
      } else {
        toast.error(`✕ ${err.message || 'Unable to connect to the server.'}`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Password requirements checklist
  const pwd = formData.password;
  const reqs = [
    { label: '8+ characters', met: pwd.length >= 8 },
    { label: 'Uppercase', met: /[A-Z]/.test(pwd) },
    { label: 'Lowercase', met: /[a-z]/.test(pwd) },
    { label: 'Number', met: /\d/.test(pwd) },
    { label: 'Special char', met: /[!@#$%^&*(),.?":{}|<>]/.test(pwd) },
  ];

  return (
    <AuthLayout
      title="Create Your Account"
      subtitle="Start planning smarter journeys across Sri Lanka."
    >
      <form onSubmit={handleSubmit} className="flex flex-col w-full">

        <FormInput
          id="full_name"
          label="Full Name"
          type="text"
          placeholder="Enter your name"
          value={formData.full_name}
          onChange={handleChange}
          error={errors.full_name}
          disabled={isLoading}
        />

        <FormInput
          id="email"
          label="Email Address"
          type="email"
          placeholder="you@example.com"
          value={formData.email}
          onChange={handleChange}
          error={errors.email}
          disabled={isLoading}
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <SearchableDropdown
            id="country_code"
            label="Country"
            options={countriesList}
            value={formData.country_code}
            onChange={handleCountryChange}
            placeholder="Select Country"
            error={errors.country_code}
          />
          <SearchableDropdown
            id="preferred_currency"
            label="Preferred Currency"
            options={currenciesList}
            value={formData.preferred_currency}
            onChange={handleCurrencyChange}
            placeholder="Select Currency"
            error={errors.preferred_currency}
          />
        </div>

        <PasswordInput
          id="password"
          label="Password"
          placeholder="••••••••"
          value={formData.password}
          onChange={handleChange}
          error={errors.password}
          disabled={isLoading}
        />

        {formData.password && (
          <div className="flex flex-wrap gap-x-4 gap-y-2 mb-4 -mt-2">
            {reqs.map((r, i) => (
              <div key={i} className={`flex items-center gap-1 text-[10px] ${r.met ? 'text-orange-500' : 'text-[#A8A29E]'}`}>
                {r.met ? <CheckCircle2 size={12} /> : <Circle size={12} />}
                {r.label}
              </div>
            ))}
          </div>
        )}

        <PasswordInput
          id="confirm_password"
          label="Confirm Password"
          placeholder="••••••••"
          value={formData.confirm_password}
          onChange={handleChange}
          error={errors.confirm_password}
          disabled={isLoading}
        />

        <div className="mb-8 mt-2">
          <label className="flex items-start gap-3 cursor-pointer group">
            <div className={`mt-0.5 relative flex items-center justify-center w-5 h-5 rounded border ${agreed ? 'bg-orange-500 border-orange-500' : 'bg-[#FBF3EA]/50 border-[#EAE2D6] group-hover:border-orange-400'} transition-colors`}>
              <input
                type="checkbox"
                className="opacity-0 absolute inset-0 cursor-pointer"
                checked={agreed}
                onChange={(e) => setAgreed(e.target.checked)}
              />
              {agreed && <CheckCircle2 size={14} className="text-white" />}
            </div>
            <span className="text-xs text-[#78716C] leading-relaxed group-hover:text-[#1C1917] transition-colors">
              I agree to the Terms & Privacy Policy
            </span>
          </label>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full rounded-full bg-orange-500 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-orange-500/25 hover:bg-orange-600 hover:scale-[1.02] transition-all disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center gap-2"
        >
          {isLoading && <Loader2 size={16} className="animate-spin" />}
          {isLoading ? 'Creating Account...' : 'Create Account'}
        </button>

        <div className="mt-8 text-center text-sm text-[#78716C]">
          Already have an account?{' '}
          <Link
            to="/login"
            className="text-orange-600 hover:text-orange-500 font-medium transition-colors"
          >
            Sign In
          </Link>
        </div>
      </form>
    </AuthLayout>
  );
}
