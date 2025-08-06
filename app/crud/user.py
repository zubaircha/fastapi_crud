from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_password_hash

# ✅ Get user by username (for duplicate check)
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# ✅ Get user by ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# ✅ Get all users (optional: use this in GET /users/)
def get_all_users(db: Session):
    return db.query(models.User).all()

# ✅ Create a new user
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ✅ Update user by replacing all fields
def update_user(db: Session, user: models.User, updated_data: schemas.UserCreate):
    user.username = updated_data.username
    user.email = updated_data.email
    user.full_name = updated_data.full_name
    user.hashed_password = updated_data.password + "notreallyhashed"
    db.commit()
    db.refresh(user)
    return user

# ✅ Delete a user
def delete_user(db: Session, user: models.User):
    db.delete(user)
    db.commit()
       
def get_all_users(db: Session):
    return db.query(models.User).all()

