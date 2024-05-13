from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import CustomUser, Propiedad, FotosPropiedad
from .forms import LoginForm, RegistrationForm, ImageUploadForm, PropiedadForm
from .Imgur.imgur_utils import upload_image_to_imgur
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
sesion_iniciada=0


def login_view(request):
    global sesion_iniciada


    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            contrasena = form.cleaned_data['contrasena']
            try:
                user = CustomUser.objects.get(email=email)
                if user.password == contrasena:
                    sesion_iniciada = user.id  # Añadir sesion_iniciada a la sesión
                    source = request.GET.get('source')
                    if(source=='lista'):
                        return redirect('lista')
                    elif(source=='usuario'):
                        return redirect('usuario')
                    else:
                        return redirect('lista')
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
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration_form.html', {'form': form})

def fotos(request):
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

def cerrar_sesion(request):
    global sesion_iniciada
    sesion_iniciada = 0
    return redirect('lista')
def lista_propiedades(request):
    # Obtener parámetros de filtro
    global sesion_iniciada
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    habitaciones = request.GET.get('habitaciones')
    metros_cuadrados_min = request.GET.get('metros_cuadrados_min')
    metros_cuadrados_max = request.GET.get('metros_cuadrados_max')


    # Filtrar propiedades
    propiedades = Propiedad.objects.all()
    if precio_min:
        propiedades = propiedades.filter(precio__gte=precio_min)
    if precio_max:
        propiedades = propiedades.filter(precio__lte=precio_max)
    if habitaciones:
        propiedades = propiedades.filter(habitaciones=habitaciones)
    if metros_cuadrados_min:
        propiedades = propiedades.filter(metros_cuadrados__gte=metros_cuadrados_min)
    if metros_cuadrados_max:
        propiedades = propiedades.filter(metros_cuadrados__lte=metros_cuadrados_max)

    # Obtener parámetro de orden
    ordenar_por = request.GET.get('ordenar_por')
    if ordenar_por:
        if ordenar_por.endswith('_desc'):
            ordenar_por = '-' + ordenar_por[:-5]  # Eliminar '_desc' y agregar '-' para orden descendente
        propiedades = propiedades.order_by(ordenar_por)

    # Convertir las propiedades en propiedades con fotos
    propiedades_con_fotos = []
    for propiedad in propiedades:
        fotos = FotosPropiedad.objects.filter(propiedad_id=propiedad.id)
        propiedades_con_fotos.append({'propiedad': propiedad, 'fotos': fotos})




    return render(request, 'lista_propiedades.html', {'propiedades_con_fotos': propiedades_con_fotos, 'sesion_iniciada': sesion_iniciada})

def usuario(request):
    if(sesion_iniciada==0):
        return redirect('login')
    usuario =  CustomUser.objects.get(id=sesion_iniciada)
    return render(request, 'usuario.html', {'usuario': usuario})


def lista_propiedades_propietario(request):
    propiedades_propietario = Propiedad.objects.filter(propietario_id=sesion_iniciada)
    propiedades_con_fotos = []
    for propiedad in propiedades_propietario:
        fotos = FotosPropiedad.objects.filter(propiedad_id=propiedad.id)
        propiedades_con_fotos.append({'propiedad': propiedad, 'fotos': fotos})

    return render(request, 'lista_usuario.html', {'propiedades': propiedades_con_fotos})

def detalle_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, pk=propiedad_id)
    fotos = FotosPropiedad.objects.filter(propiedad_id=propiedad_id)
    propietario = propiedad.propietario
    usuario_actual = sesion_iniciada
    return render(request, 'detalle_propiedad.html', {'propiedad': propiedad, "usuario_actual_iniciado": usuario_actual, 'fotos': fotos, 'propietario': propietario, 'usuario_actual': request.session.get('user_id')})



def crear_propiedad(request):
    # Verificar si hay una sesión iniciada
    if not request.session.get('sesion_iniciada'):
        # Si no hay sesión iniciada, redirigir al inicio de sesión
        return redirect('login')  # Ajusta el nombre de la URL según tu configuración

    if request.method == 'POST':
        # Si se envió un formulario POST, procesar los datos
        direccion = request.POST.get('direccion')
        tipo = request.POST.get('tipo')
        habitaciones = request.POST.get('habitaciones')
        banos = request.POST.get('banos')
        metros_cuadrados = request.POST.get('metros_cuadrados')
        precio = request.POST.get('precio')

        # Obtener el ID del propietario desde la sesión iniciada
        propietario_id = request.session.get('sesion_iniciada')

        # Crear la propiedad en la base de datos
        propiedad = Propiedad.objects.create(
            direccion=direccion,
            tipo=tipo,
            habitaciones=habitaciones,
            banos=banos,
            metros_cuadrados=metros_cuadrados,
            precio=precio,
            propietario_id=propietario_id
        )

        # Redirigir a la página de detalle de la propiedad creada
        return redirect('detalle_propiedad', propiedad_id=propiedad.id)  # Ajusta el nombre de la URL según tu configuración

    # Si no se envió un formulario POST, renderizar el formulario para crear la propiedad
    form = ImageUploadForm()
    return render(request, 'crear_propiedad.html', {'form': form})

def editar_propiedad(request, propiedad_id):
    # Obtener la propiedad existente si el ID se proporciona
    propiedad = get_object_or_404(Propiedad, id=propiedad_id) if propiedad_id else None

    if request.method == 'POST':
        # Si se envía el formulario, instanciar el formulario con los datos enviados
        form = PropiedadForm(request.POST, instance=propiedad)
        if form.is_valid():
            # Guardar los cambios si el formulario es válido
            form.save()
            return redirect('/propiedad/'+ str(propiedad_id))  # Redirigir a la página deseada después de guardar los cambios
    else:
        # Si no se envió el formulario, crear un nuevo formulario con la instancia de la propiedad
        form = PropiedadForm(instance=propiedad)

    # Renderizar la plantilla con el formulario
    return render(request, 'editar_propiedad.html', {'form': form})


def crear_propiedad(request):
    # Verificar si hay una sesión iniciada
    if not request.session.get('sesion_iniciada'):
        # Si no hay sesión iniciada, redirigir al inicio de sesión
        return redirect('login')  # Ajusta el nombre de la URL según tu configuración

    if request.method == 'POST':
        # Si se envió un formulario POST, procesar los datos
        direccion = request.POST.get('direccion')
        tipo = request.POST.get('tipo')
        habitaciones = request.POST.get('habitaciones')
        banos = request.POST.get('banos')
        metros_cuadrados = request.POST.get('metros_cuadrados')
        precio = request.POST.get('precio')

        # Obtener el ID del propietario desde la sesión iniciada
        propietario_id = request.session.get('sesion_iniciada')

        # Crear la propiedad en la base de datos
        propiedad = Propiedad.objects.create(
            direccion=direccion,
            tipo=tipo,
            habitaciones=habitaciones,
            banos=banos,
            metros_cuadrados=metros_cuadrados,
            precio=precio,
            propietario_id=sesion_iniciada
        )

        # Redirigir a la página de detalle de la propiedad creada
        return redirect('detalle_propiedad', propiedad_id=propiedad.id)  # Ajusta el nombre de la URL según tu configuración

    # Si no se envió un formulario POST, renderizar el formulario para crear la propiedad
    return render(request, 'crea_propiedad.html')