from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import DestroyModelMixin, \
    ListModelMixin, RetrieveModelMixin, \
    UpdateModelMixin, CreateModelMixin
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import TestSerializer, \
    ChoiceTaskSerializer, ExtendTaskSerializer, ChoiceAnswersSerializer

from .models import Test, ChoiceTask, ExtendTask, ChoiceAnswers, Vacancy


@extend_schema_view(
    retrieve=extend_schema(
        tags=['test'],
        summary="return test by id",
    ),
    destroy=extend_schema(
        tags=['test'],
        summary="delete the test",
    ),
    partial_update=extend_schema(
        tags=['test'],
        summary="update the test"
    ),
    create=extend_schema(
        tags=['test'],
        summary="create the test"
    ),
)
class TestView(GenericViewSet,
               DestroyModelMixin,
               UpdateModelMixin,
               RetrieveModelMixin,
               CreateModelMixin):
    serializer_class = TestSerializer
    queryset = Test
    http_method_names = ["patch", "get", "delete", "post"]


@extend_schema_view(
    retrieve=extend_schema(
        tags=['test'],
        summary="return choice_answers by id",
    ),
    destroy=extend_schema(
        tags=['test'],
        summary="delete the choice_answers",
    ),
    partial_update=extend_schema(
        tags=['test'],
        summary="update the choice_answers"
    ),
    create=extend_schema(
        tags=['test'],
        summary="create the choice_answers"
    ),
)
class ChoiceTaskView(GenericViewSet,
                     DestroyModelMixin,
                     UpdateModelMixin,
                     RetrieveModelMixin,
                     CreateModelMixin, ):
    serializer_class = ChoiceTaskSerializer
    queryset = ChoiceTask
    http_method_names = ["patch", "get", "delete", "post"]


@extend_schema_view(
    retrieve=extend_schema(
        tags=['test'],
        summary="return choice_task by id",
    ),
    destroy=extend_schema(
        tags=['test'],
        summary="delete the choice_task",
    ),
    partial_update=extend_schema(
        tags=['test'],
        summary="update the choice_task"
    ),
    create=extend_schema(
        tags=['test'],
        summary="create the choice_task"
    ),
)
class ChoiceAnswersView(GenericViewSet,
                        DestroyModelMixin,
                        UpdateModelMixin,
                        RetrieveModelMixin,
                        CreateModelMixin, ):
    serializer_class = ChoiceAnswersSerializer
    queryset = ChoiceAnswers
    http_method_names = ["patch", "get", "delete", "post"]


@extend_schema_view(
    retrieve=extend_schema(
        tags=['test'],
        summary="return extend_task by id",
    ),
    destroy=extend_schema(
        tags=['test'],
        summary="delete the extend_task",
    ),
    partial_update=extend_schema(
        tags=['test'],
        summary="update the extend_task"
    ),
    create=extend_schema(
        tags=['test'],
        summary="create the extend_task"
    ),
)
class ExtendTaskView(GenericViewSet,
                     DestroyModelMixin,
                     UpdateModelMixin,
                     RetrieveModelMixin,
                     CreateModelMixin,):
    serializer_class = ExtendTaskSerializer
    queryset = ExtendTask
    http_method_names = ["patch", "get", "delete", "post"]

# TODO check why this method not in swagger
@extend_schema_view(
    retrieve=extend_schema(
        tags=['test12'],
        summary="return test for the vacancy",
    ),
)
class VacancyTestsView(GenericViewSet,
                       RetrieveModelMixin):
    serializer_class = TestSerializer

    def get_object(self, id):
        return get_object_or_404(Vacancy, pk=id).test
