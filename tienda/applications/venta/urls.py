from django.urls import path
from . import views


app_name = "venta_app"

urlpatterns = [
    path(
        "api/venta/reportes/", views.ReporteVentasList.as_view(), name="reporte-venta"
    ),
    path("api/venta/registrar/", views.RegistrarVenta.as_view(), name="crear-venta"),
    path("api/venta/registrar2/", views.RegistrarVenta2.as_view(), name="crear-venta2"),
]
