import os
import django
import urllib.request
import time
from bs4 import BeautifulSoup
import sys
from django.db import transaction

# Asegúrate de agregar el directorio principal de tu proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vinyls_project.settings')

django.setup()

from vinyls.models import Vinilo


def extraer_vinilos_apparell():
    vinilos = []
    base_url = "https://apparell.com/collections/boutique?filter.p.m.custom.categoria=Cultura&page="
    
    for num_pagina in range(1, 5):  
        try:
            url = base_url + str(num_pagina)
            response = urllib.request.urlopen(url)
            soup = BeautifulSoup(response, "lxml")
        except Exception as e:
            print(f"Error al procesar la página {num_pagina}: {e}")
            continue

        product_grid = soup.find("div", id="CollectionProductGrid")
        if not product_grid:
            continue
        
        productos = product_grid.find_all("div", class_="product-item")
        
        for producto in productos:
            try:
                titulo_tag = producto.find("div", class_="product-item__title")
                titulo = titulo_tag.text.strip() if titulo_tag else "N/A"
                
                precio_tag = producto.find("span", class_="product-price--original")
                precio = precio_tag.text.strip() if precio_tag else "N/A"
                
                img_tag = producto.find("img")
                imagen = "https:" + img_tag["src"] if img_tag and "src" in img_tag.attrs else "N/A"
                
                link_tag = producto.find("a", class_="product-item__invisible-link")
                link = "https://apparell.com" + link_tag["href"] if link_tag and "href" in link_tag.attrs else "N/A"
                
                detalle_response = urllib.request.urlopen(link)
                detalle_soup = BeautifulSoup(detalle_response, "lxml")
                
                artista_tag = detalle_soup.find("a", class_="collection")
                artista = artista_tag.text.strip() if artista_tag else "N/A"
                
                # Obtener la descripción del div con clase 'description'
                descripcion_tag = detalle_soup.find("div", class_="description")
                descripcion = ""
                if descripcion_tag:
                    # Extraer el texto de todos los <p> dentro del div con clase 'description'
                    for p in descripcion_tag.find_all("p"):
                        descripcion += p.text.strip() + "\n"
                else:
                    descripcion = "Descripción no disponible"
                
                vinilos.append({
                    "titulo": titulo,
                    "precio": precio,
                    "imagen": imagen,
                    "artista": artista,
                    "descripcion": descripcion
                })
                
                time.sleep(1)  # Evita sobrecargar el servidor
            except Exception as e:
                print(f"Error al procesar un producto: {e}")
    return vinilos


def extraer_vinilos_marilians():
    vinilos = []
    base_url = "https://www.marilians.com/8-destacados"
    
    try:
        response = urllib.request.urlopen(base_url)
        soup = BeautifulSoup(response, "lxml")
        
        product_grid = soup.find("div", id="js-product-list")
        if not product_grid:
            print("No se encontró la lista de productos.")
            return vinilos
        
        productos = product_grid.find_all("article", class_="product-miniature")
        for producto in productos: 
            try:
                titulo_tag = producto.find("h2", class_="h3 product-title")
                titulo = titulo_tag.text.strip() if titulo_tag else "N/A"
            
                precio_tag = producto.find("span", class_="price")
                precio = precio_tag.text.strip() if precio_tag else "N/A"

                img_tag = producto.find("img")
                imagen = "https:" + img_tag["src"] if img_tag and "src" in img_tag.attrs else "N/A"

                link_tag = producto.find("a", class_="thumbnail product-thumbnail")
                link = link_tag["href"] if link_tag and "href" in link_tag.attrs else "N/A"
                detalle_response = urllib.request.urlopen(link)
                detalle_soup = BeautifulSoup(detalle_response, "lxml")
                
                # Extraer el artista
                artista_tag = detalle_soup.find("ul", class_="producttags")
                artista = "N/A"
                if artista_tag:
                    artista_list = artista_tag.find_all("a")
                    if artista_list:
                        artista = artista_list[0].text.strip()  # Consideramos el primer artista
                
                # Extraer la descripción
                descripcion_tag = detalle_soup.find("div", id="product-description-5288")
                descripcion = descripcion_tag.text.strip() if descripcion_tag else "Descripción no disponible"

                vinilos.append({
                    "titulo": titulo,
                    "precio": precio,
                    "imagen": imagen,
                    "artista": artista,
                    "descripcion": descripcion
                })
                
                time.sleep(1)  # Evita sobrecargar el servidor
            except Exception as e:
                print(f"Error al procesar un producto: {e}")
    
    except Exception as e:
        print(f"Error al obtener la página: {e}")
    
    return vinilos


def almacenar_bd():
    vinilos_apparell = extraer_vinilos_apparell() 
    vinilos_marilians = extraer_vinilos_marilians()

    with transaction.atomic():
        for vinilo_data in vinilos_apparell and vinilos_marilians:
            Vinilo.objects.update_or_create(
                titulo=vinilo_data["titulo"],
                defaults={
                    "precio": vinilo_data["precio"],
                    "artista": vinilo_data["artista"],
                    "descripcion": vinilo_data["descripcion"],
                    "imagen": vinilo_data["imagen"]
                }
            )

    print(f"Se han almacenado {len(vinilos_apparell) + len(vinilos_marilians)} vinilos en la base de datos.")


if __name__ == "__main__":
    almacenar_bd()
