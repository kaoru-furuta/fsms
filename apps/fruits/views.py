from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Fruit
from .serializers import FruitSerializer


class FruitViewSet(viewsets.ModelViewSet):
    queryset = Fruit.objects
    serializer_class = FruitSerializer
    permission_classes = (IsAuthenticated,)
    # parser_classes = [FormParser, MultiPartParser]


def download(request, pk):
    fruit = get_object_or_404(Fruit, pk=pk)
    return FileResponse(fruit.image)
