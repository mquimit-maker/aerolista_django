from django.urls import include, path

urlpatterns = [
    path("", include("reservas.urls")),   # todas las rutas viven en la app reservas
]
