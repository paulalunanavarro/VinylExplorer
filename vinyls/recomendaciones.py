from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import django
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vinyls_project.settings')
django.setup()

from vinyls.models import Vinilo


# funcion para obtener todos los vinilos de la base de datos
def obtener_vinilos_bd():
    vinilos = Vinilo.objects.all()
    vinilos_data = []
    
    for vinilo in vinilos:
        vinilos_data.append({
            "titulo": vinilo.titulo,
            "descripcion": vinilo.descripcion,
            "artista": vinilo.artista,
        })
    
    return vinilos_data


# funcion que calcula las similitudes entre los vinilos 
def recomendar_vinilos(vinilos):
    descripcion_vinilos = [vinilo["descripcion"] for vinilo in vinilos]
    
    # Convertimos las descripciones en vectores numéricos con TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(descripcion_vinilos)
    
    # Calculamos la similitud de coseno entre los vinilos
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    print("Matriz de similitudes:")
    print(similarity_matrix)
    return similarity_matrix



# función para obtener las recomendacioes 
def obtener_recomendaciones(vinilos, vinilo_id):
    similarity_matrix = recomendar_vinilos(vinilos)
    
    # Obtén las similitudes para el vinilo dado (vinilo_id)
    vinilo_similitudes = similarity_matrix[vinilo_id]
    
    # Ordena los vinilos por la similitud en orden descendente
    recomendaciones = sorted(enumerate(vinilo_similitudes), key=lambda x: x[1], reverse=True)
    
    # Devuelve los 5 vinilos más similares (sin incluir el vinilo original)
    vinilos_recomendados = []
    for i, _ in recomendaciones[1:6]:  # [1:6] para evitar recomendar el mismo vinilo
        vinilos_recomendados.append(vinilos[i])
    
    return vinilos_recomendados


def recomendar_vinilos_basados_en_caracteristicas(vinilo_id):
    # Obtener todos los vinilos desde la base de datos
    vinilos = obtener_vinilos_bd()

    # Obtener recomendaciones basadas en el vinilo seleccionado
    vinilos_recomendados = obtener_recomendaciones(vinilos, vinilo_id)
    
    # Devolver los vinilos recomendados
    return vinilos_recomendados


if __name__ == "__main__":
    # Obtener todos los vinilos desde la base de datos
    vinilos = obtener_vinilos_bd()

    # Mostrar la cantidad de vinilos para saber si se está obteniendo correctamente
    print(f"Total de vinilos: {len(vinilos)}")
    
    # Supongamos que quieres obtener recomendaciones para el primer vinilo (vinilo_id = 0)
    vinilo_id = 0
    
    # Obtener las recomendaciones
    vinilos_recomendados = recomendar_vinilos_basados_en_caracteristicas(vinilo_id)
    
    # Mostrar las recomendaciones
    print("\nVinilos recomendados:")
    vinilo_seleccionado = vinilos[vinilo_id]
    print("el vinilo seleccionado es: ", vinilo_seleccionado['titulo'])
    for vinilo in vinilos_recomendados:
        print(f"Título: {vinilo['titulo']}")

