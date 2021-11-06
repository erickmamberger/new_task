import os
from threading import Thread

from PIL import Image
from rest_framework import status, generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import mailing_func, get_dist
from .models import User, Like
from .serializers import LoginSerializer, GiveSerializer, UserSerializer, GeoSerializer
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


class AllUsersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
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


class FilterByGenderView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, gender):
        queryset = User.objects.filter(gender=gender)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

class FilterByNameView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, username):
        queryset = User.objects.filter(username=username)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

class FilterBySurnameView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, usersurname):
        queryset = User.objects.filter(usersurname=usersurname)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class FilterByKmView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, max_km):
        owner_la = request.user.la
        owner_lo = request.user.lo
        print(max_km)
        # Начинаем фильтровать пользователей по расстоянию, сравнивая расстояние до них с
        # макс. допустимым - max_km
        all = User.objects.all()
        queryset = []
        for x in all:
            # Если мы выпали сами себе, то переходим на след. итерац.
            if x.pk == request.user.pk:
                continue
            # Проверяем заполненна ли геопозиция у человека, если нет, то пропускаем его.
            if x.la == 0.1:
                continue
            print(get_dist(owner_la, x.la, owner_lo, x.lo))
            if get_dist(owner_la, x.la, owner_lo, x.lo) < max_km:
                queryset.append(x)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

# VIEW для заполнения значений геопозиции у пользователя
class CreateGeoView(APIView):
    permission_classes = [AllowAny]
    serializer_class = GeoSerializer

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        la = serializer['la'].value
        lo = serializer['lo'].value
        print(la, lo)
        object = User.objects.get(pk=pk)
        object.la = la
        object.lo = lo
        object.save()
        return Response({'success': {'la': f'{la}', 'lo': f'{lo}'}})