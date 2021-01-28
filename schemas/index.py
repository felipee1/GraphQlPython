import graphene
from schemas.UserSchema import PersonQuery, CreateUser
from schemas.AuthUser import AuthenUser

class Query(PersonQuery,graphene.ObjectType):
    pass


class Mutations(graphene.ObjectType):
    NewPerson = CreatePerson.Field()
    Login = AuthenUser.Field()