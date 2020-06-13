from rest_framework import serializers

from .models import Sale


class SaleSerializer(serializers.ModelSerializer):
    fruit_name = serializers.SerializerMethodField()

    def get_fruit_name(self, obj):
        return obj.fruit.name

    class Meta:
        model = Sale
        fields = ["id", "fruit", "fruit_name", "number", "amount", "sold_at"]
        read_only_fields = ("id", "fruit_name")
