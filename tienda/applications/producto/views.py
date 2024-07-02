from django.shortcuts import render

from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)


from .models import Product
from .serializers import ProductSerializer


# Create your views here.


class ListProductByUser(ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        print("***********")
        usuario = self.request.user
        return Product.objects.productos_por_user(usuario)


class ListProductSotck(ListAPIView):
    serializer_class = ProductSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser]

    def get_queryset(self):

        return Product.objects.productos_con_stok()


# * Parámetros por url en rest_framework
class ListProductGender(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        genero = self.kwargs["genero"]
        return Product.objects.productos_por_genero(genero)


class FiltrarProductos(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        varon = self.request.query_params.get("man", None)
        mujer = self.request.query_params.get("woman", None)
        nombre = self.request.query_params.get("name", None)
        print(varon)
        print(mujer)
        print(nombre)

        return Product.objects.filtrar_productos(man=varon, woman=mujer, name=nombre)
