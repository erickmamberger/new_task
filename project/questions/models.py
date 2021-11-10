from django.db import models


class Questions(models.Model):
    text = models.CharField(max_length=255, null=False)
    # Q_TYPE = (
    #     (1, 'Один вариант ответа'),
    #     (2, 'Несколько вариантов ответа'),
    # )
    one_answer = models.BooleanField(default=1)


class Test(models.Model):

    title = models.CharField(max_length=255)
    start_date = models.CharField(max_length=255)
    end_date = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=0)
    questions = models.ManyToManyField(Questions)


class Answers(models.Model):

    student = models.CharField(max_length=255)
    test_id = models.IntegerField()
    answers = models.CharField(max_length=3000)