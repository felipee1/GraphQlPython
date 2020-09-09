import graphene
from schemas.Person import Person
from schemas.Mult import RelizarMult
from schemas.Soma import RelizarSoma

class Query(graphene.ObjectType):
    person = graphene.Field(Person)


class Mutations(graphene.ObjectType):
    soma = RelizarSoma.Field()
    multiplicar = RelizarMult.Field()