from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Fruit
from .serializers import FruitSerializer


class FruitViewSet(viewsets.ModelViewSet):
    queryset = Fruit.objects
    serializer_class = FruitSerializer
    permission_classes = (IsAuthenticated,)


# from django.http import FileResponse
#
# def download(request, pk):
#     upload_file = get_object_or_404(UploadFile, pk=pk)
#     file = upload_file.file  # ファイル本体
#     return FileResponse(file)
