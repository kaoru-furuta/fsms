from django.db import models


class Fruit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, null=False, unique=True)
    price = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
