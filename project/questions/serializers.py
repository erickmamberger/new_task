from django.db.migrations import serializer
from rest_framework import serializers

from .models import Test, Questions, Answers


class AnswersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = '__all__'

class QEditSerializer(serializers.ModelSerializer):
    Q_TYPE = (
        (1, 'Один вариант ответа'),
        (2, 'Несколько вариантов ответа'),
    )
    text = serializers.CharField(max_length=255, required=False)
    one_answer = serializers.BooleanField(required=False)

    class Meta:
        model = Questions
        fields = '__all__'


class QuestionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questions
        fields = '__all__'


class TestEditSerializer(serializers.ModelSerializer):

    title = serializers.CharField(max_length=255, required=False)
    end_date = serializers.CharField(required=False)
    description = serializers.CharField(max_length=1000, required=False)
    is_active = serializers.BooleanField(default=0, required=False)

    class Meta:
        model = Test
        fields = ('id', 'title', 'end_date', 'description', 'is_active',)


class TestSerializer(serializers.ModelSerializer):
    answers = QuestionsSerializer(read_only=True)

    class Meta:
        model = Test
        fields = '__all__'