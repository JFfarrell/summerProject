import graphene
from graphene_django import DjangoObjectType
from .models import Customers


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customers
        fields = ('id', 'name', 'gender')


class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)

    def resolve_all_customers(root, info):
        return Customers.objects.all()


class CreateCustomer(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    gender = graphene.String()

    class Arguments:
        name = graphene.String()
        gender = graphene.String()

    def mutate(self, info, name, gender):
        customer = Customers(name=name, gender=gender)
        customer.save()

        return CreateCustomer(
            id=customer.id,
            name=customer.name,
            gender=customer.gender
        )


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
