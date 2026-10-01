import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Sparkles, ArrowLeft } from "lucide-react";
import toast from "react-hot-toast";

import PricingCard from "../components/PricingCard";

import {
    getCurrentSubscription,
    selectSubscriptionPlan,
    createCheckoutSession,
    cancelSubscription
} from "../services/subscriptionApi";
import CancellationProcessingModal from "../components/CancellationProcessingModal";


export default function SubscriptionPlans() {

    const navigate = useNavigate();

    const [subscription, setSubscription] = useState(null);
    const [loading, setLoading] = useState(true);
    const [upgrading, setUpgrading] = useState(false);
    const [cancelling, setCancelling] = useState(false);


    const token = localStorage.getItem("token");



    useEffect(() => {

        loadSubscription();

    }, []);



    const loadSubscription = async () => {

        try {

            const response =
                await getCurrentSubscription(token);


            setSubscription(
                response.subscription
            );


        } catch (error) {

            console.error(
                "Subscription loading failed:",
                error
            );

        } finally {

            setLoading(false);

        }

    };

    const handlePremiumUpgrade = async () => {

        try {

            setUpgrading(true);


            const data = await createCheckoutSession();


            window.location.href =
                data.checkout_url;


        } catch(error) {

            console.error(
                "Payment initialization failed:",
                error
            );


            toast.error(
                "Unable to start payment"
            );


        } finally {

            setUpgrading(false);

        }

    };

    const handleCancelSubscription = async () => {

        try {

            setCancelling(true);
            setUpgrading(true);

            await cancelSubscription();

            for (let i = 0; i < 5; i++) {

                await new Promise(
                    resolve => setTimeout(resolve, 1000)
                );

                const response =
                    await getCurrentSubscription(
                        localStorage.getItem("token")
                    );

                if (response.subscription.plan === "free") {
                    break;
                }
            }

            navigate("/dashboard?subscription=cancelled");

        } catch (error) {

            console.error(
                "Subscription cancellation failed:",
                error
            );

            toast.error(
                "Unable to cancel subscription"
            );

            setCancelling(false);

        } finally {

            setUpgrading(false);
        }
    };



    const handleUpgrade = async (plan) => {

        try {

            setUpgrading(true);


            await selectSubscriptionPlan(
                token,
                plan
            );


            await loadSubscription();


            if (plan === "premium") {

                toast.success(
                    "🎉 Welcome to Serendib AI Premium!"
                );

            } else {

                toast.success(
                    "Free plan activated"
                );

            }


        } catch (error) {

            console.error(
                "Plan selection failed:",
                error
            );


            toast.error(
                "Unable to update subscription"
            );


        } finally {

            setUpgrading(false);

        }

    };



    if (loading) {

        return (

            <div
                className="
                min-h-screen
                bg-[#FFFCF8]
                flex
                items-center
                justify-center
                text-[#57534E]
                "
            >

                Loading plans...

            </div>

        );

    }



    const currentPlan = subscription?.plan;



    return (

        <div
            className="
            min-h-screen
            bg-[#FFFCF8]
            px-6
            py-12
            "
        >

            <div
                className="
                max-w-6xl
                mx-auto
                "
            >


                {/* Back button */}

                <div className="mb-8">

                    <button
                        onClick={() => navigate("/dashboard")}
                        className="
                        flex
                        items-center
                        gap-2
                        text-sm
                        font-medium
                        text-[#57534E]
                        hover:text-orange-600
                        transition-colors
                        "
                    >

                        <ArrowLeft size={18} />

                        Back to Dashboard

                    </button>

                </div>



                {/* Header */}

                <div
                    className="
                    text-center
                    mb-12
                    "
                >

                    <div
                        className="
                        flex
                        justify-center
                        mb-4
                        "
                    >

                        <div
                            className="
                            w-14
                            h-14
                            rounded-2xl
                            bg-orange-100
                            flex
                            items-center
                            justify-center
                            "
                        >

                            <Sparkles
                                size={28}
                                className="text-orange-500"
                            />

                        </div>

                    </div>



                    <h1
                        className="
                        text-4xl
                        font-bold
                        font-serif
                        text-[#1C1917]
                        "
                    >

                        Choose your Serendib AI plan

                    </h1>



                    <p
                        className="
                        mt-3
                        text-[#78716C]
                        "
                    >

                        Unlock smarter travel planning with AI

                    </p>


                </div>




                {/* Pricing Cards */}

                <div
                    className="
                    grid
                    md:grid-cols-2
                    gap-8
                    max-w-4xl
                    mx-auto
                    "
                >


                    <PricingCard

                        title="Free"

                        price="$0"

                        currentPlan={
                            currentPlan === "free"
                        }

                        description="
                        Explore Serendib AI with basic travel planning
                        "

                        features={[
                            "3 AI travel consultations",
                            "3 guided Sri Lanka trip plans",
                            "Basic destination recommendations",
                            "Standard itinerary generation",
                        ]}


                        buttonText={
                            upgrading
                                ? "Updating..."
                                : currentPlan === "free"
                                    ? "Current Plan"
                                    : "Choose Free"
                        }


                        onClick={() =>
                            !upgrading &&
                            currentPlan !== "free" &&
                            handleUpgrade("free")
                        }

                    />





                    <PricingCard

                        title="Premium"

                        price="$9.99"

                        currentPlan={
                            currentPlan === "premium"
                        }

                        description="
                        Unlimited AI-powered travel experiences
                        "

                        highlighted={true}


                        features={[
                            "Unlimited AI travel consultations",
                            "Unlimited guided trip planning",
                            "Advanced personalized recommendations",
                            "Smart route and experience optimization",
                        ]}


                        buttonText={
                            upgrading
                                ? "Updating..."
                                : currentPlan === "premium"
                                    ? "Cancel Plan"
                                    : "Upgrade Premium"
                        }


                        onClick={() =>
                            !upgrading &&
                            (
                                currentPlan === "premium"
                                    ? handleCancelSubscription()
                                    : handlePremiumUpgrade()
                            )
                        }
                    />


                </div>


            </div>

         <CancellationProcessingModal
            isOpen={cancelling}
        />               
        </div>

    );

}