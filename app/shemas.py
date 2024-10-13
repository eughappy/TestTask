from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
