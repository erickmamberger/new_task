from django.urls import re_path, include, path

from .views import StartParsingView

urlpatterns = [
    path('start/', StartParsingView.as_view()),
]