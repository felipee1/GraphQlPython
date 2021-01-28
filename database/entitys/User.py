from graphene_sqlalchemy import SQLAlchemyObjectType
from models import UserModel
from pydantic import BaseModel


class UserInfoBase(BaseModel):
    username: str


class UserCreate(UserModel):
    username: str
    fullname: str
    password: str


class UserAuthenticate(UserModel):
    username: str
    password: str


class UserInformation(UserModel):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class UserInfoSchema(SQLAlchemyObjectType):
    class Meta:
        model = UserInfo
