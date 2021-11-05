import time
import jwt
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .manager import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=255)
    usersurname = models.CharField(max_length=255)
    GENDER_TYPES = (
        (1, 'Женщина'),
        (2, 'Мужчина'),
    )
    gender = models.IntegerField(choices=GENDER_TYPES)

    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
        )
    photo = models.ImageField()

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    # Свойство USERNAME_FIELD сообщает что будем использовать для входа
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ('username',)

    # Управляет объектами этого типа.
    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):

        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(time.mktime(dt.timetuple()))
        }, settings.SECRET_KEY, algorithm='HS256')

        try:
            token = token.encode('utf-8')['b']
        except Exception as ex:
            print(ex)

        return token


class Like(models.Model):
    owner = models.IntegerField(db_index=True)
    target = models.IntegerField(db_index=True)