import graphene
from schemas.UserSchema import CreateUser, AuthenUser
from schemas.AdminSchema import CreateAdmin
from schemas.ProductSchema import CreateProduct, ProductQuery, UpdateProduct


class Query(ProductQuery, graphene.ObjectType):
    pass


class Mutations(graphene.ObjectType):
    UpdateProduct = UpdateProduct.Field()
    Register = CreateUser.Field()
    AdminRegister = CreateAdmin.Field()
    Login = AuthenUser.Field()
    NewProduct = CreateProduct.Field()
