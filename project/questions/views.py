from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import uuid
from .models import Test, Questions, Answers
from .serializers import TestSerializer, TestEditSerializer, QuestionsSerializer, QEditSerializer


# from .serializers import GiveSerializer


# создание вопросов
class QView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionsSerializer

    def get(self, request):
        queryset = Questions.objects.all()
        serializer = QuestionsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


# создание теста
class TestsView(APIView):
    permission_classes = (IsAuthenticated,)
    # permission_classes = [AllowAny]
    serializer_class = TestSerializer

    def get(self, request):
        queryset = Test.objects.all()
        serializer = TestSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

# Редактирования теста
class TestsEditView(APIView):
    permission_classes = (IsAuthenticated,)
    # permission_classes = [AllowAny]
    serializer_class = TestEditSerializer
    def get(self, request, id):
        queryset = Test.objects.get(pk=id)
        serializer = TestSerializer(queryset)
        return Response(serializer.data)

    def post(self, request, id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        test = Test.objects.get(pk=id)

        try:
            test.title = serializer.data['title']
        except:
            pass
        try:
            test.end_date = serializer.data['end_date']
        except:
            pass
        try:
            test.description = serializer.data['description']
        except:
            pass
        try:
            test.questions = serializer.data['questions']
        except:
            pass
        try:
            test.is_active = serializer.data['is_active']
        except:
            pass
        test.save()

        return Response(serializer.data)


# Редактирование вопросов
class QEditView(APIView):
    permission_classes = (IsAuthenticated,)
    # permission_classes = [AllowAny]
    serializer_class = QEditSerializer

    def get(self, request, id):
        queryset = Questions.objects.get(pk=id)
        serializer = QuestionsSerializer(queryset)
        return Response(serializer.data)

    def post(self, request, id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        q = Questions.objects.get(pk=id)

        try:
            q.text = serializer.data['text']
        except:
            pass
        try:
            q.one_answer = serializer.data['one_answer']
        except:
            pass
        q.save()

        return Response(serializer.data)


# Удаление теста
class TestDelView(APIView):
    permission_classes = (IsAuthenticated,)
    # permission_classes = [AllowAny]
    serializer_class = TestSerializer

    def get(self, request, id):
        obj = Test.objects.get(pk=id)
        obj.delete()
        return Response({'answer': f'Тест {id} успешно удален'})


# Удаление вопроса
class QDelView(APIView):
    permission_classes = (IsAuthenticated,)
    # permission_classes = [AllowAny]
    serializer_class = QuestionsSerializer

    def get(self, request, id):
        obj = Questions.objects.get(pk=id)
        obj.delete()
        return Response({'answer': f'Вопрос {id} успешно удален'})
# Ниже Пользовтаельская часть

# Список активных опросов
class TestsClientsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Test.objects.filter(is_active=1)
        serializer = TestSerializer(queryset, many=True)
        return Response(serializer.data)


# Прохождение опроса
class StudyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        obj = Test.objects.get(pk=id)
        if obj.is_active == 1:
            queryset = obj.questions.all()
            serializer = QuestionsSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"answer": "Вопрос неактивен"})

    def post(self, request, id):
        if request.session['id']:
            pass
        else:
            request.session['id'] = uuid.uuid4().hex
        student = request.session['id']
        data = request.data['answers']
        string = '|'
        for x in data:
            string += f' {x} |'
        print(string)
        Answers.objects.create(student=student, test_id=id, answers=string)
        return Response({"answer": "Ответы записаны"})


class StudentAnswersView(APIView):
    permission_classes = (IsAuthenticated,)
    # permission_classes = [AllowAny]
    serializer_class = QuestionsSerializer

    def get(self, request, user_id, test_id):
        obj = Answers.objects.get(student=user_id, test_id=test_id)
        answers = obj.answers
        return Response({"answers": answers})
