from pydantic import BaseModel, Field
from typing import Optional
class M(BaseModel):
    amount: Optional[float] = Field(default=None, gt=0)

try:
    M(amount=None)
    print("None is OK")
except Exception as e:
    print(e)

try:
    M(amount=0)
    print("0 is OK")
except Exception as e:
    print("0 fails")
