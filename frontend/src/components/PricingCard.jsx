import FeatureItem from "./FeatureItem";

export default function PricingCard({
    title,
    price,
    description,
    features,
    highlighted,
    buttonText,
    onClick,
}) {

    return (
        <div
            className={`
                relative
                rounded-3xl
                p-8
                border
                transition-all

                ${
                    highlighted
                        ? "bg-[#1C1917] text-white border-orange-500 shadow-xl scale-105"
                        : "bg-white border-[#EAE2D6]"
                }
            `}
        >

            {highlighted && (
                <div
                    className="
                        absolute
                        -top-4
                        left-1/2
                        -translate-x-1/2
                        bg-orange-500
                        text-white
                        px-4
                        py-1
                        rounded-full
                        text-xs
                        font-bold
                    "
                >
                    MOST POPULAR
                </div>
            )}


            <h2 className="text-2xl font-bold mb-2">
                {title}
            </h2>


            <p
                className={`
                    text-sm
                    mb-6

                    ${
                        highlighted
                            ? "text-gray-300"
                            : "text-[#78716C]"
                    }
                `}
            >
                {description}
            </p>


            <div className="mb-8 flex items-end gap-1">

                <span className="text-4xl font-bold">
                    {price}
                </span>

                <span
                    className="
                        text-sm
                        opacity-70
                        mb-1
                    "
                >
                    /month
                </span>

            </div>


            <div className="space-y-4 mb-8">

                {features.map((feature, index) => (
                    <FeatureItem key={index}>
                        {feature}
                    </FeatureItem>
                ))}

            </div>


            <button
                onClick={onClick}
                className={`
                    w-full
                    py-3
                    rounded-xl
                    font-semibold
                    transition-all

                    ${
                        highlighted
                            ? "bg-orange-500 text-white hover:bg-orange-600"
                            : "bg-[#FBF3EA] text-[#1C1917] hover:bg-orange-100"
                    }
                `}
            >
                {buttonText}
            </button>


        </div>
    );
}