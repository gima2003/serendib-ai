SUBSCRIPTION_PLANS = {

    "free": {

        "name": "Free Explorer",

        "price": 0,

        "currency": "USD",

        "billing_period": "forever",


        "limits": {

            "ai_prompt_limit": 3,

            "guided_plan_limit": 3

        },


        "features": [

            "Basic AI travel planning",

            "3 AI conversations",

            "3 guided trip generations",

            "Basic destination recommendations"

        ]

    },


    "premium": {

        "name": "Serendib Explorer",

        "price": 4.99,

        "currency": "USD",

        "billing_period": "monthly",


        "limits": {

            "ai_prompt_limit": -1,

            "guided_plan_limit": -1

        },


        "features": [

            "Unlimited AI travel planning",

            "Unlimited guided trip generation",

            "Advanced personalization",

            "Smart route optimization",

            "Food and accommodation intelligence",

            "Priority trip customization"

        ]

    }

}