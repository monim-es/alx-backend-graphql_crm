import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation

class Query(CRMQuery, graphene.ObjectType):
    # hello = graphene.String()

    # def resolve_hello(self, info):
    #     return "Hello, GraphQL!"
    pass

class Mutation(CRMMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
# schema = graphene.Schema(query=Query, mutation=Mutation, types=[CustomerType, ProductType, OrderType])



