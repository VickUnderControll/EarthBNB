from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo de email es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    nombre = models.CharField(max_length=255)
    foto_perfil = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # ¡Recuerda usar un algoritmo seguro para almacenar contraseñas!

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    PASSWORD_FIELD = 'password'

    class Meta:
        db_table = 'usuarios'


    def __str__(self):
        return self.email

    def last_login(self):
        # No hacemos nada, ya que no necesitamos este método
        pass

    def is_active(self):
        # No hacemos nada, ya que no necesitamos este método
        pass

    def is_staff(self):
        # No hacemos nada, ya que no necesitamos este método
        pass


class Propiedad(models.Model):
    direccion = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    habitaciones = models.IntegerField()
    banos = models.IntegerField()
    metros_cuadrados = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    propietario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    class Meta:
        db_table = 'propiedades'





    def __str__(self):
        return self.direccion

class FotosPropiedad(models.Model):
        propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
        ruta_foto = models.CharField(max_length=255)

        class Meta:
            db_table = 'fotos_propiedad'