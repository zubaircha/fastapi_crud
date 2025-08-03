from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema for creating a new user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    password: str  # plain password (will be hashed)

# Schema for returning user data
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str]

    class Config:
        orm_mode = True
