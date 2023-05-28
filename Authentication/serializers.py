from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, CharField
from .models import CustomUser, Curator, Trainee, Languages, WorkExperience, Education
from rest_framework import serializers
import logging
from project.auth import KeycloakOIDCAuthenticationBackend
from django.conf import settings

logger = logging.getLogger(__name__)


class UserSerializer(ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'firstname', 'lastname', 'avatar', 'password', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True}
        }


class CuratorSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Curator
        fields = ('id', 'user',)

    def create(self, validated_data):
        validated_data['user']['password'] = make_password(validated_data['user']['password'])
        user = CustomUser(**validated_data['user'])
        user.save()
        validated_data.pop('user')
        try:
            curator = Curator.object.create(user=user)
        except Exception as e:
            logger.error(f"Failed to create Curator, the error is {e}")
            user.delete()
        return curator


class LanguagesSerializer(ModelSerializer):
    class Meta:
        model = Languages
        fields = ("language", "level")


class WorkExperienceSerializer(ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ("title_organisation", 'position',
                  "start_work", "end_work", "work_duties")


class EducationSerializer(ModelSerializer):
    class Meta:
        model = Education
        fields = ("graduation", "university", "faculty",
                  "major", "start_education", "end_education",)


class TraineeSerializer(ModelSerializer):
    user = UserSerializer()
    languages = LanguagesSerializer()
    work_experience = WorkExperienceSerializer()
    education_serializer = EducationSerializer()

    class Meta:
        model = Trainee
        fields = ('id', 'user', 'languages',
                  "work_experience", "education_serializer", "surname", "sex",
                  "country", "city", "number", "tag", "native_language", "about_yourself",
                  "vk", "telegram")

    def create(self, validated_data):
        validated_data['user']['password'] = make_password(validated_data['user']['password'])
        user = CustomUser(**validated_data['user'])
        user.save()
        validated_data.pop('user')
        try:
            trainee = Trainee.object.create(user=user, **validated_data)
        except Exception as e:
            logger.error(f"Failed to create Trainee, the error is {e}")
            user.delete()
        return trainee
