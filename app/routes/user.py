from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database
from app.crud import user as crud  # ✅ This fixes it


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Dependency to get DB session
get_db = database.get_db

# POST /users/ → create a new user
@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

# GET /users/{user_id} → get a user by ID
@router.get("/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# PUT /users/{user_id} → update a user's data
@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user=db_user, updated_data=updated_user)

# DELETE /users/{user_id} → delete a user
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db=db, user=db_user)
    return {"message": "User deleted successfully"}

@router.get("/", response_model=list[schemas.UserOut])
def read_all_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)







