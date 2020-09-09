import graphene
from schemas.Querys.Person import Person
from schemas.Querys.Mult import RelizarMult
from schemas.Querys.Soma import RelizarSoma

class Query(graphene.ObjectType):
    person = graphene.Field(Person)


class Mutations(graphene.ObjectType):
    soma = RelizarSoma.Field()
    multiplicar = RelizarMult.Field()