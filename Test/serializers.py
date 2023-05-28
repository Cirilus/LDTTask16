from rest_framework.serializers import ModelSerializer, CharField
from .models import ExtendTask, ChoiceTask, ChoiceAnswers, Test


class ExtendTaskSerializer(ModelSerializer):
    class Meta:
        model = ExtendTask
        fields = ("id", "question", "user_answer", "answer", "test",)
        extra_kwargs = {
            'id': {'read_only': True},
            'test': {'write_only': True},
        }


class ChoiceAnswersSerializer(ModelSerializer):
    class Meta:
        model = ChoiceAnswers
        fields = ("id", "answer", "task")
        extra_kwargs = {
            'id': {'read_only': True},
            'task': {'write_only': True},
        }


class ChoiceTaskSerializer(ModelSerializer):
    answers = ChoiceAnswersSerializer(many=True, read_only=True)

    class Meta:
        model = ChoiceTask
        fields = ("id", "question", "test", "right_answer", "answers")
        extra_kwargs = {
            'id': {'read_only': True},
            'right_answer': {'write_only': True},
        }


class TestSerializer(ModelSerializer):
    choice_task = ChoiceTaskSerializer(many=True, read_only=True, required=False)
    extend_task = ExtendTaskSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Test
        fields = ("id", "description", "vacancy", "choice_task", "extend_task")
        extra_kwargs = {
            'id': {'read_only': True},
            'vacancy': {'write_only': True},
        }