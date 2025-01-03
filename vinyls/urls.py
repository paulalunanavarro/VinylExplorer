from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('cargar_bd/', views.cargar_bd, name='cargar_bd'),
    path('buscar/', views.buscar_vinilos, name='buscar_vinilos'),
    path('buscar_artista/', views.buscar_por_artista, name='buscar_por_artista'),
    path('tres_discos_caros/', views.tres_discos_caros, name='tres_discos_caros'),
    path('tres_discos_baratos/', views.tres_discos_baratos, name='tres_discos_baratos'),
    path('vinilos_similares/', views.obtener_vinilos_similares, name='vinilos_similares'),
    re_path(r'^vinilos_similares/(?P<titulo>.+)/$', views.mostrar_vinilos_similares_detalle, name='mostrar_similares'),
    


]
