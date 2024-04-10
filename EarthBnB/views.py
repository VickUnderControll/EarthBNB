from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistroForm
from .models import Usuario
from django.contrib import messages
from django.shortcuts import render
from .forms import ImageUploadForm
from .Imgur.imgur_utils import upload_image_to_imgur
def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            contrasena = form.cleaned_data['contrasena']
            usuario = authenticate(email=email, password=contrasena)
            if usuario is not None:
                login(request, usuario)
                return redirect('inicio')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'iniciar_sesion.html', {'form': form})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            contrasena = form.cleaned_data['contrasena']
            Usuario.objects.create_user(nombre=nombre, email=email, contrasena=contrasena)
            return redirect('iniciar_sesion')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def mi_vista(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_data = request.FILES['image'].read()
            image_link = upload_image_to_imgur(image_data)
            if image_link:
                return render(request, 'image_uploaded.html', {'image_link': image_link})
            else:
                return render(request, 'error.html')
    else:
        form = ImageUploadForm()
    return render(request, 'mi_template.html', {'form': form})