from django.urls import re_path, include, path
from .views import RegistrationAPIView, AllUsersView
from .views import LoginAPIView

urlpatterns = [

    path('clients/create/', RegistrationAPIView.as_view()),
    path('clients/auth/', LoginAPIView.as_view()),
    path('v1/', include('questions.urls')),

]