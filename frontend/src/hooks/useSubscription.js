import { useEffect, useState } from "react";

import {
    getCurrentSubscription
} from "../services/subscriptionApi";


export default function useSubscription() {

    const [subscription, setSubscription] = useState(null);
    const [loading, setLoading] = useState(true);


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


        } catch(error){

            console.error(
                "Subscription loading failed",
                error
            );

        }
        finally{

            setLoading(false);

        }

    };


    return {
        subscription,
        loading,

        plan:
            subscription?.plan || "free",

        usage:
            subscription?.usage || {
                ai_prompts_used:0,
                guided_plans_used:0
            },

        limits:
            subscription?.limits || {
                ai_prompt_limit:3,
                guided_plan_limit:3
            },

        refresh:
            loadSubscription
    };
}