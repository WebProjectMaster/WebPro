from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Создаёт токены для существующих пользователей'
    def handle (self, *args, **options):
        for user in User.objects.all():
            Token.objects.get_or_create(user=user)
            self.stdout.write(self.style.SUCCESS('Создан токен для пользователя %s' % user))
