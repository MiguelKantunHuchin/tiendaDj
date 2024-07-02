from django.urls import path
from . import views

app_name = "producto_app"

urlpatterns = [
    path("api/produc/by-user", views.ListProductByUser.as_view(), name="product-user"),
    path("api/produc/by-stock", views.ListProductSotck.as_view(), name="product-stock"),
    path(
        "api/produc/by-gender/<genero>",
        views.ListProductGender.as_view(),
        name="product-gender",
    ),
    path(
        "api/produc/filtrar/",
        views.FiltrarProductos.as_view(),
        name="product-filtrar",
    ),
]
