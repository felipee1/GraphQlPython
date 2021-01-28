import sys
from sqlalchemy.orm import Session
from entitys import User
from models import UserModel
import bcrypt


def get_user_by_username(db: Session, username: str):
    return db.query(UserModel.UserInfo).filter(UserModel.UserInfo.username == username).first()


def create_user(db: Session, user: User.UserCreate):
    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = UserModel.UserInfo(
        username=user.username, password=hashed_password, fullname=user.fullname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_username_password(db: Session, user: User.UserAuthenticate):
    db_user_info: UserModel.UserInfo = get_user_by_username(
        db, username=user.username)
    return bcrypt.checkpw(user.password.encode('utf-8'), db_user_info.password.encode('utf-8'))
