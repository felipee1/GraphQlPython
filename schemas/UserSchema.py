import graphene
from graphene import Field, Schema, String, Int, ObjectType, InputObjectType, Mutation
from graphql.execution.executors.asyncio import AsyncioExecutor
from graphql import GraphQLError
from utils.JWTRsesolver import decode_access_token
from database.config import crud
from database.models import UserModel
from database.database import db_session
from database.entitys import UserInfoSchema, UserCreate

import bcrypt

db = db_session.session_factory()


class Person(ObjectType):
    username = graphene.String(required=True)
    fullname = graphene.String()


class PersonQuery(ObjectType):
    person = Field(Person, token=String(required=True))

    def resolve_person(self, root, token):
        datas = decode_access_token(data=token)
        return {"name": "jorge", "age": 13}


class PersonInput(InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    fullname = graphene.String()


class CreateUser(Mutation):
    class Arguments:
        user_data = PersonInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserInfoSchema)

    def mutate(self, root, info, user_data=None):
        hashed_password = bcrypt.hashpw(
            user_data.password.encode('utf-8'), bcrypt.gensalt())
        user = UserInfoSchema(username=user_data.username,
                              password=hashed_password, fullname=user_data.fullname)
        ok = True
        db_user = crud.get_user_by_username(db, username=user_data.username)
        if db_user:
            raise GraphQLError("Username already registered")
        user_info = UserCreate(username=user_data.username,
                               password=user_data.password, fullname=user_data.fullname)
        crud.create_user(db, user_info)
        return CreateUser(user=user, ok=ok)
