from django.db import models
from django.contrib.auth.models import User
from django.db.models.expressions import RawSQL

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username

class Pelicula(models.Model):
    id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=200)
    director = models.CharField(max_length=100)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.titulo
    
class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.usuario.username} en {self.pelicula.titulo}"


