from django.contrib.auth import get_user_model
from django.db import models
from Authentication.models import Trainee, Curator, CustomUser


class Company(models.Model):
    user = models.OneToOneField(CustomUser, related_name="company",
                                unique=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, unique=True)
    description = models.CharField(max_length=500)
    curators = models.ManyToManyField(CustomUser, related_name="companies",
                                      blank=True)
    is_active = models.BooleanField(default=False, verbose_name='Аккредитована ли компания')


def vacancy_upload_images(instance, filename):
    return 'vacancy/images/{filename}'.format(filename=filename)

class Vacancy(models.Model):
    tag_choice = (
        ('1', "IT-город"),
        ('2', "Медийный город"),
        ('3', "Комфортная городская среда"),
        ('4', "HR-город"),
        ('5', "Социальный город"),
        ('6', "Правовое пространство"),
        ('7', "Городская экономика"),
    )

    status_choice = (
        ('-1', "заявка отклонена"),
        ('0', "на рассмотрение"),
        ('1', "заявка одобрена"),
    )

    nameJob = models.CharField(max_length=500)

    applications = models.ManyToManyField(CustomUser, related_name="uservacancies",
                                          blank=True)

    company = models.ForeignKey(CustomUser, related_name="companyvacancies", on_delete=models.CASCADE)
    curators = models.ManyToManyField(CustomUser, related_name="curatorsvacancies",
                                      blank=True, null=True)

    tag = models.CharField(max_length=30, choices=tag_choice)
    status = models.CharField(max_length=30, choices=status_choice, default='0')

    imagePreviewImg = models.ImageField(upload_to=vacancy_upload_images,
                                        verbose_name="привью", blank=True, null=True)

    responsibilities = models.TextField(verbose_name="обязанности")
    requirements = models.TextField(verbose_name="требования")
    conditions = models.TextField(verbose_name="условия")

    rating = models.DecimalField(max_digits=2, decimal_places=1)

    adress = models.TextField(verbose_name="локация")
    latitude = models.DecimalField(max_digits=20, decimal_places=10)
    longitude = models.DecimalField(max_digits=20, decimal_places=10)

    startOfSelection = models.DateField(verbose_name="начала отбора на стажировку")
    endOfSelection = models.DateField(verbose_name="конец отбора на стажировку")
    startOfTheInternship = models.DateField(verbose_name="начала стажировки")
    endOfInternship = models.DateField(verbose_name="конец стажировки")


class Project(models.Model):
    title = models.CharField(max_length=500)

    applications = models.ManyToManyField(CustomUser, related_name="userprojects",
                                          blank=True)

    company = models.ForeignKey(CustomUser, related_name="companyprojects", on_delete=models.CASCADE,
                                blank=True, null=True)

    short_description = models.CharField(max_length=500)
    description = models.CharField(max_length=500)

    price = models.CharField(max_length=500)
    skills = models.CharField(max_length=500)


class Statistic(models.Model):
    title = models.TextField()
    count = models.IntegerField()