from fastapi import FastAPI
from . import models
from .database import engine
from .routes import user, auth  # ✅ import the auth route file

app = FastAPI()

# Create all tables
models.Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(user.router)
app.include_router(auth.router)  # ✅ Add this line
