from django.db import models


class Vinilo(models.Model):
    titulo = models.CharField(max_length=255)  
    precio = models.CharField(max_length=50)  
    artista = models.CharField(max_length=255)  
    descripcion = models.TextField()    
    imagen = models.URLField()  

    def __str__(self):
        return f"{self.titulo} - {self.artista}"
