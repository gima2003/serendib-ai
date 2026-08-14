import React from 'react';

export default function FormInput({ label, id, error, ...props }) {
  return (
    <div className="flex flex-col gap-1.5 mb-4 w-full">
      <label htmlFor={id} className="text-xs font-semibold text-[#78716C] uppercase tracking-wide">
        {label}
      </label>
      <input
        id={id}
        className={`w-full bg-[#FBF3EA]/50 border ${
          error ? 'border-red-500/50 focus:border-red-500' : 'border-[#EAE2D6] focus:border-orange-400 focus:shadow-[0_0_0_2px_rgba(249,115,22,0.1)]'
        } rounded-xl px-4 py-3 text-sm text-[#1C1917] placeholder-[#A8A29E] focus:outline-none transition-all duration-300`}
        {...props}
      />
      {error && <span className="text-xs text-red-500 mt-1 font-medium">{error}</span>}
    </div>
  );
}
