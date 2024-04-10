from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class RegistroForm(forms.Form):
    nombre = forms.CharField(label='Nombre')
    email = forms.EmailField(label='Email')
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput)