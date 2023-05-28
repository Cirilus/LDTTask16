from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import DestroyModelMixin, \
    ListModelMixin, RetrieveModelMixin, \
    UpdateModelMixin, CreateModelMixin
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ProjectSerializer, CompanySerializer, \
    AdminVacanciesSerializer, AddCuratorRequest, \
    UsersVacancySerializer, DetailCompanySerializer, DetailVacancySerializer, VacanciesSerializer, StatisticSerializer
from .models import Project, Company, Vacancy, Statistic
from .permissions import IsCompany
from rest_framework.permissions import IsAuthenticated


@extend_schema_view(
    retrieve=extend_schema(
        tags=['company'],
        summary="return company by id",
    ),
    list=extend_schema(
        tags=['company'],
        summary="return all company"
    ),
    destroy=extend_schema(
        tags=['company'],
        summary="delete the company",
    ),
    partial_update=extend_schema(
        tags=['company'],
        summary="update the company"
    ),
    create=extend_schema(
        tags=['company'],
        summary="create the company"
    ),
)
class DetailCompanyViews(GenericViewSet,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin):
    serializer_class = DetailCompanySerializer
    http_method_names = ["patch", "get", "delete", "post"]

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(Company, id=pk)


@extend_schema_view(
    list=extend_schema(
        tags=['company'],
        summary="return all company"
    ),
)
class CompanyViews(GenericViewSet,
                   ListModelMixin):
    serializer_class = CompanySerializer

    def get_queryset(self):
        return Company.objects.all()


class CompanyVacanciesView(GenericViewSet,
                           RetrieveModelMixin):
    serializer_class = UsersVacancySerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['company'],
                   summary='return all vacancys of company',
                   request=None,
                   responses={
                       200: AdminVacanciesSerializer
                   }, )
    def get(self, request):
        pk = self.request.user.pk
        vacancies = get_object_or_404(Vacancy, company__id=pk)
        response = self.serializer_class(vacancies, many=True)

        return response.data


class AddCurator(GenericViewSet):
    serializer_class = AddCuratorRequest

    @extend_schema(tags=['company'],
                   summary='add the curator to company',
                   request=AddCuratorRequest,
                   responses={
                       201: None
                   }, )
    def post(self, request, id):
        curator_id = AddCuratorRequest(request.data).data['curator_id']
        company_id = id
        company = Company.objects.get(pk=company_id).curators.add(curator_id)
        return Response(status=201, data={"message": "ok"})

    @extend_schema(tags=['company'],
                   summary='remove curator from company',
                   request=AddCuratorRequest,
                   responses={
                       201: None
                   },
                   )
    def delete(self, request, id):
        curator_id = AddCuratorRequest(request.data).data['curator_id']
        company_id = id
        company = Company.objects.get(pk=company_id).curators.remove(curator_id)
        return Response(status=201, data={"message": "ok"})


@extend_schema_view(
    list=extend_schema(
        tags=['vacancy-admin'],
        summary="return all vacancy",
        parameters=[OpenApiParameter(name='limit', location=OpenApiParameter.QUERY, description='limit', required=False,
                                     type=int)]
    ),
    destroy=extend_schema(
        tags=['vacancy-admin'],
        summary="delete the vacancy",
    ),
    partial_update=extend_schema(
        tags=['vacancy-admin'],
        summary="update the vacancy"
    ),
    create=extend_schema(
        tags=['vacancy-admin'],
        summary="create the vacancy"
    ),
)
class AdminVacanciesViews(GenericViewSet,
                          ListModelMixin,
                          CreateModelMixin,
                          UpdateModelMixin,
                          DestroyModelMixin):
    serializer_class = AdminVacanciesSerializer
    http_method_names = ["patch", "get", "delete", "post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        limit = self.request.query_params.get("limit")
        if limit:
            return Vacancy.objects.all().prefetch_related("company")[:int(limit)]
        return Vacancy.objects.all().prefetch_related("company")


@extend_schema_view(
    list=extend_schema(
        tags=['vacancy'],
        summary="return all vacancy",
        parameters=[OpenApiParameter(name='limit', location=OpenApiParameter.QUERY, description='limit', required=False,
                                     type=int),
                    OpenApiParameter(name='search', location=OpenApiParameter.QUERY, description='search in nameJob',
                                     required=False,
                                     type=str),
                    OpenApiParameter(name='tag', location=OpenApiParameter.QUERY, description='tag', required=False,
                                     type=str),
                    ]

    ),
)
class UserVacanciesViews(GenericViewSet,
                         ListModelMixin, ):
    serializer_class = VacanciesSerializer
    http_method_names = ["patch", "get", "delete", "post"]

    def get_queryset(self):
        limit = self.request.query_params.get("limit")
        tag = self.request.query_params.get("tag")
        search = self.request.query_params.get("search")
        vacancy = Vacancy.objects.all().prefetch_related("company")
        if tag:
            vacancy = vacancy.filter(tag=tag)
        if search:
            vacancy = vacancy.filter(nameJob__icontains=search)
        if limit:
            return vacancy[:int(limit)]

        return vacancy


@extend_schema_view(
    retrieve=extend_schema(
        tags=['vacancy'],
        summary="return detail info about vacancy"
    ),
)
class DetailVacancyViews(GenericViewSet,
                         RetrieveModelMixin, ):
    serializer_class = DetailVacancySerializer
    http_method_names = ["get"]

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Vacancy, pk=pk)


class SubscribeOnVacancyView(GenericViewSet,
                             RetrieveModelMixin):
    queryset = Vacancy

    @extend_schema(tags=['trainee'],
                   summary='subscribe on vacancy',
                   request=None,
                   responses={
                       200: AdminVacanciesSerializer
                   }, )
    def get(self, request, id):
        user_id = self.request.user.pk
        vacancy_id = id
        self.queryset.objects.get(id=vacancy_id).applications.add(user_id)
        return Response({"message": "ok"})


@extend_schema_view(
    retrieve=extend_schema(
        tags=['project'],
        summary="return vacancy by id",
    ),
    list=extend_schema(
        tags=['project'],
        summary="return all vacancy"
    ),
    destroy=extend_schema(
        tags=['project'],
        summary="delete the vacancy",
    ),
    partial_update=extend_schema(
        tags=['project'],
        summary="update the vacancy"
    ),
    create=extend_schema(
        tags=['project'],
        summary="create the vacancy"
    ),
)
class ProjectViews(GenericViewSet,
                   RetrieveModelMixin,
                   CreateModelMixin,
                   ListModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin):
    serializer_class = ProjectSerializer
    http_method_names = ["patch", "get", "delete", "post"]

    def get_object(self):
        pk = self.kwargs['pk']
        return Project.objects.prefetch_related("applications").get(id=pk)

    def get_queryset(self):
        return Project.objects.all().prefetch_related("applications")


@extend_schema_view(
    list=extend_schema(
        tags=['statistic'],
        summary="return all statistics"
    ),
    create=extend_schema(
        tags=['statistic'],
        summary="create the statistic"
    ),
    partial_update=extend_schema(
        tags=['statistic'],
        summary="update the statistic"
    ),
)
class StatisticViews(GenericViewSet,
                     ListModelMixin,
                     CreateModelMixin,
                     UpdateModelMixin):
    serializer_class = StatisticSerializer
    queryset = Statistic.objects.all()
    http_method_names = ["patch", "get", "delete", "post"]
