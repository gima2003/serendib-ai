from pydantic import BaseModel
from typing import List, Optional



class FoodRecommendation(BaseModel):

    restaurant_name: str

    cuisine_type: Optional[str]

    price_level: Optional[str]

    rating: Optional[float]


    suitable_for: List[str]


    recommended_dishes: List[str]


    reasoning: List[str]



class DestinationFoodRecommendation(BaseModel):

    destination: str

    restaurants: List[FoodRecommendation]



class FoodAgentResponse(BaseModel):

    food_recommendations: List[
        DestinationFoodRecommendation
    ]