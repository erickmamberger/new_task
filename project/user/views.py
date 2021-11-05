import os
from threading import Thread

from PIL import Image
from rest_framework import status, generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import mailing_func
from .models import User, Like
from .serializers import LoginSerializer, GiveSerializer, UserSerializer
from .serializers import RegistrationSerializer


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        photo = serializer.validated_data['photo']

        base_image = Image.open(photo)
        watermark = Image.open('media/watermark.jpeg')
        serializer.validated_data['photo'] = base_image.paste(watermark, (0, 0))
        try:
            base_image.save(f'media/{serializer.validated_data["email"]}.jpg')
        except:
            base_image.save(f'media/{serializer.validated_data["email"]}.png')
            os.remove(f'media/{serializer.validated_data["email"]}.jpg')

        serializer.save()

        object = User.objects.get(email=f'{serializer.validated_data["email"]}')
        object.photo = f'{serializer.validated_data["email"]}.jpg'
        object.save()


        return Response(
            {
                'token': serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)

class MatchView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        target = User.objects.filter(pk=pk)
        serializer = UserSerializer#(request.user)
        like_owner = request.user
        # print(serializer.data)

        # Ищем лайк, который создала мишень, целью которого был хозяин текущего лайка
        try:
            like = Like.objects.get(owner=pk, target=like_owner.pk)
            # Лайк нашелся, значит у нас match!
            # Собираем информацию для рассылки обоим участникам
            u = User.objects.get(pk=pk)
            mail = u.email
            user_username = u.username

            second_username = like_owner.username
            second_mail = like_owner.email
            th = Thread(target=mailing_func, args=(user_username, mail, second_username, second_mail,))
            th.start()
            return Response({'answer': f'match! {mail}'})
        except Exception as ex:
            print(ex)
            # Мы не нашли лайк цели в строну like_owner, поэтому создаем лайк адресованный цели
            # И ждем match с его стороны
            like_object = Like()
            like_object.owner = like_owner.pk
            like_object.target = pk
            like_object.save()
            return Response({'answer': 'keep going'})
