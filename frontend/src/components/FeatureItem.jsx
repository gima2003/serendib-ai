import { Check } from "lucide-react";


export default function FeatureItem({
    children
}) {

    return (
        <div className="flex items-center gap-3 text-sm text-[#57534E]">

            <div className="w-5 h-5 rounded-full bg-orange-100 flex items-center justify-center">
                <Check
                    size={13}
                    className="text-orange-600"
                />
            </div>

            <span>
                {children}
            </span>

        </div>
    );
}