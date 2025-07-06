from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

# User Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    stripe_customer_id = Column(String, nullable=True)

    agents = relationship("Agent", back_populates="owner")

# Agent Table
class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    n8n_webhook_url = Column(String, nullable=False)  # NEW FIELD
    workflow_config = Column(JSON, nullable=True)  # Changed from String to JSON

    owner = relationship("User", back_populates="agents")
    task_logs = relationship("TaskLog", back_populates="agent")

    
# Task Log Table
class TaskLog(Base):
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    task_status = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    agent = relationship("Agent", back_populates="task_logs")
