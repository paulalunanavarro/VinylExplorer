from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('cargar_bd/', views.cargar_bd, name='cargar_bd'),
    path('buscar/', views.buscar_vinilos, name='buscar_vinilos'),
    path('buscar_artista/', views.buscar_por_artista, name='buscar_por_artista'),
]
