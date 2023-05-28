from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Mentors, Trainee, Curator


class IsMentors(BasePermission):
    def has_permission(self, request, view):
        return Mentors.objects.is_user_hr(request.user)


class IsTrainee(BasePermission):
    def has_permission(self, request, view):
        return Trainee.objects.is_user_hr(request.user)


class IsCurator(BasePermission):
    def has_permission(self, request, view):
        return Curator.objects.is_user_hr(request.user)
