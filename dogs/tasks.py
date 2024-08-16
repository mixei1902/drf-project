from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from dogs.models import Dog
from services import send_telegram_message
from users.models import User


@shared_task
def send_information_about_like(email):
    """Отправляет сообщение пользователю что его собаке поставили лайк"""
    message = 'Вашей собаке поставили лайк'
    send_mail('Новый лайк!', 'Вашей собаке поставили лайк', EMAIL_HOST_USER, [email])
    user = User.objects.get(email=email)
    if user.tg_chat_id:
        send_telegram_message(user.tg_chat_id, message)



@shared_task()
def send_mail_about_birthday():
    today = timezone.now().today()
    dogs = Dog.objects.filter(owner__isnull=False, date_born=today)
    email_list = []
    message = 'Поздравляем вашу собаку с днём рождения'
    for dog in dogs:
        email_list.append(dog.owner.email)
        if dog.owner.tg_chat_id:
            send_telegram_message(dog.owner.tg_chat_id, message)
    if email_list:
        send_mail('Позздравление!', message, EMAIL_HOST_USER, [email_list])
