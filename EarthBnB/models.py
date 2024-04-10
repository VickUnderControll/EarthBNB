from django.db import models

class Propiedad(models.Model):
    direccion = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    habitaciones = models.IntegerField(null=True)
    banos = models.IntegerField(null=True)
    metros_cuadrados = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

class FotosPropiedad(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    ruta_foto = models.CharField(max_length=255)

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    contrasena = models.CharField(max_length=255)
