from django.urls import re_path, include, path

from .views import RegistrationAPIView, TestView, MatchView
from .views import LoginAPIView

urlpatterns = [
    path('test/', TestView.as_view()),
    path('clients/create/', RegistrationAPIView.as_view()),
    path('clients/auth/', LoginAPIView.as_view()),
    path('clients/<int:pk>/match/', MatchView.as_view()),
]