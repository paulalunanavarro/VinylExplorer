import os
import sys
import shutil
import warnings 
warnings.filterwarnings("ignore", category=SyntaxWarning)

from datetime import datetime
from whoosh.fields import Schema, TEXT, DATETIME
from whoosh.index import create_in
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
        fecha_indexado=DATETIME(stored=True)
    )
    
    # Crear el índice (elimina si ya existe para un reinicio limpio)
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    ix = create_in("Index", schema=schema)
    writer = ix.writer()

    # Obtener datos de las funciones de scraping
    vinilos_apparell = extraer_vinilos_apparell()
    vinilos_marilians = extraer_vinilos_marilians()
    vinilos = vinilos_apparell + vinilos_marilians

    # Indexar los datos
    for vinilo in vinilos:
        writer.add_document(
            titulo=vinilo["titulo"],
            precio=vinilo["precio"],
            artista=vinilo["artista"],
            descripcion=vinilo["descripcion"],
            imagen=vinilo["imagen"],
            fecha_indexado=datetime.now()
        )
    
    writer.commit()
    print(f"Se han indexado {len(vinilos)} vinilos en el índice.")


# Realiza busquedas en el indice por el titulo del vinilo
def buscar_vinilos(consulta):
    from whoosh.index import open_dir

    ix = open_dir("Index")
    with ix.searcher() as searcher:
        query = QueryParser("titulo", ix.schema).parse(consulta)
        results = searcher.search(query, limit=10)
        for result in results:
            print("Título:", result["titulo"])
            print("Artista:", result["artista"])
            print("Precio:", result["precio"])
            print("Descripción:", result["descripcion"])
            print("Fecha indexado:", result["fecha_indexado"])
            print("-" * 40)


if __name__ == "__main__":
    # almacenar_datos()
    consulta = input("Introduce una consulta para buscar vinilos: ")
    buscar_vinilos(consulta)
