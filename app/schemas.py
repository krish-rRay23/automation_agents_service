from pydantic import BaseModel, EmailStr
from typing import Optional

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


class AgentBase(BaseModel):
    agent_name: str
    n8n_webhook_url: str
    workflow_config: Optional[dict] = None  # Optional JSON field

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    agent_name: Optional[str] = None
    n8n_webhook_url: Optional[str] = None
    workflow_config: Optional[dict] = None

class AgentOut(AgentBase):
    id: int

    class Config:
        orm_mode = True