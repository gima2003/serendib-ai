import { Sparkles, X } from "lucide-react";
import { useNavigate } from "react-router-dom";


export default function UpgradeModal({
    isOpen,
    onClose,
    feature = "ai_prompt"
}) {

    const navigate = useNavigate();
    const content = {

        ai_prompt:{
            title:"✨ AI Consultation Limit Reached",
            description:
            "You've used all 3 free AI conversations. Upgrade to Premium for unlimited AI travel assistance."
        },


        guided_plan:{
            title:"✨ Guided Trip Limit Reached",
            description:
            "You've used all 3 free guided trip plans. Upgrade to Premium for unlimited itinerary generation."
        }

    };


    if (!isOpen) return null;


    return (

        <div
            className="
            fixed inset-0
            z-50
            flex
            items-center
            justify-center
            bg-black/40
            backdrop-blur-sm
            "
        >

            <div
                className="
                bg-white
                rounded-3xl
                p-8
                max-w-md
                w-full
                mx-4
                shadow-xl
                "
            >

                <div className="flex justify-between items-start">

                    <div
                        className="
                        w-12 h-12
                        rounded-2xl
                        bg-orange-100
                        flex
                        items-center
                        justify-center
                        "
                    >
                        <Sparkles
                            className="text-orange-500"
                        />
                    </div>


                    <button
                        onClick={onClose}
                    >
                        <X size={20}/>
                    </button>

                </div>


                <h2
                    className="
                    mt-6
                    text-2xl
                    font-bold
                    text-[#1C1917]
                    "
                >
                    {content[feature]?.title || "You've reached your limit"}
                </h2>


                <p
                    className="
                    mt-3
                    text-[#78716C]
                    "
                >
                    {content[feature]?.description || "You've reached your limit"}
                </p>


                <button
                    onClick={() => navigate("/subscription")}
                    className="
                    mt-6
                    w-full
                    rounded-xl
                    bg-orange-500
                    text-white
                    py-3
                    font-semibold
                    hover:bg-orange-600
                    "
                >
                    Upgrade to Premium
                </button>


            </div>

        </div>

    );

}