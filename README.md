# VinylExplorer

**VinylExplorer** es una aplicación web que permite explorar vinilos a través de un índice de búsqueda que se genera a partir de los datos extraídos de diferentes fuentes. La aplicación permite buscar vinilos por título o artista, filtrar vinilos por precio y cargar los datos en una base de datos.

## Requisitos

- Python 3.x
- Django
- Whoosh (para el índice de búsqueda)
- Un navegador web moderno

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/paulalunanavarro/VinylExplorer.git
2. **Instalar las dependencias**:  
   Asegúrate de tener `pip` instalado y luego ejecuta:
   ```bash
   pip install -r requirements.txt
  ### Configurar el entorno

Si es necesario, configura las variables de entorno y ajusta el archivo `settings.py` en Django.

### Cargar los datos en la base de datos

La base de datos se carga desde una fuente externa utilizando la función `almacenar_datos`. Puedes cargar los datos ejecutando el siguiente comando:

  ```bash
  python manage.py cargar_bd


