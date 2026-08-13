import { countries } from 'countries-list';

// Transform the countries-list object into an array suitable for our dropdowns
export const getCountries = () => {
  return Object.keys(countries).map((code) => {
    const country = countries[code];
    let primaryCurrency = '';
    if (country.currency) {
      primaryCurrency = Array.isArray(country.currency) 
        ? country.currency[0] 
        : (typeof country.currency === 'string' ? country.currency.split(',')[0] : '');
    }
    
    return {
      code, // e.g., 'LK'
      name: country.name, // e.g., 'Sri Lanka'
      flagUrl: `https://flagcdn.com/w40/${code.toLowerCase()}.png`, // reliable cross-platform SVG/PNG flags
      currency: primaryCurrency,
      label: country.name // SearchableDropdown will render flagUrl + label
    };
  }).sort((a, b) => a.name.localeCompare(b.name));
};

export const getCurrencies = () => {
  const currenciesSet = new Set();
  const currencyList = [];

  Object.values(countries).forEach((country) => {
    if (country.currency) {
      const codes = Array.isArray(country.currency) 
        ? country.currency 
        : (typeof country.currency === 'string' ? country.currency.split(',') : []);
        
      codes.forEach(code => {
        const trimmedCode = code.trim();
        if (trimmedCode && !currenciesSet.has(trimmedCode)) {
          currenciesSet.add(trimmedCode);
          currencyList.push({
            code: trimmedCode,
            label: `${trimmedCode}`
          });
        }
      });
    }
  });

  return currencyList.sort((a, b) => a.code.localeCompare(b.code));
};
