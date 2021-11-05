import time
from django.core.mail import send_mail

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
