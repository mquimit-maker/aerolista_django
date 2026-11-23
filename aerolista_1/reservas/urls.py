from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("vuelos/nuevo/", views.registrar_vuelo, name="registrar_vuelo"),   # va ANTES de <codigo>
    path("vuelos/<str:codigo>/", views.vuelo_detalle, name="vuelo"),
    path("vuelos/<str:codigo>/reservar/", views.reservar, name="reservar"),
    path("vuelos/<str:codigo>/modificar/<int:numero>/", views.modificar, name="modificar"),
    path("vuelos/<str:codigo>/eliminar/<int:numero>/", views.eliminar, name="eliminar"),
]
