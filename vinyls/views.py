from django.shortcuts import render
from django.http import JsonResponse
from scraping.scraping import almacenar_bd
from . import indice


def index(request):
    # Obtener los valores de min_precio, max_precio y orden desde la solicitud GET
    min_precio = request.GET.get('min_precio', None)
    max_precio = request.GET.get('max_precio', None)
    orden = request.GET.get('orden', None)

    # Convertir a números si los valores son proporcionados
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

    # Obtener los vinilos, aplicando el filtro de precios si es necesario
    vinilos = indice.obtener_vinilos_por_precio(min_precio, max_precio)
    
    # Ordenar los vinilos según el parámetro 'orden'
    if orden == 'asc':
        vinilos = sorted(vinilos, key=lambda x: float(x['precio'].replace('€', '').replace(',', '.')))
    elif orden == 'desc':
        vinilos = sorted(vinilos, key=lambda x: float(x['precio'].replace('€', '').replace(',', '.')), reverse=True)

    return render(request, 'index.html', {'vinilos': vinilos, 'min_precio': min_precio, 'max_precio': max_precio, 'orden': orden})


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
