from sqlalchemy.orm import Session
from app import schemas
from . import models
from passlib.context import CryptContext
import requests

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(db: Session, user):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_agent(db: Session, agent: schemas.AgentCreate, user_id: int):
    db_agent = models.Agent(
        agent_name=agent.agent_name,
        user_id=user_id,
        n8n_webhook_url=agent.n8n_webhook_url,
        workflow_config=agent.workflow_config
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)

    # Trigger the webhook automatically
    payload = {"message": f"Agent {db_agent.agent_name} created successfully!"}
    try:
        response = requests.post(db_agent.n8n_webhook_url, json=payload)
        print(f"Webhook triggered: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Failed to trigger webhook: {str(e)}")

    return db_agent
def get_agents(db: Session, user_id: int):
    return db.query(models.Agent).filter(models.Agent.user_id == user_id).all()
def get_agent(db: Session, agent_id: int, user_id: int):
    return db.query(models.Agent).filter(models.Agent.id == agent_id, models.Agent.user_id == user_id).first()
def update_agent(db: Session, agent_id: int, agent_update, user_id: int):
    db_agent = get_agent(db, agent_id, user_id)
    if db_agent:
        if agent_update.agent_name is not None:
            db_agent.agent_name = agent_update.agent_name
        if agent_update.n8n_webhook_url is not None:
            db_agent.n8n_webhook_url = agent_update.n8n_webhook_url
        if agent_update.workflow_config is not None:
            db_agent.workflow_config = agent_update.workflow_config
        db.commit()
        db.refresh(db_agent)
    return db_agent
def delete_agent(db: Session, agent_id: int, user_id: int):
    db_agent = get_agent(db, agent_id, user_id)
    if db_agent:
        db.delete(db_agent)
        db.commit()
    return db_agent
