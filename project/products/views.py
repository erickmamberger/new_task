from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .parser import get_page
from .serializers import StandartSerializer


class StartParsingView(APIView):
    serializer_class = StandartSerializer

    def get(self, request):
        url = 'https://www.citilink.ru/catalog/smartfony/'
        get_page(url)
        return Response({'answer': 'success'})