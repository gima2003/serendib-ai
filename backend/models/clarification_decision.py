from typing import Literal
from pydantic import BaseModel

class ClarificationDecision(BaseModel):

    action: Literal[
        "continue_clarification",
        "finalize_available_profile",
        "request_clear_permission",
    ]

    message: str | None = None