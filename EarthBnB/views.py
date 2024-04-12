from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import LoginForm, RegistrationForm



from django.contrib import messages
from django.shortcuts import render
from .forms import ImageUploadForm
from .Imgur.imgur_utils import upload_image_to_imgur


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            contrasena = form.cleaned_data['contrasena']

            # Busca el usuario por su correo electrónico en la base de datos
            try:
                user = CustomUser.objects.get(email=email)
                # Verifica si la contraseña proporcionada coincide
                if user.password == contrasena:
                    # Inicia sesión manualmente
                    request.session['user_id'] = user.id
                    messages.success(request, '¡Inicio de sesión exitoso!')
                    return redirect('/')
                else:
                    messages.error(request, 'Credenciales incorrectas. Por favor, inténtalo de nuevo.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'El usuario con este correo electrónico no existe.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el usuario en la base de datos si el formulario es válido
            return redirect('login')  # Redirige al usuario a la página de inicio de sesión
    else:
        form = RegistrationForm()
    return render(request, 'registration_form.html', {'form': form})

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