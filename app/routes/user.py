from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database
from app.crud import user as crud  # ✅ This fixes it
from app.auth import get_current_user,require_admin
from app import models



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Dependency to get DB session
get_db = database.get_db

@router.get("/protected")
def protected_route(current_user: models.User = Depends(get_current_user)):
    return {"message": f"Helloooooo {current_user.username}, you're authorized!"}

@router.get("/admin-only")
def admin_dashboard(current_user: models.User = Depends(require_admin)):
    return {"message": f"Welcome Admin {current_user.username}!"}

@router.get("/", response_model=list[schemas.UserOut])
def read_all_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user=db_user, updated_data=updated_user)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db=db, user=db_user)
    return {"message": "User deleted successfully"}
