from django.shortcuts import render
from django.http import JsonResponse
from scraping.scraping import almacenar_bd
from . import indice


def index(request):
    # Obtener parámetros de la solicitud
    min_precio = request.GET.get('min_precio', None)
    max_precio = request.GET.get('max_precio', None)
    orden = request.GET.get('orden', None)
    stock = request.GET.get('stock', '')

    # Convertir min_precio y max_precio a float si son válidos
    if min_precio:
        try:
            min_precio = float(min_precio)
        except ValueError:
            min_precio = None
    if max_precio:
        try:
            max_precio = float(max_precio)
        except ValueError:
            max_precio = None

    # Obtener todos los vinilos filtrados por precio (sin stock filtrado aún)
    vinilos = indice.obtener_vinilos_por_precio(min_precio, max_precio)

    # Filtrar por stock si se especifica 'disponible' o 'no_disponible'
    if stock == 'disponible':
        vinilos = [vinilo for vinilo in vinilos if vinilo.get('stock', '').strip() != 'Agotado']
    elif stock == 'no_disponible':
        vinilos = [vinilo for vinilo in vinilos if vinilo.get('stock', '').strip() == 'Agotado']

    # Ordenar los vinilos si se especifica
    if orden == 'asc':
        vinilos = sorted(vinilos, key=lambda x: float(x['precio'].replace('€', '').replace(',', '.')))
    elif orden == 'desc':
        vinilos = sorted(vinilos, key=lambda x: float(x['precio'].replace('€', '').replace(',', '.')), reverse=True)

    # Devolver los resultados filtrados
    return render(request, 'index.html', {
        'vinilos': vinilos,
        'min_precio': min_precio,
        'max_precio': max_precio,
        'orden': orden,
        'stock': stock,
    })


def cargar_bd(request):
    try:
        print("Cargando datos en la base de datos...")  
        almacenar_bd()  
        print("Base de datos cargada correctamente.")  
        return JsonResponse({'status': 'success', 'message': 'Base de datos cargada correctamente.'})
    except Exception as e:
        print(f"Error al cargar la base de datos: {e}")
        return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {e}'})


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
