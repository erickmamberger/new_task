import time
from django.core.mail import send_mail
from math import radians, cos, sin, asin, sqrt


# расчет дистанции по гаверсинусу в км.
def get_dist(La1, La2, Lo1, Lo2):
    Lo1 = radians(Lo1)
    Lo2 = radians(Lo2)
    La1 = radians(La1)
    La2 = radians(La2)


    D_Lo = Lo2 - Lo1
    D_La = La2 - La1
    P = sin(D_La / 2) ** 2 + cos(La1) * cos(La2) * sin(D_Lo / 2) ** 2

    Q = 2 * asin(sqrt(P))

    R_km = 6371

    return (Q * R_km)

def mailing_func(name1, mail1, name2, mail2):
    send_mail(
        'Взаимная симпатия!',
        f'Вы понравились {name2}! Почта участника: {mail2}',
        'erickmambergermail@yandex.ru',
        [f'{mail1}'],
        fail_silently=False,
    )
    send_mail(
        'Взаимная симпатия!',
        f'Вы понравились {name1}! Почта участника: {mail1}',
        'erickmambergermail@yandex.ru',
        [f'{mail2}'],
        fail_silently=False,
    )

