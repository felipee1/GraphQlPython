import graphene
from graphene import Field, Schema, String, Int, ObjectType, InputObjectType, Mutation
from graphql.execution.executors.asyncio import AsyncioExecutor
from graphql import GraphQLError
from starlette.graphql import GraphQLApp
from utils.JWTRsesolver import create_access_token
from utils.JWTRsesolver import decode_access_token
from database.models import UserModel
from database.config import crud
from database.config.database import db_session
from database.entitys.User import UserInfoSchema, UserCreate, UserInfoFullSchema
from database.entitys.User import TokenData
from jwt import PyJWTError
from datetime import timedelta
import bcrypt

ACCESS_TOKEN_EXPIRE_MINUTES = 5000


db = db_session.session_factory()


class AdminInput(InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    email = graphene.String(required=True)
    fullName = graphene.String()
    token = graphene.String()


class CreateAdmin(Mutation):
    class Arguments:
        user_data = AdminInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserInfoSchema)

    def mutate(self, root, user_data=None):
        try:
            payload = decode_access_token(data=user_data.token)
            username: str = payload.get("sub")

            if username is None:
                raise GraphQLError("Invalid credentials")
            token_data = TokenData(username=username)
            adm = crud.get_user_by_username(db, username=token_data.username)
            if adm is None:
                raise GraphQLError("Invalid credentials")
            if adm.admin is False or adm.admin is None:
                raise GraphQLError("You don't have the credentials to do this")

        except PyJWTError:
            raise GraphQLError("Invalid credentials")

        hashed_password = bcrypt.hashpw(
            user_data.password.encode('utf-8'), bcrypt.gensalt())
        user = UserInfoFullSchema(username=user_data.username, email=user_data.email,
                                  password=hashed_password, fullName=user_data.fullName)
        ok = True
        db_user = crud.get_user_by_username(db, username=user_data.username)
        db_user_mail = crud.get_user_by_username(db, username=user_data.email)
        if user_data.email.find("@") < 0:
            raise GraphQLError("Invalid E-mail")
        if db_user:
            raise GraphQLError("Admin already registered")
        if db_user_mail:
            raise GraphQLError("E-mail already registered")
        user_info = UserCreate(username=user_data.username, email=user_data.email,
                               password=user_data.password, fullName=user_data.fullName, admin=True)
        data = crud.create_user(db, user_info)
        return CreateAdmin(user=data, ok=ok)
