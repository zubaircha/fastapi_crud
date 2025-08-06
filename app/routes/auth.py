# routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from app import models, schemas, database
from app.auth import verify_password, create_access_token,get_current_user,require_admin

router = APIRouter(tags=["Auth"])

@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == login_data.username).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected")
def protected_route(current_user: models.User = Depends(get_current_user)):
    return {"message": f"Helloooooo {current_user.username}, you're authorized!"}
@router.get("/admin-only")
def admin_dashboard(current_user: models.User = Depends(require_admin)):
    return {"message": f"Welcome Admin {current_user.username}!"}
