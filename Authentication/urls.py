from django.urls import path, include
from rest_framework import routers
from .views import CuratorViews, TraineeViews, login_page
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register('curator', CuratorViews, basename="curator")
router.register('trainee', TraineeViews, basename="trainee")

urlpatterns = [
    # JWT auth
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('login/', login_page),

    path("", include(router.urls)),
]