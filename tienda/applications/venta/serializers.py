from rest_framework import serializers


from .models import Sale, SaleDetail


class ReporteVentaSerializer(serializers.ModelSerializer):

    productos = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = (
            "id",
            "date_sale",
            "amount",
            "count",
            "type_invoce",
            "cancelado",
            "type_payment",
            "state",
            "adreese_send",
            "anulate",
            "user",
            "productos",
        )

    def get_productos(self, obj):
        query = SaleDetail.objects.productos_por_venta(obj.id)
        productos_serializados = DetalleVentaSerializer(query, many=True).data
        return productos_serializados


class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = ("id", "sale", "product", "count", "price_purchase", "price_sale")


class ProductDetalleSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    count = serializers.IntegerField()


# *Serializador dentro de serializador
class ProcesoVentaSerializer(serializers.Serializer):
    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    adreese_send = serializers.CharField()
    productos = ProductDetalleSerializer(many=True)


class ArrayIntegerSerializer(serializers.ListField):
    child = serializers.IntegerField()


# * Lo mismo pero usando ListField Serializer para optimizar la consulta
class ProcesoVentaSerializer2(serializers.Serializer):
    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    adreese_send = serializers.CharField()
    productos = ArrayIntegerSerializer()
    cantidades = ArrayIntegerSerializer()

    def validate(self, data): 
        if data["type_payment"] != "0":
            raise serializers.ValidationError("Ingrese un tipo de pago correcto")
        return data

    def validated_type_invoce(self, value):
        if value != "0":
            raise serializers.ValidationError("Ingrese un valor correcto")
        return value
