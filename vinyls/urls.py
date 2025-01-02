from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('cargar_bd/', views.cargar_bd, name='cargar_bd'),
    path('buscar/', views.buscar_vinilos, name='buscar_vinilos'),
    path('buscar_artista/', views.buscar_por_artista, name='buscar_por_artista'),
    path('tres_discos_caros/', views.tres_discos_caros, name='tres_discos_caros'),
    path('tres_discos_baratos/', views.tres_discos_baratos, name='tres_discos_baratos'),
]
