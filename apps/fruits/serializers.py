from rest_framework import serializers

from .models import Fruit


class FruitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fruit
        fields = ["id", "name", "price", "image", "created_at", "updated_at"]
        read_only_fields = ("id", "created_at", "updated_at")
