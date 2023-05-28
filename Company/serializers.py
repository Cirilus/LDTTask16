import logging
import environ
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, IntegerField, \
    Serializer, CharField, SerializerMethodField, DecimalField
from Authentication.models import CustomUser
from .models import Company, Vacancy, Project, Statistic
from Authentication.serializers import CuratorSerializer, TraineeSerializer, UserSerializer
from yandex_geocoder import Client

logger = logging.getLogger(__name__)

env = environ.Env()
environ.Env.read_env()

YandexApiKey = env.str("YANDEX_GEOCODER", "")

yandex_client = Client(YandexApiKey)


class DetailCompanySerializer(ModelSerializer):
    curators = CuratorSerializer(many=True, required=False, read_only=True)
    user = UserSerializer()
    id = IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Company
        fields = ("id", "title", "description", "user", "is_active", "curators")
        extra_kwargs = {
            'is_active': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['user']['password'] = make_password(validated_data['user']['password'])
        user = CustomUser(**validated_data['user'])
        user.save()
        title = validated_data['title']
        description = validated_data['description']
        validated_data.pop('user')
        try:
            company = Company.objects.create(user=user, title=title, description=description)
        except Exception as e:
            logger.error(f"Failed to create Company, the error is {e}")
            user.delete()
        return company


class CompanySerializer(ModelSerializer):
    id = CharField(source="user.id", read_only=True)

    class Meta:
        model = Company
        fields = ("id", "title", "description", "is_active")
        extra_kwargs = {
            'is_active': {'read_only': True},
        }


class AdminVacanciesSerializer(ModelSerializer):
    nameOrg = CharField(source="company.company.title", read_only=True,
                        allow_blank=True, allow_null=True)

    class Meta:
        model = Vacancy
        fields = ("id", "nameJob", "nameOrg", "company", "rating",
                  "status", "adress", "latitude", "longitude", "responsibilities",
                  "requirements", "conditions", "tag",
                  "startOfSelection", "endOfSelection",
                  "startOfTheInternship", "endOfInternship", "imagePreviewImg")
        extra_kwargs = {
            'latitude': {'read_only': True},
            'longitude': {'read_only': True},
            'responsibilities': {'write_only': True},
            'requirements': {'write_only': True},
            'conditions': {'write_only': True},
            "company": {'write_only': True},
        }

    def create(self, validated_data):
        coords = yandex_client.coordinates(validated_data['adress'])
        validated_data['latitude'] = coords[0]
        validated_data['longitude'] = coords[1]
        return super().create(validated_data)


class CoordinatesSerializer(Serializer):
    latitude = DecimalField(max_digits=20, decimal_places=10)
    longitude = DecimalField(max_digits=20, decimal_places=10)


class VacanciesSerializer(ModelSerializer):
    nameOrg = CharField(source="company.company.title", read_only=True,
                              allow_blank=True, allow_null=True)
    coordinates = SerializerMethodField()

    class Meta:
        model = Vacancy
        fields = ("id", "nameJob", "nameOrg", "company", "rating",
                  "adress", "coordinates", "responsibilities",
                  "requirements", "conditions", "tag",
                  "startOfSelection", "endOfSelection",
                  "startOfTheInternship", "endOfInternship", "imagePreviewImg")
        extra_kwargs = {
            'coordinates': {'read_only': True},
            'responsibilities': {'write_only': True},
            'requirements': {'write_only': True},
            'conditions': {'write_only': True},
            'tag': {'write_only': True},
            "company": {'write_only': True},
        }

    def create(self, validated_data):
        coords = yandex_client.coordinates(validated_data['adress'])
        validated_data['latitude'] = coords[0]
        validated_data['longitude'] = coords[1]
        return super().create(validated_data)

    def get_coordinates(self, instance):
        coordinates_data = {
            'latitude': instance.latitude,
            'longitude': instance.longitude
        }
        return CoordinatesSerializer(coordinates_data).data


class DetailVacancySerializer(ModelSerializer):
    nameOrg = CharField(source="company.company.title")
    responsibilities = SerializerMethodField()
    requirements = SerializerMethodField()
    conditions = SerializerMethodField()
    coordinates = SerializerMethodField()

    class Meta:
        model = Vacancy
        fields = ("id", "nameJob",
                  "startOfSelection", "endOfSelection",
                  "startOfTheInternship", "endOfInternship",
                  "nameOrg", "rating", "tag",
                  "responsibilities", "requirements",
                  "conditions", "adress", "coordinates", "imagePreviewImg")

    def get_responsibilities(self, instance):
        return instance.responsibilities.split("&")

    def get_requirements(self, instance):
        return instance.responsibilities.split("&")

    def get_conditions(self, instance):
        return instance.responsibilities.split("&")

    def get_coordinates(self, instance):
        coordinates_data = {
            'latitude': instance.latitude,
            'longitude': instance.longitude
        }
        return CoordinatesSerializer(coordinates_data).data


class UsersVacancySerializer(ModelSerializer):
    curators = CuratorSerializer(many=True, required=False, read_only=True)
    applications = TraineeSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Vacancy
        fields = ("id", "nameJob", "curators", "applications")
        extra_kwargs = {
            'company': {'write_only': True}
        }


class ProjectSerializer(ModelSerializer):
    applications = TraineeSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Project
        fields = ("id", "title", "applications", "company", "short_description", "price", "skills")
        extra_kwargs = {
            'company': {'write_only': True},
        }


class StatisticSerializer(ModelSerializer):
    class Meta:
        model = Statistic
        fields = ("id", "title", "count")


class AddCuratorRequest(Serializer):
    curator_id = IntegerField()
