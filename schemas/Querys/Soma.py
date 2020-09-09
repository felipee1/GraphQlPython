import graphene
from graphql.execution.executors.asyncio import AsyncioExecutor

class Soma(graphene.ObjectType):
    number1 = graphene.Float()
    number2 = graphene.Float()
    result = graphene.Float()

class SomaInput(graphene.InputObjectType):
    number1 = graphene.Float(required=True)
    number2 = graphene.Float(required=True)

class RelizarSoma(graphene.Mutation):
    class Arguments:
        soma_data = SomaInput(required=True)

    soma = graphene.Field(Soma)

    def mutate(root, info, soma_data=None):
        soma = Soma(
            result = soma_data.number1+soma_data.number2
        )
        return RelizarSoma(soma=soma)
