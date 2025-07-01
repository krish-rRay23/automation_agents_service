from fastapi import FastAPI
from . import models
from .database import engine
from .routers import auth_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add this line to include the auth routes
app.include_router(auth_router.router)

@app.get("/")
def read_root():
    return {"message": "Automation Agents Service is running 🚀"}
