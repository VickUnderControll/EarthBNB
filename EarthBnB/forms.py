
from django import forms
from .models import CustomUser,Propiedad
from .models import CustomUser,Propiedad


class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = ['direccion', 'tipo', 'habitaciones', 'banos', 'metros_cuadrados', 'precio']

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser  # Usa el modelo de usuario personalizado
        fields = ['nombre', 'email', 'password']  # Define los campos que deseas en el formulario de registro