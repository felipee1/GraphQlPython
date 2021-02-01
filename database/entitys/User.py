from graphene_sqlalchemy import SQLAlchemyObjectType
from database.models.UserModel import UserInfo
from pydantic import BaseModel


class UserInfoBase(BaseModel):
    username: str


class UserCreate(UserInfoBase):
    fullName: str
    email: str
    password: str


class UserAuthenticate(UserInfoBase):
    password: str


class UserInformation(UserInfoBase):
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
