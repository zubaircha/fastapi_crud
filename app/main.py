from fastapi import FastAPI
from . import models
from .database import engine
from .routes import user

app = FastAPI()

# Create database tables on startup
models.Base.metadata.create_all(bind=engine)


# Include user routes
app.include_router(user.router)
