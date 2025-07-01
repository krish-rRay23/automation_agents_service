from pydantic import BaseModel, EmailStr

# User Input Schema (For registration)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# User Response Schema (What we send back)
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
