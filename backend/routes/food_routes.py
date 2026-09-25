from fastapi import APIRouter

from agents.food_agent_node import food_agent_node


router = APIRouter(
    prefix="/api/food",
    tags=["Food Intelligence"]
)



@router.post("/recommend")
def recommend_food(state: dict):

    """
    Local Food & Restaurant Intelligence Agent

    Input:
    Traveller profile + destination recommendations

    Output:
    Restaurant recommendations
    """

    updated_state = food_agent_node(
        state
    )


    return {

        "status": "success",

        "food_recommendations":
            updated_state.get(
                "food_recommendations",
                []
            )
    }