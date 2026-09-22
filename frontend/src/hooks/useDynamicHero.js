import { useState, useEffect } from "react";
import { IMG, wiki } from "../components/common/Shared";

const heroSlides = [
  { img: wiki(IMG.sigiriya, 2000), align: "center", city: "Sigiriya", location: "Sigiriya Rock Fortress" },
  { img: wiki(IMG.ellaBridge, 2000), align: "bottom", city: "Ella", location: "Nine Arches Bridge" },
  { img: wiki(IMG.tea, 2000), align: "center", city: "Nuwara Eliya", location: "Nuwara Eliya" },
  { img: wiki(IMG.mirissa, 2000), align: "center", city: "Mirissa", location: "Mirissa Beach" },
  { img: wiki(IMG.elephants, 2000), align: "center", city: "Yala", location: "Yala National Park" },
  { img: wiki(IMG.galleDutch, 2000), align: "center", city: "Galle", location: "Galle Fort" },
  { img: wiki(IMG.tooth, 2000), align: "center", city: "Kandy", location: "Temple of the Tooth" },
];

export function useDynamicHero() {
  const [idx, setIdx] = useState(0);
  useEffect(() => {
    const timer = setInterval(() => setIdx((i) => (i + 1) % heroSlides.length), 7000);
    return () => clearInterval(timer);
  }, []);
  return heroSlides[idx];
}
