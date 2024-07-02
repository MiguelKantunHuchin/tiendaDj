from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Sale, SaleDetail
from .serializers import ProcesoVentaSerializer2, ReporteVentaSerializer
from applications.producto.models import Product


class VentasViewSet(viewsets.ViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = Sale.objects.all()
        serializer = ReporteVentaSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProcesoVentaSerializer2(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)

        venta = Sale.objects.create(
            date_sale=timezone.now(),
            amount=0,
            count=0,
            type_invoce=serializer.validated_data["type_invoce"],
            type_payment=serializer.validated_data["type_payment"],
            adreese_send=serializer.validated_data["adreese_send"],
            user=self.request.user,
        )

        # * Se recuperan los productos de la venta
        productos = Product.objects.filter(
            id__in=serializer.validated_data["productos"]
        )

        amount = 0
        count = 0

        cantidades = serializer.validated_data["cantidades"]

        ventas_detalle = []
        for producto, cantidad in zip(productos, cantidades):
            venta_detalle = SaleDetail(
                sale=venta,
                product=producto,
                count=cantidad,
                price_purchase=producto.price_purchase,
                price_sale=producto.price_sale,
            )
            count = count + cantidad
            amount = amount + producto.price_sale * cantidad
            ventas_detalle.append(venta_detalle)

        venta.amount = amount
        venta.count = count
        venta.save()

        SaleDetail.objects.bulk_create(ventas_detalle)
        return Response({"msg": "Venta exitosa"})

    def retrieve(self, request, pk=None):
        venta = get_object_or_404(Sale.objects.all(), pk=pk)
        serializer = ReporteVentaSerializer(venta)
        return Response(serializer.data)
