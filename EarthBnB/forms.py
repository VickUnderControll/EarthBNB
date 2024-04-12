
from django import forms
from .models import CustomUser  # Importa el modelo de usuario personalizado

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser  # Usa el modelo de usuario personalizado
        fields = ['nombre', 'email', 'password']  # Define los campos que deseas en el formulario de registro