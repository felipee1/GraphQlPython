import graphene
from graphene import Field, Schema, String, Int, ObjectType, InputObjectType, Mutation
from graphql.execution.executors.asyncio import AsyncioExecutor
from graphql import GraphQLError
from starlette.graphql import GraphQLApp
from utils.JWTRsesolver import create_access_token
from utils.JWTRsesolver import decode_access_token
from database.models import ProductModel
from database.config import crud
from jwt import PyJWTError
from database.config.database import db_session
from database.entitys.Product import ProductInfoSchema, ProductInfoBase, ProductCreate, ProductInformation
from database.entitys.User import TokenData
from datetime import timedelta
import bcrypt

db = db_session.session_factory()


class ProductQuery(graphene.ObjectType):

    all_products = graphene.List(ProductInfoSchema)

    def resolve_all_products(self, info):
        query = ProductInfoSchema.get_query(info)  # SQLAlchemy query
        return query.all()


class ProductInput(InputObjectType):
    productName = graphene.String(required=True)
    code = graphene.String(required=True)
    price = graphene.String(required=True)
    description = graphene.String()
    token = graphene.String()


class CreateProduct(Mutation):
    class Arguments:
        product_data = ProductInput(required=True)

    ok = graphene.Boolean()
    product = graphene.Field(lambda: ProductInfoSchema)

    def mutate(self, root, product_data=None):
        try:
            payload = decode_access_token(data=product_data.token)
            username: str = payload.get("sub")

            if username is None:
                raise GraphQLError("Invalid credentials")
            token_data = TokenData(username=username)

        except PyJWTError:
            raise GraphQLError("Invalid credentials")

        user = crud.get_user_by_username(db, username=token_data.username)

        if user is None:
            raise GraphQLError("Invalid credentials")
        product = ProductInfoSchema(productName=product_data.productName, code=product_data.code,
                                    price=product_data.price, description=product_data.description, userId=user.id)
        ok = True
        db_product = crud.get_by_param(
            db, param=ProductModel.ProductInfo, field=ProductModel.ProductInfo.productName, data=product_data.productName)
        if db_product:
            raise GraphQLError("Product already registered")

        product_info = ProductCreate(productName=product_data.productName, code=product_data.code,
                                     price=product_data.price, description=product_data.description, userId=user.id)

        data = crud.create_any(db, ProductModel.ProductInfo(productName=product_info.productName, code=product_info.code,
                                                            price=product_info.price, description=product_info.description, userId=user.id))

        return CreateProduct(product=data, ok=ok)
