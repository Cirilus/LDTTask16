import graphene
from graphene_django import DjangoObjectType

from .models import Vacancy, Company


class CompanyType(DjangoObjectType):
    class Meta:
        model = Company
        fields = ("id", "title", "description", "user", "is_active", "curators")

class VacancyType(DjangoObjectType):
    company = graphene.List(CompanyType)
    class Meta:
        model = Vacancy
        fields = ("id", "applications", "company", "curators",
                  "short_description", "description", "salary",
                  "skills")


class Query(graphene.ObjectType):
    all_vacancies = graphene.List(VacancyType)

    def resolve_all_vacancies(self, info):
        return Vacancy.objects.select_related("company").all()



schema = graphene.Schema(query=Query)