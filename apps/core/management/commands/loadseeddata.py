from django.core.management import BaseCommand, call_command

from core.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command(
            "loaddata", "user", "fruit", "sale",
        )
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()
