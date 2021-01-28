import graphene
from graphene import Field, Schema, String, Int, ObjectType, InputObjectType, Mutation
from graphql.execution.executors.asyncio import AsyncioExecutor
from graphql import GraphQLError
from starlette.graphql import GraphQLApp
from utils.JWTRsesolver import create_access_token
from datetime import timedelta

class AuthenUser(Mutation):
    class Arguments:
        username = String(required=True)
        password = String(required=True)

    token = String()

    @staticmethod
    def mutate(root, info, username, password):
        db_user = 'teste'
        if db_user is None:
            raise GraphQLError("Username not existed")
        else:
            is_password_correct = True
            if is_password_correct is False:
                raise GraphQLError("Password is not correct")
            else:                
                access_token_expires = timedelta(minutes=5)                
                access_token = create_access_token(
                    data={"sub": username}, expires_delta=access_token_expires)
                return AuthenUser(token=access_token)
