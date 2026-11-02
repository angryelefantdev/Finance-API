from pydantic import BaseModel,Field

class UserCreate(BaseModel):
    username:str = Field(...,min_length=3,max_length=50,description="Username")
    password:str = Field(...,min_length=8,max_length=128)

class FetchUser(BaseModel):
    id:int
    username:str

    class Config:
            from_attributes = True
