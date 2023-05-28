from django.db import models
from Company.models import Vacancy


class Test(models.Model):
    description = models.TextField(verbose_name="описание")
    vacancy = models.ForeignKey(Vacancy, related_name="test",
                                on_delete=models.CASCADE, verbose_name="вакансия")


class ChoiceTask(models.Model):
    test = models.ForeignKey(Test, related_name="choice_task",
                                 on_delete=models.CASCADE, verbose_name="тест")

    question = models.TextField(verbose_name="вопрос")
    right_answer = models.IntegerField(verbose_name="правильный ответ")


class ChoiceAnswers(models.Model):
    answer = models.TextField(verbose_name="ответ")
    task = models.ForeignKey(ChoiceTask, related_name="answers",
                             on_delete=models.CASCADE, verbose_name="задание")


class ExtendTask(models.Model):
    question = models.TextField(verbose_name="вопрос")
    user_answer = models.TextField(verbose_name="ответ пользователя")
    answer = models.TextField(verbose_name="правильный ответ")
    test = models.ForeignKey(Test, related_name="extend_answer",
                             on_delete=models.CASCADE, verbose_name="тест")
