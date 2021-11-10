from django.contrib import admin
from django.urls import path, include

from .views import TestsView, TestsEditView, QEditView, QView, QDelView, TestDelView, TestsClientsView, StudyView, \
    StudentAnswersView

urlpatterns = [

    path('tests/', TestsView.as_view()),
    path('q/', QView.as_view()),
    path('tests/<int:id>/', TestsEditView.as_view()),
    path('q/<int:id>/', QEditView.as_view()),
    path('tests/<int:id>/delete/', TestDelView.as_view()),
    path('q/<int:id>/delete/', QDelView.as_view()),
    path('client/list/', TestsClientsView.as_view()),
    path('client/study/<int:id>/', StudyView.as_view()),
    path('view/user=<str:user_id>test=<int:test_id>/', StudentAnswersView.as_view()),

]
