import sys
from sqlalchemy.orm import Session
from database.entitys import User
from database.entitys.User import UserAuthenticate
from database.models import UserModel
import bcrypt


def get_user_by_username(db: Session, username: str):
    user = db.query(UserModel.UserInfo).filter(
        UserModel.UserInfo.username == username).first()
    email = db.query(UserModel.UserInfo).filter(
        UserModel.UserInfo.email == username).first()
    byid = db.query(UserModel.UserInfo).filter(
        UserModel.UserInfo.id == int(username)).first()
    return user or email or byid


def get_by_param(db: Session, param: any, field: any, data: any):
    return db.query(param).filter(field == data).first()


def create_any(db: Session, model: any):
    db_data = model
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def update_any(db: Session, model: any):
    db_data = model
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def create_user(db: Session, user: User.UserCreate):
    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'), bcrypt.gensalt()).decode()
    db_user = UserModel.UserInfo(
        username=user.username, email=user.email, password=hashed_password, fullName=user.fullName, admin=user.admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_username_password(db: Session, user: UserAuthenticate):
    db_user_info: UserModel.UserInfo = get_user_by_username(
        db, username=user.username)
    return bcrypt.checkpw(user.password.encode('utf-8'), db_user_info.password.encode('utf-8'))
