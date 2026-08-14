import React, { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';

export default function PasswordInput({ label, id, error, ...props }) {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="flex flex-col gap-1.5 mb-4 w-full">
      <label htmlFor={id} className="text-xs font-semibold text-[#78716C] uppercase tracking-wide">
        {label}
      </label>
      <div className="relative w-full">
        <input
          id={id}
          type={showPassword ? 'text' : 'password'}
          className={`w-full bg-[#FBF3EA]/50 border ${
            error ? 'border-red-500/50 focus:border-red-500' : 'border-[#EAE2D6] focus:border-orange-400 focus:shadow-[0_0_0_2px_rgba(249,115,22,0.1)]'
          } rounded-xl pl-4 pr-12 py-3 text-sm text-[#1C1917] placeholder-[#A8A29E] focus:outline-none transition-all duration-300`}
          {...props}
        />
        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-[#A8A29E] hover:text-[#57534E] transition-colors focus:outline-none"
          aria-label={showPassword ? "Hide password" : "Show password"}
        >
          {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
        </button>
      </div>
      {error && <span className="text-xs text-red-500 mt-1 font-medium">{error}</span>}
    </div>
  );
}
