from django.core.validators import MinValueValidator
from django.db import models

from fruits.models import Fruit


class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(null=False, validators=[MinValueValidator(1)])
    amount = models.IntegerField(null=False)
    sold_at = models.DateTimeField()

    def __str__(self):
        return str(self.id)
