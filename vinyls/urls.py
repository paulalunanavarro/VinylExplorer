from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('cargar_bd/', views.cargar_bd, name='cargar_bd'),
]
