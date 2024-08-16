from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(selfself, *args, **kwargs):
        user = User.objects.create(email="vr@vr.ru")
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.set_password("123456")
        user.save()
