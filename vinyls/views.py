from django.shortcuts import render
from django.http import HttpResponse
from scraping.scraping import almacenar_bd


def index(request):
    return render(request, 'index.html')


def cargar_bd(request):
    try:
        print("Cargando datos en la base de datos...")  
        almacenar_bd()  
        print("Base de datos cargada correctamente.")  
        return HttpResponse("Base de datos cargada correctamente.")
    except Exception as e:
        print(f"Error al cargar la base de datos: {e}")
        return HttpResponse(f"Ocurrió un error: {e}")
