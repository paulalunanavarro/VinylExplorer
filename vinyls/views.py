from django.shortcuts import render
from django.http import HttpResponse
from scraping.scraping import almacenar_bd
from . import indice


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
    

def buscar_vinilos(request):
    consulta = request.GET.get('consulta', '').strip()
    resultados = []

    if consulta:  
        resultados = indice.buscar_vinilos_por_titulo(consulta)
    
    return render(request, 'buscar.html', {
        'consulta': consulta,
        'resultados': resultados,
    })
    

def buscar_por_artista(request):
    consulta = request.GET.get('consulta', '').strip()
    resultados = []

    if consulta:  
        resultados = indice.buscar_vinilos_por_artista(consulta)
    
    return render(request, 'buscar_artista.html', {
        'consulta': consulta,
        'resultados': resultados,
    })
