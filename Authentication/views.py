from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import DestroyModelMixin, \
    ListModelMixin, RetrieveModelMixin, \
    UpdateModelMixin, CreateModelMixin
from django.shortcuts import get_object_or_404, get_list_or_404, render

from .serializers import CuratorSerializer, TraineeSerializer, UserSerializer
from .models import Curator, Trainee
from rest_framework.permissions import IsAuthenticated


@extend_schema_view(
    retrieve=extend_schema(
        tags=['curators'],
        summary="return curator by id",
    ),
    list=extend_schema(
        tags=['curators'],
        summary="return all curators"
    ),
    destroy=extend_schema(
        tags=['curators'],
        summary="delete the curator",
    ),
    partial_update=extend_schema(
        tags=['curators'],
        summary="update the curator"
    ),
    create=extend_schema(
        tags=['curators'],
        summary="create the curator",
    ),
)
class CuratorViews(GenericViewSet,
                   RetrieveModelMixin,
                   CreateModelMixin,
                   ListModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin):
    serializer_class = CuratorSerializer
    http_method_names = ["patch", "get", "delete", "post"]

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(Curator, id=pk)

    def get_queryset(self):
        return Curator.object.all()


@extend_schema_view(
    retrieve=extend_schema(
        tags=['trainee'],
        summary="return trainee by id",
    ),
    list=extend_schema(
        tags=['trainee'],
        summary="return all trainees"
    ),
    destroy=extend_schema(
        tags=['trainee'],
        summary="delete the trainee",
    ),
    partial_update=extend_schema(
        tags=['trainee'],
        summary="update the trainee"
    ),
    create=extend_schema(
        tags=['trainee'],
        summary="create the curator",
    ),
)
class TraineeViews(GenericViewSet,
                   RetrieveModelMixin,
                   CreateModelMixin,
                   ListModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin):
    serializer_class = TraineeSerializer
    http_method_names = ["patch", "get", "delete", "post"]

    def get_object(self):
        print(self.request.user)
        pk = self.kwargs['pk']
        return get_object_or_404(Trainee, id=pk)

    def create(self, request, *args, **kwargs):
        print(self.request.user)
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return Trainee.object.all()


def login_page(request):
    return render(request, "templates/login.html")
