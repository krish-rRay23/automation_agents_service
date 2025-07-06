from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, crud
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()

# Create Agent
@router.post("/agents", response_model=schemas.AgentOut)
def create_agent(agent: schemas.AgentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_agent(db, agent, current_user.id)

# Get All Agents
@router.get("/agents", response_model=list[schemas.AgentOut])
def read_agents(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_agents(db, current_user.id)

# Get Single Agent
@router.get("/agents/{agent_id}", response_model=schemas.AgentOut)
def read_agent(agent_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_agent = crud.get_agent(db, agent_id, current_user.id)
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agent

# Update Agent
@router.put("/agents/{agent_id}", response_model=schemas.AgentOut)
def update_agent(agent_id: int, agent: schemas.AgentUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_agent = crud.update_agent(db, agent_id, agent, current_user.id)
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agent

# Delete Agent
@router.delete("/agents/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_agent = crud.delete_agent(db, agent_id, current_user.id)
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted successfully"}
