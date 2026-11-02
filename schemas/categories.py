from pydantic import BaseModel, Field, ConfigDict

class CreateCategory(BaseModel):
    category_name: str = Field(..., min_length=2, max_length=100)

class FetchCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_id: int
    category_name: str
    user_id: int