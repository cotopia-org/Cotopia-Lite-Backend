from passlib.context import CryptContext
from sqlalchemy.orm import Session

from common.http_exceptions import PASS_NOTACCEPTABLE
from db.models import User as UserModel
from schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()


def get_password_hash(password):
    if password is None:
        return None
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate):
    if len(user.password) < 8:
        raise PASS_NOTACCEPTABLE
    password = get_password_hash(user.password)
    db_user = UserModel(username=user.username, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def edit_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(UserModel).get(user_id)

    # Update model class variable from requested fields
    for var, value in vars(user).items():
        if value:
            setattr(db_user, var, value)

    if getattr(user, "password", None):
        if len(user.password) < 8:
            raise PASS_NOTACCEPTABLE
        password = get_password_hash(user.password)
        db_user.password = password

    db.add(db_user)
    db.commit()
    # db.refresh(db_user)
    return db_user
