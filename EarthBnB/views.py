
from django.shortcuts import get_object_or_404
from .models import CustomUser, Propiedad, FotosPropiedad
from .forms import LoginForm, RegistrationForm, ImageUploadForm, PropiedadForm
from django.contrib.auth import update_session_auth_hash
from .Imgur.imgur_utils import upload_image_to_imgur
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
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
    if (sesion_iniciada == 0):
        return redirect('login')
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
    if (sesion_iniciada == 0):
        return redirect('login')

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
    if (sesion_iniciada == 0):
        return redirect('login')
    propiedad = Propiedad.objects.get(pk=propiedad_id)
    fotos_propiedad = FotosPropiedad.objects.filter(propiedad=propiedad)
    if request.method == 'POST':
        # Procesar el formulario de la propiedad
        form = PropiedadForm(request.POST, instance=propiedad)
        if form.is_valid():
            form.save()
        # Procesar la subida de fotos
        form_fotos = ImageUploadForm(request.POST, request.FILES)
        if form_fotos.is_valid():
            for foto in request.FILES.getlist('fotos'):
                FotosPropiedad.objects.create(propiedad=propiedad, foto=foto)
        return redirect('/propiedad/'+ str(propiedad_id))  # Redirigir a la página deseada después de guardar los cambios
    else:
        # Si no se envió el formulario, crear un nuevo formulario con la instancia de la propiedad
        form = PropiedadForm(instance=propiedad)
        form_fotos = ImageUploadForm()  # Formulario para la subida de fotos

    # Renderizar la plantilla con el formulario
    return render(request, 'editar_propiedad.html', {'propiedad': propiedad, 'fotos_propiedad': fotos_propiedad, 'form': form, 'form_fotos': form_fotos})


def guardar_foto(request, propiedad_id):
    if (sesion_iniciada == 0):
        return redirect('login')
        image_data = request.FILES['fotos'].read()
        image_link = upload_image_to_imgur(image_data)
        if image_link:
            test=FotosPropiedad.objects.create(propiedad_id=propiedad_id, ruta_foto=image_link)
            return JsonResponse({'success': True, 'image_links': image_link, 'idFoto' :test.id})
        else:
            return JsonResponse({'success': False, 'error': 'Error al cargar las fotos'})



def eliminar_foto(request, foto_id):
    if (sesion_iniciada == 0):
        return redirect('login')
    try:
        foto = FotosPropiedad.objects.get(pk=foto_id)
        foto.delete()
        return JsonResponse({'success': True})
    except FotosPropiedad.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'La foto no existe'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def crear_propiedad(request):
    if(sesion_iniciada==0):
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


def eliminar_foto_perfil(request, usuario_id):
    if (sesion_iniciada == 0):
        return redirect('login')
    try:
        usuario = CustomUser.objects.get(pk=usuario_id)
        usuario.foto_perfil = ''
        usuario.save()
        return JsonResponse({'success': True})
    except CustomUser.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def editar_foto_perfil(request, usuario_id):
    if (sesion_iniciada == 0):
        return redirect('login')
    if 'foto' not in request.FILES:
        return JsonResponse({'success': False, 'error': 'No se ha subido ninguna foto'})

    image_data = request.FILES['foto'].read()
    image_link = upload_image_to_imgur(image_data)

    if image_link:
        try:
            usuario = CustomUser.objects.get(id=usuario_id)
            usuario.foto_perfil = image_link
            usuario.save()
            return JsonResponse({'success': True, 'nueva_foto_url': image_link})
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Usuario no encontrado'})
    else:
        return JsonResponse({'success': False, 'error': 'Error al cargar la foto a Imgur'})


def eliminar_propiedad(request, propiedad_id):
    if (sesion_iniciada == 0):
        return redirect('login')
    try:
        propiedad = get_object_or_404(Propiedad, pk=propiedad_id)
        propiedad.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return None


def editar_usuario(request):
    if(sesion_iniciada==0):
        return redirect('login')
    user =  CustomUser.objects.get(id=sesion_iniciada)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Validación de campos obligatorios
        if not nombre or not email:
            return render(request, 'editar_usuario.html',
                          {'usuario': user, 'error': 'Nombre y Email son campos obligatorios.'})

        # Actualizar nombre y email
        user.first_name = nombre
        user.email = email

        # Validar y actualizar la contraseña si se proporcionan las nuevas contraseñas
        if new_password or confirm_password:
            if new_password != confirm_password:
                return render(request, 'editar_usuario.html',
                              {'usuario': user, 'error': 'Las nuevas contraseñas no coinciden.'})

            if not user.password==current_password:
                return render(request, 'editar_usuario.html',
                              {'usuario': user, 'error': 'La contraseña actual es incorrecta.'})

            user.password=new_password

        user.save()

        # Actualizar la sesión para mantener al usuario autenticado si la contraseña ha cambiado
        if new_password:
            update_session_auth_hash(request, user)

        return render(request, 'usuario.html', {'usuario': user, 'success': 'Perfil actualizado con éxito.'})

    return render(request, 'editar_usuario.html', {'usuario': user})