from rest_framework import serializers

from .models import Fruit


class FruitSerializer(serializers.ModelSerializer):
    image = serializers.FileField(write_only=True, required=False)
    image_name = serializers.SerializerMethodField()

    def get_image_name(self, obj):
        return obj.image.name

    class Meta:
        model = Fruit
        fields = [
            "id",
            "name",
            "price",
            "image",
            "image_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "image_name", "created_at", "updated_at")
