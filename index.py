import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from schemas.schemas import Query, Mutations
from graphql.execution.executors.asyncio import AsyncioExecutor

app = FastAPI()
app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutations), executor_class=AsyncioExecutor))
