from datetime import date
from decimal import Decimal
from typing import Literal,Optional
from pydantic import BaseModel, Field,ConfigDict

class CreateTransaction(BaseModel):
    amount: Decimal
    type: Literal["income", "expense"]
    description: str = Field(..., min_length=3, max_length=50)
    date: date
    category_id: int

class FetchTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    transaction_id: int
    amount: Decimal
    type: Literal["income", "expense"]
    description: str
    date: date
    category_id: int
    user_id: int

class UpdateTransaction(BaseModel):
    aamount: Optional[Decimal] = Field(default=None, gt=0)
    type: Optional[Literal["income", "expense"]] = None
    description: Optional[str] = Field(default=None, min_length=3, max_length=50)
    date: Optional[date] = None
    category_id: Optional[int] = None