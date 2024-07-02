from rest_framework import viewsets
from rest_framework.response import Response

from .models import Colors, Product
from .serializers import ColorSerializer, ProductSerializer, ProductSerializerViewSet


class ColorViewSet(viewsets.ModelViewSet):
    serializer_class = ColorSerializer
    queryset = Colors.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializerViewSet
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(
            video = "AAAAAAAAAAAAAAAAA"
        )
