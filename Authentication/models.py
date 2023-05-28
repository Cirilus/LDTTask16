from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CuratorManager, CustomUserManager, TraineeManager, MentorsManager


def avatar_upload_images(instance, filename):
    return 'authentication/avatars/{filename}'.format(filename=filename)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(verbose_name='никнейм')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    firstname = models.CharField(max_length=30, verbose_name='Имя')
    lastname = models.CharField(max_length=30, verbose_name='Фамилия')
    is_active = models.BooleanField(default=True, verbose_name='Активированный аккаунт')
    is_staff = models.BooleanField(default=False, verbose_name="Админ")

    avatar = models.ImageField(upload_to=avatar_upload_images,
                               default=None,
                               blank=True, null=True,
                               verbose_name="аватар")

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()


class Curator(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name="curator", )
    object = CuratorManager()


class Mentors(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name="mentor")
    object = MentorsManager()


class Trainee(models.Model):
    tag_choice = (
        ('1', "IT-город"),
        ('2', "Медийный город"),
        ('3', "Комфортная городская среда"),
        ('4', "HR-город"),
        ('5', "Социальный город"),
        ('6', "Правовое пространство"),
        ('7', "Городская экономика"),
    )

    sex_choice = (
        ("М", "мужской"),
        ("Ж", "женский")
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="noob", )
    curator = models.ForeignKey(Curator, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="trainees")
    surname = models.TextField(verbose_name="отчество")
    sex = models.CharField(max_length=30, choices=sex_choice, verbose_name="пол")
    country = models.TextField(verbose_name="страна")
    city = models.TextField(verbose_name="город")
    number = models.TextField(verbose_name="номер")

    tag = models.CharField(max_length=30, choices=tag_choice, verbose_name="направление")
    native_language = models.TextField(verbose_name="родной язык")

    about_yourself = models.TextField(verbose_name="о себе")
    vk = models.TextField(verbose_name="вк")
    telegram = models.TextField(verbose_name="телеграм")

    object = TraineeManager()


class Languages(models.Model):
    language = models.TextField(verbose_name="название")
    level = models.TextField(verbose_name="уровень")

    user = models.ForeignKey(Trainee, on_delete=models.CASCADE,
                             related_name="foreign_language", verbose_name="пользователь")


class WorkExperience(models.Model):
    title_organisation = models.TextField(verbose_name="название организации")
    position = models.TextField(verbose_name="позиция")
    start_work = models.DateField(verbose_name="начало работы")
    end_work = models.DateField(verbose_name="окончание работы")
    work_duties = models.TextField(verbose_name="рабочие обязанности")

    user = models.ForeignKey(Trainee, on_delete=models.CASCADE,
                             related_name="work_experience", verbose_name="пользователь")


class Education(models.Model):
    graduation = models.TextField(verbose_name="уровень образования")
    university = models.TextField(verbose_name="учебное заведение")
    faculty = models.TextField(verbose_name="факультет")
    major = models.TextField(verbose_name="специальность")
    start_education = models.DateField(verbose_name="начала обучения")
    end_education = models.DateField(verbose_name="конец обучения")

    user = models.ForeignKey(Trainee, on_delete=models.CASCADE,
                             related_name="education", verbose_name="пользователь")
