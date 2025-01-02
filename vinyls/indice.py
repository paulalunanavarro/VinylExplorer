import os
import sys
import shutil
import warnings
from datetime import datetime
from whoosh.fields import Schema, TEXT, DATETIME
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

# Añadir la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraping.scraping import extraer_vinilos_apparell, extraer_vinilos_marilians


# Define el esquema para los datos de vinilos
def almacenar_datos():
    schema = Schema(
        titulo=TEXT(stored=True),
        precio=TEXT(stored=True),
        artista=TEXT(stored=True),
        descripcion=TEXT(stored=True),
        imagen=TEXT(stored=True),
        stock=TEXT(stored=True),
        enlace=TEXT(stored=True),
        fecha_indexado=DATETIME(stored=True)
    )
    
    # Crear el índice
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    ix = create_in("Index", schema=schema)
    writer = ix.writer()

    vinilos_apparell = extraer_vinilos_apparell()
    vinilos_marilians = extraer_vinilos_marilians()
    vinilos = vinilos_apparell + vinilos_marilians

    for vinilo in vinilos:
        writer.add_document(
            titulo=vinilo["titulo"],
            precio=vinilo["precio"],
            artista=vinilo["artista"],
            descripcion=vinilo["descripcion"],
            imagen=vinilo["imagen"],
            stock=vinilo["stock"],
            enlace=vinilo["enlace"],
            fecha_indexado=datetime.now()
        )
        
    
    writer.commit()
    print(f"Se han indexado {len(vinilos)} vinilos en el índice.")


def buscar_vinilos_por_titulo(consulta):
    ix = open_dir("Index")
    resultados = []  
    
    with ix.searcher() as searcher:
        query = QueryParser("titulo", ix.schema).parse(consulta)
        results = searcher.search(query, limit=10)
        
        for result in results:
            resultados.append({
                "titulo": result["titulo"],
                "artista": result["artista"],
                "precio": result["precio"],
                "descripcion": result["descripcion"],
                "imagen": result["imagen"],
                "stock": result["stock"],
                "enlace": result["enlace"],
                "fecha_indexado": result["fecha_indexado"],
            })
    
    return resultados


def buscar_vinilos_por_artista(consulta):
    ix = open_dir("Index")
    resultados = []  
    
    with ix.searcher() as searcher:
        query = QueryParser("artista", ix.schema).parse(consulta)
        results = searcher.search(query, limit=10)
        
        for result in results:
            resultados.append({
                "titulo": result["titulo"],
                "artista": result["artista"],
                "precio": result["precio"],
                "descripcion": result["descripcion"],
                "imagen": result["imagen"],
                "stock": result["stock"],
                "enlace": result["enlace"],
                "fecha_indexado": result["fecha_indexado"],
            })
    
    return resultados


def obtener_todos_los_vinilos():
    ix = open_dir("Index")
    vinilos = []
    
    with ix.searcher() as searcher:
        results = searcher.all_stored_fields()
        
        for result in results:
            vinilos.append({
                "titulo": result["titulo"],
                "precio": result["precio"],
                "imagen": result["imagen"],
                "enlace": result["enlace"],
            })
    
    return vinilos


def obtener_vinilos_por_precio(min_precio=None, max_precio=None):
    ix = open_dir("Index")
    vinilos = []
    
    with ix.searcher() as searcher:
        # Obtener todos los documentos sin ningún filtro (limit=None)
        results = searcher.all_stored_fields()
        
        for result in results:
            precio = float(result["precio"].replace('€', '').replace(',', '.').
                           strip())
            
            # Filtrar vinilos por precio si se especifican los límites
            if min_precio and precio < min_precio:
                continue
            if max_precio and precio > max_precio:
                continue

            vinilos.append({
                "titulo": result["titulo"],
                "precio": result["precio"],
                "imagen": result["imagen"],
                "enlace": result["enlace"],
                "stock": result["stock"],
            })
    
    return vinilos


def obtener_tres_discos_caros():
    ix = open_dir("Index")
    vinilos = []

    with ix.searcher() as searcher:
        results = searcher.all_stored_fields()  
        for result in results:
            try:
                precio = float(result["precio"].replace('€', '').replace(',', '.').strip())
                vinilos.append({**result, "precio": precio})
            except ValueError:
                continue  

    vinilos_ordenados = sorted(vinilos, key=lambda vinilo: vinilo["precio"], reverse=True)
    return vinilos_ordenados[:3]


def obtener_tres_discos_baratos():
    ix = open_dir("Index")
    vinilos = []

    with ix.searcher() as searcher:
        results = searcher.all_stored_fields()  
        for result in results:
            try:
                precio = float(result["precio"].replace('€', '').replace(',', '.').strip())
                vinilos.append({**result, "precio": precio})
            except ValueError:
                continue  

    vinilos_ordenados = sorted(vinilos, key=lambda vinilo: vinilo["precio"])
    print(f"Vinilos ordenados por precio (de menor a mayor): {vinilos_ordenados[:3]}")  # Verifica los primeros 5
    return vinilos_ordenados[:3]


if __name__ == "__main__":
    almacenar_datos()  # Descomentar si necesitas indexar los datos
    consulta = input("Introduce una consulta para buscar vinilos por título: ")
    resultados = buscar_vinilos_por_titulo(consulta)
