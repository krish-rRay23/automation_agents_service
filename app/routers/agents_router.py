from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column
from .. import schemas, models, crud
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()

def get_user_id(user):
    # Handles both ORM instances and accidental class/Column usage
    if hasattr(user, 'id'):
        if isinstance(user.id, Column):
            return 0
        try:
            return int(user.id)
        except Exception:
            return 0
    return 0

# Create Agent
@router.post("/agents", response_model=schemas.AgentOut)
def create_agent(
    agent: schemas.AgentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_agent(db, agent, get_user_id(current_user))

# Get All Agents
@router.get("/agents", response_model=list[schemas.AgentOut])
def read_agents(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_agents(db, user_id=get_user_id(current_user))

# Get Single Agent
@router.get("/agents/{agent_id}", response_model=schemas.AgentOut)
def read_agent(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user_id = get_user_id(current_user)
    db_agent = crud.get_agent(db, agent_id, user_id)
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agent

# Update Agent
@router.put("/agents/{agent_id}", response_model=schemas.AgentOut)
def update_agent(
    agent_id: int,
    agent: schemas.AgentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user_id = get_user_id(current_user)
    db_agent = crud.update_agent(db, agent_id, agent, user_id)
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agent

# Delete Agent
@router.delete("/agents/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_agent = crud.delete_agent(db, agent_id, get_user_id(current_user))
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted successfully"}

# Run Agent Workflow
@router.post("/agents/{agent_id}/run")
def run_agent(agent_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    agent = crud.get_agent(db, agent_id, get_user_id(current_user))
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")

    from app.agent_graph import graph  # import your compiled LangGraph
    # Use agent.workflow_config or a default input for the workflow
    workflow_config = getattr(agent, 'workflow_config', None)
    if isinstance(workflow_config, Column) or not workflow_config
        workflow_input = "Start task"
    else:
        workflow_input = workflow_config.get("input", "Start task")
    result = graph.invoke({"input": workflow_input})

    return {"status": "Workflow complete", "result": result}
