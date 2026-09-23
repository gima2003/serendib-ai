import { useEffect } from "react";
import { X } from "lucide-react";

/* ================================================================== */
/*  Overlay — a centered modal with a soft fade + scale-up entrance.    */
/*  Every popup in the app (profile, budget, weather, calendar, etc.)    */
/*  uses this, so they all open and close the same way.                 */
/*                                                                       */
/*  type="wide-modal"  → wider card, for content-heavy popups            */
/*                        (profile editor)                               */
/*  type="calendar"    → medium card sized for a festival/date list      */
/*  (default)          → compact card for short status popups            */
/* ================================================================== */

const WIDTH = {
  "wide-modal": "max-w-2xl",
  calendar: "max-w-lg",
};

export default function Overlay({ isOpen, onClose, title, type, children }) {
  useEffect(() => {
    if (!isOpen) return undefined;
    const onKey = (e) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", onKey);
      document.body.style.overflow = prevOverflow;
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;
  const maxW = WIDTH[type] || "max-w-md";

  return (
    <div className="fixed inset-0 z-[80] flex items-center justify-center p-4" role="dialog" aria-modal="true" aria-label={title}>
      <style>{`
        @keyframes overlayFade { from { opacity: 0; } to { opacity: 1; } }
        @keyframes overlayPop {
          from { opacity: 0; transform: translateY(18px) scale(.94); }
          to   { opacity: 1; transform: translateY(0) scale(1); }
        }
        .overlay-fade { animation: overlayFade .22s ease both; }
        .overlay-pop { animation: overlayPop .32s cubic-bezier(.22,1,.36,1) both; }
        @media (prefers-reduced-motion: reduce) {
          .overlay-fade, .overlay-pop { animation: none; }
        }
      `}</style>

      <div className="overlay-fade absolute inset-0 bg-[#0E1512]/60 backdrop-blur-sm" onClick={onClose} aria-hidden />

      <div className={`overlay-pop relative flex max-h-[85vh] w-full ${maxW} flex-col overflow-hidden rounded-3xl bg-white shadow-[0_40px_100px_-20px_rgba(14,21,18,0.45)]`}>
        <div className="flex shrink-0 items-center justify-between border-b border-[#EAE2D6] bg-white px-6 py-4">
          <h3 className="font-display text-xl font-semibold text-[#1C1917]">{title}</h3>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className="grid h-9 w-9 place-items-center rounded-full text-[#78716C] transition-all duration-200 hover:-rotate-90 hover:bg-orange-50 hover:text-orange-600"
          >
            <X size={18} />
          </button>
        </div>
        <div className="overflow-y-auto p-6">{children}</div>
      </div>
    </div>
  );
}