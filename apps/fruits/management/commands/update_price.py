from django.core.management.base import BaseCommand

from fruits.models import Fruit


class Command(BaseCommand):
    def handle(self, *args, **options):
        for fruit in Fruit.objects.all():
            fruit.price *= 2
            fruit.save()
