export default function SubscriptionUsageCard({
    usage,
    limits,
    plan
}) {


    const aiRemaining =
        limits.ai_prompt_limit === -1
            ? "Unlimited"
            :
            `${Math.max(
                    limits.ai_prompt_limit - usage.ai_prompts_used,
                    0
                )}/${limits.ai_prompt_limit}`;


    const guidedRemaining =
        limits.guided_plan_limit === -1
            ? "Unlimited"
            :
            `${Math.max(
                limits.guided_plan_limit - usage.guided_plans_used,
                0
            )}/${limits.guided_plan_limit}`;



    return (

        <div
            className="
            rounded-2xl
            bg-white
            border
            border-[#EAE2D6]
            p-6
            "
        >

            <h3
                className="
                text-lg
                font-bold
                mb-5
                "
            >
                {plan === "premium"
                    ? "✨ Premium Plan"
                    : "🌱 Free Plan"
                }
            </h3>


            <div className="space-y-4">


                <div>

                    <div className="flex justify-between text-sm mb-1">

                        <span>
                            AI Consultations
                        </span>

                        <span className="font-semibold">
                            {aiRemaining}
                        </span>

                    </div>

                </div>



                <div>

                    <div className="flex justify-between text-sm mb-1">

                        <span>
                            Guided Trip Plans
                        </span>

                        <span className="font-semibold">
                            {guidedRemaining}
                        </span>

                    </div>

                </div>


            </div>


        </div>

    );

}