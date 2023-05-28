from django.urls import path, include
from rest_framework import routers
from .views import TestView, ChoiceTaskView, ExtendTaskView, \
    ChoiceAnswersView, VacancyTestsView


router = routers.DefaultRouter()
router.register('', TestView, basename="test")

router.register('choice_task', ChoiceTaskView, basename="choice_task")
router.register('choice_answers', ChoiceAnswersView, basename="choice_answers")


router.register('extend_task', ExtendTaskView, basename="extend_task")


urlpatterns = [
    path("", include(router.urls)),
    path('vacancy/<int:id>', VacancyTestsView.as_view({"get:get"}), name="vacancy's test")
]
