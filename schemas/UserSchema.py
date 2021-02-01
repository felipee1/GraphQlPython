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
from database.entitys.User import UserInfoSchema, UserCreate, UserAuthenticate
from datetime import timedelta
import bcrypt

ACCESS_TOKEN_EXPIRE_MINUTES = 5000


db = db_session.session_factory()


class AuthenUser(Mutation):
    class Arguments:
        username = String(required=True)
        password = String(required=True)

    token = String()

    @staticmethod
    def mutate(root, info, username, password):
        db_user = crud.get_user_by_username(db, username=username)
        user_authenticate = UserAuthenticate(
            username=username, password=password)
        if db_user is None:
            raise GraphQLError("Username or e-mail not existed")
        else:
            is_password_correct = crud.check_username_password(
                db, user_authenticate)
            if is_password_correct is False:
                raise GraphQLError("Password is not correct")
            else:
                access_token_expires = timedelta(
                    minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(
                    data={"sub": username}, expires_delta=access_token_expires)
                return AuthenUser(token=access_token)


class UserInput(InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    email = graphene.String(required=True)
    fullName = graphene.String()


class CreateUser(Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserInfoSchema)

    def mutate(self, root, user_data=None):
        hashed_password = bcrypt.hashpw(
            user_data.password.encode('utf-8'), bcrypt.gensalt())
        user = UserInfoSchema(username=user_data.username, email=user_data.email,
                              password=hashed_password, fullName=user_data.fullName)
        ok = True
        db_user = crud.get_user_by_username(db, username=user_data.username)
        if user_data.email.find("@") < 0:
            raise GraphQLError("Invalid E-mail")
        if db_user:
            raise GraphQLError("Username already registered")
        user_info = UserCreate(username=user_data.username, email=user_data.email,
                               password=user_data.password, fullName=user_data.fullName)
        data = crud.create_user(db, user_info)
        return CreateUser(user=data, ok=ok)
