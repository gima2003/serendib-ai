import { useState, useEffect } from "react";
import { Sun, CloudSun, Cloud, CloudFog, CloudRain, CloudLightning } from "lucide-react";

const COORDS = {
  Colombo: { lat: 6.92, lon: 79.86 },
  Kandy: { lat: 7.29, lon: 80.63 },
  Galle: { lat: 6.03, lon: 80.21 },
  "Nuwara Eliya": { lat: 6.97, lon: 80.78 },
  Sigiriya: { lat: 7.95, lon: 80.75 },
  Ella: { lat: 6.87, lon: 81.05 }, // fixed: was 80.04 (Ella is ~81.05°E, not 80.04°E)
  Hatton: { lat: 6.89, lon: 80.59 },
  Mirissa: { lat: 5.94, lon: 80.45 },
  Yala: { lat: 6.37, lon: 81.52 },
  "Arugam Bay": { lat: 6.84, lon: 81.83 },
  "Horton Plains": { lat: 6.8, lon: 80.8 },
  Anuradhapura: { lat: 8.31, lon: 80.41 },
};

export function useSriLankaWeather(names = ["Colombo", "Kandy", "Galle", "Nuwara Eliya"]) {
  const [data, setData] = useState({});
  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const reqs = names.map((n) => {
          const c = COORDS[n] || COORDS.Colombo;
          return `latitude=${c.lat}&longitude=${c.lon}`;
        });
        const url = `https://api.open-meteo.com/v1/forecast?${reqs.join(
          "&"
        )}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&timezone=Asia%2FColombo`;
        const res = await fetch(url);
        if (!res.ok) throw new Error("weather unavailable");
        const json = await res.json();
        const list = Array.isArray(json) ? json : [json];
        const next = {};
        list.forEach((row, i) => {
          const c = row.current;
          if (c && names[i]) {
            next[names[i]] = {
              temp: c.temperature_2m,
              feels: c.apparent_temperature,
              humidity: c.relative_humidity_2m,
              wind: c.wind_speed_10m,
              code: c.weather_code,
            };
          }
        });
        if (!cancelled) setData(next);
      } catch {
        /* keep placeholders — the UI shows "--" until the next refresh */
      }
    };
    load();
    const id = setInterval(load, 15 * 60 * 1000);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [JSON.stringify(names)]);
  return data;
}

export function useColomboClock() {
  const [now, setNow] = useState(() => new Date());
  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 15000);
    return () => clearInterval(id);
  }, []);
  return now;
}

export const fmtTime = new Intl.DateTimeFormat("en-US", {
  hour: "numeric",
  minute: "2-digit",
  timeZone: "Asia/Colombo",
});

export const fmtDate = new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
  year: "numeric",
  timeZone: "Asia/Colombo",
});

/* WMO weather code → { label, icon }. Same mapping Home.jsx uses, so the  */
/* dashboard's weather widget matches the home page's hero weather card.  */
export function wmo(code) {
  if (code === 0) return { label: "Clear sky", icon: Sun };
  if (code === 1 || code === 2) return { label: "Partly cloudy", icon: CloudSun };
  if (code === 3) return { label: "Overcast", icon: Cloud };
  if (code === 45 || code === 48) return { label: "Foggy", icon: CloudFog };
  if (code >= 51 && code <= 67) return { label: "Rain", icon: CloudRain };
  if (code >= 80 && code <= 82) return { label: "Rain showers", icon: CloudRain };
  if (code >= 95) return { label: "Thunderstorm", icon: CloudLightning };
  return { label: "Cloudy", icon: Cloud };
}