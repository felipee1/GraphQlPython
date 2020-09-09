import graphene
from graphql.execution.executors.asyncio import AsyncioExecutor

class Mult(graphene.ObjectType):
    number1 = graphene.Float()
    number2 = graphene.Float()
    result = graphene.Float()

class MultInput(graphene.InputObjectType):
    number1 = graphene.Float(required=True)
    number2 = graphene.Float(required=True)

class RelizarMult(graphene.Mutation):
    class Arguments:
        mult_data = MultInput(required=True)

    mult = graphene.Field(Mult)

    def mutate(root, info, mult_data=None):
        mult = Mult(
            result = mult_data.number1*mult_data.number2
        )
        return RelizarMult(mult=mult)
