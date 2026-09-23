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
  const [currentIdx, setCurrentIdx] = useState(0);
  const [prevIdx, setPrevIdx] = useState(null);

  useEffect(() => {
    let active = true;

    const loadNext = (idx) => {
      const img = new Image();
      img.src = heroSlides[idx].img;
      img.onload = () => {
        if (active) {
          setPrevIdx(currentIdx);
          setCurrentIdx(idx);
        }
      };
      img.onerror = () => {
        if (active) {
          // If image fails to load, skip to the next valid one immediately
          loadNext((idx + 1) % heroSlides.length);
        }
      };
    };

    const timer = setTimeout(() => {
      loadNext((currentIdx + 1) % heroSlides.length);
    }, 5000);

    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, [currentIdx]);

  return {
    current: heroSlides[currentIdx],
    previous: prevIdx !== null ? heroSlides[prevIdx] : null,
    slides: heroSlides,
  };
}
