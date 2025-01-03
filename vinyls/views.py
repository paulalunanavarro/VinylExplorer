from django.shortcuts import render
from django.http import JsonResponse
from scraping.scraping import almacenar_bd
from . import indice
from . import recomendaciones
import os
import django
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vinyls_project.settings')
django.setup()

from vinyls.models import Vinilo



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


def tres_discos_caros(request):
    consulta = request.GET.get('consulta', '').strip()
    resultados = []

    if consulta:  
        resultados = indice.obtener_tres_discos_caros(consulta)
    
    return render(request, 'tres_discos_caros.html', {
        'consulta': consulta,
        'resultados': resultados,
    })
    
    
def tres_discos_baratos(request):
    consulta = request.GET.get('consulta', '').strip()
    resultados = []

    if consulta:  
        resultados = indice.obtener_tres_discos_baratos(consulta)
    
    return render(request, 'tres_discos_baratos.html', {
        'consulta': consulta,
        'resultados': resultados,
    })


def obtener_vinilos_similares(request):
    # Obtener el título desde el parámetro 'titulo' en el request
    titulo = request.GET.get('titulo')  # Usamos GET para obtener el parámetro
    
    if not titulo:
        # Si no se proporciona el título, devolvemos un error
        return JsonResponse({'error': 'Se debe proporcionar un título de vinilo.'}, status=400)

    try:
        # Buscar el vinilo por título en la base de datos
        vinilo = Vinilo.objects.get(titulo__iexact=titulo)  # Usamos 'iexact' para una comparación insensible a mayúsculas/minúsculas
        
        # Obtener vinilos recomendados utilizando el ID del vinilo encontrado
        vinilos_recomendados = recomendaciones.recomendar_vinilos_basados_en_caracteristicas(vinilo.id)
        
        # Prepara los datos para devolver
        vinilos_similares = []
        for vinilo_recomendado in vinilos_recomendados:
            vinilos_similares.append({
                'titulo': vinilo_recomendado['titulo'],
                'artista': vinilo_recomendado['artista'],
                'precio': vinilo_recomendado['precio'],
                'imagen': vinilo_recomendado['imagen'],
                'enlace': vinilo_recomendado['enlace'],
            })
        
        # Retornar los vinilos similares en formato JSON
        return JsonResponse({'vinilos_similares': vinilos_similares})
    
    except Vinilo.DoesNotExist:
        # Si no se encuentra el vinilo con ese título, devolvemos un error
        return JsonResponse({'error': 'Vinilo no encontrado con el título proporcionado.'}, status=404)
    

from urllib.parse import unquote

def mostrar_vinilos_similares_detalle(request, titulo):
    # Decodificar el título si es necesario
    titulo_decodificado = unquote(titulo)
    
    try:
        vinilo = Vinilo.objects.get(titulo__iexact=titulo_decodificado)
        
        # Obtener vinilos recomendados utilizando el ID del vinilo encontrado
        vinilos_recomendados = recomendaciones.recomendar_vinilos_basados_en_caracteristicas(vinilo.id)
        
        # Prepara los datos para pasar a la plantilla
        vinilos_similares = []
        for vinilo_recomendado in vinilos_recomendados:
            vinilos_similares.append({
                'titulo': vinilo_recomendado['titulo'],
                'artista': vinilo_recomendado['artista'],
                'precio': vinilo_recomendado['precio'],
                'imagen': vinilo_recomendado['imagen'],
                'enlace': vinilo_recomendado['enlace'],
            })
        
        # Renderizar la plantilla con los vinilos similares
        return render(request, 'vinilos_similares.html', {
            'vinilos_similares': vinilos_similares,
            'titulo_vinilo': vinilo.titulo
        })
    
    except Vinilo.DoesNotExist:
        return render(request, 'error.html', {'mensaje': 'Vinilo no encontrado.'})

