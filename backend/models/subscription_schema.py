from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class SubscriptionUsage(BaseModel):

    ai_prompts_used: int = 0

    guided_plans_used: int = 0



class SubscriptionLimits(BaseModel):

    ai_prompt_limit: Optional[int] = None

    guided_plan_limit: Optional[int] = None



class Subscription(BaseModel):

    user_id: str

    plan: Literal[
        "free",
        "premium"
    ] = "free"


    status: Literal[
        "active",
        "expired"
    ] = "active"


    usage: SubscriptionUsage = Field(
        default_factory=SubscriptionUsage
    )


    limits: SubscriptionLimits


    created_at: datetime

    updated_at: datetime