from django.urls import re_path, include, path

from .views import RegistrationAPIView, AllUsersView, MatchView, FilterByGenderView, FilterByNameView, \
    FilterBySurnameView, FilterByKmView, CreateGeoView
from .views import LoginAPIView

urlpatterns = [
    path('clients/create/', RegistrationAPIView.as_view()),
    path('clients/auth/', LoginAPIView.as_view()),
    path('clients/<int:pk>/match/', MatchView.as_view()),
    path('list/', AllUsersView.as_view()),
    path('list/gender=<int:gender>/', FilterByGenderView.as_view()),
    path('list/username=<str:username>/', FilterByNameView.as_view()),
    path('list/usersurname=<str:usersurname>/', FilterBySurnameView.as_view()),
    path('list/max_km=<int:max_km>/', FilterByKmView.as_view()),
    path('clients/position/<int:pk>/', CreateGeoView.as_view()),
    path('parser/', include('products.urls'))
]