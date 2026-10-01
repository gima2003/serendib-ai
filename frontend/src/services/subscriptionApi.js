const API_URL =
    import.meta.env.VITE_API_URL ||
    "http://127.0.0.1:8000";


export const getCurrentSubscription = async (token) => {

    const response = await fetch(
        `${API_URL}/api/subscription/current`,
        {
            headers:{
                Authorization:`Bearer ${token}`
            }
        }
    );


    const data = await response.json();


    if(!response.ok){
        throw new Error(
            data.detail || "Failed to get subscription"
        );
    }


    return data;
};



export const selectSubscriptionPlan = async (
    token,
    plan
)=>{


    const response = await fetch(
        `${API_URL}/api/subscription/select?plan=${plan}`,
        {
            method:"POST",

            headers:{
                Authorization:`Bearer ${token}`
            }
        }
    );


    const data = await response.json();


    if(!response.ok){
        throw new Error(
            data.detail || "Failed to update subscription"
        );
    }


    return data;
};

export async function checkGuidedPlanAccess(){

    const token = localStorage.getItem("token");


    const response = await fetch(
        "http://127.0.0.1:8000/api/subscription/check-guided-plan",
        {
            headers:{
                Authorization:`Bearer ${token}`
            }
        }
    );


    if(!response.ok){

        const error = await response.json();

        throw {
            status: response.status,
            response:{
                status: response.status
            },
            detail:error
        };

    }


    return response.json();

}

export async function createCheckoutSession() {

    const token = localStorage.getItem("token");

    const response = await fetch(
        "http://127.0.0.1:8000/api/payment/create-checkout",
        {
            method: "POST",

            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        }
    );


    const data = await response.json();


    if (!response.ok) {
        throw new Error(
            data.detail || "Payment initialization failed"
        );
    }


    return data;
}

export async function cancelSubscription() {

    const token = localStorage.getItem("token");

    const response = await fetch(
        "http://127.0.0.1:8000/api/payment/cancel-subscription",
        {
            method: "POST",

            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Failed to cancel subscription"
        );
    }

    return data;
}