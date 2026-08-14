import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Search } from 'lucide-react';

export default function SearchableDropdown({ label, id, options, value, onChange, placeholder, error }) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const dropdownRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const filteredOptions = options.filter(opt =>
    opt.label.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const selectedOption = options.find(opt => opt.code === value);

  return (
    <div className="flex flex-col gap-1.5 mb-4 w-full relative" ref={dropdownRef}>
      <label htmlFor={id} className="text-xs font-semibold text-[#78716C] uppercase tracking-wide">
        {label}
      </label>
      
      <div 
        className={`w-full bg-[#FBF3EA]/50 border ${
          error ? 'border-red-500/50' : 'border-[#EAE2D6] hover:border-orange-300'
        } rounded-xl px-4 py-3 text-sm text-[#1C1917] cursor-pointer flex justify-between items-center transition-all duration-300 ${isOpen ? 'border-orange-400 shadow-[0_0_0_2px_rgba(249,115,22,0.1)]' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        id={id}
      >
        <span className={`flex items-center gap-2 ${selectedOption ? 'text-[#1C1917]' : 'text-[#A8A29E]'}`}>
          {selectedOption ? (
            <>
              {selectedOption.flagUrl && <img src={selectedOption.flagUrl} alt={selectedOption.code} className="w-5 h-auto object-cover rounded-sm shadow-sm" />}
              <span>{selectedOption.label}</span>
            </>
          ) : (
            placeholder
          )}
        </span>
        <ChevronDown size={16} className={`text-[#A8A29E] transition-transform duration-300 ${isOpen ? 'rotate-180 text-[#57534E]' : ''}`} />
      </div>

      {error && <span className="text-xs text-red-500 mt-1 font-medium">{error}</span>}

      {isOpen && (
        <div className="absolute top-[72px] left-0 w-full bg-white border border-[#EAE2D6] rounded-xl shadow-[0_8px_30px_rgb(0,0,0,0.08)] z-50 overflow-hidden flex flex-col max-h-60 animate-in fade-in slide-in-from-top-2 duration-200">
          <div className="p-2 border-b border-[#EAE2D6] flex items-center gap-2 text-[#78716C] px-3 bg-[#FBF3EA]/50">
            <Search size={14} />
            <input 
              type="text" 
              className="bg-transparent border-none text-sm text-[#1C1917] placeholder-[#A8A29E] w-full focus:outline-none"
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onClick={(e) => e.stopPropagation()}
              autoFocus
            />
          </div>
          <div className="overflow-y-auto">
            {filteredOptions.length > 0 ? (
              filteredOptions.map((opt) => (
                <div 
                  key={opt.code}
                  className={`px-4 py-2.5 text-sm cursor-pointer transition-colors flex items-center gap-2 ${
                    value === opt.code ? 'bg-orange-50 text-orange-600 font-medium' : 'text-[#57534E] hover:bg-[#FBF3EA]/50'
                  }`}
                  onClick={() => {
                    onChange(opt.code);
                    setIsOpen(false);
                    setSearchTerm('');
                  }}
                >
                  {opt.flagUrl && <img src={opt.flagUrl} alt={opt.code} className="w-5 h-auto object-cover rounded-sm shadow-sm" />}
                  <span>{opt.label}</span>
                </div>
              ))
            ) : (
              <div className="px-4 py-3 text-sm text-[#A8A29E] text-center">No results found</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
