from PIL import Image
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
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
        base_image.save(f'media/{serializer.validated_data["email"]}.jpg')

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