from django.contrib.auth.models import BaseUserManager
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, *args, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, *args, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, *args, **kwargs):
        return self.create_user(email, password, is_staff=True, is_superuser=True, *args, **kwargs)


class UserSubClassAbstractManager(models.Manager):
    class Meta:
        abstract = True

    def get_subobject_byuser(self, user):
        subuser = super().get_queryset().get(user=user)
        return subuser


class CuratorManager(UserSubClassAbstractManager):

    def is_user_curator(self, user):
        try:
            self.get_subobject_byuser(user=user)
            return True
        except ObjectDoesNotExist:
            return False


class TraineeManager(UserSubClassAbstractManager):
    def is_user_trainee(self, user):
        try:
            self.get_subobject_byuser(user=user)
            return True
        except ObjectDoesNotExist:
            return False


class MentorsManager(UserSubClassAbstractManager):
    def is_user_mentor(self, user):
        try:
            self.get_subobject_byuser(user=user)
            return True
        except ObjectDoesNotExist:
            return False

