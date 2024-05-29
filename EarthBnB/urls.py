from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.lista_propiedades, name='lista'),
    path('crea/', views.crear_propiedad, name='crea'),
    path('propiedad/<int:propiedad_id>/', views.detalle_propiedad, name='detalle_propiedad'),
    path('edit/<int:propiedad_id>/', views.editar_propiedad, name='editar_propiedad'),
    path('fotos/', views.fotos, name='fotos'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.register_view, name='registro'),
    path('usuario/', views.usuario, name='usuario_view'),
    path('editar_usuario/', views.editar_usuario, name='editar_usuario'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('crea_propiedad/', views.crear_propiedad, name='crear_propiedad'),
    path('listado/', views.lista_propiedades_propietario, name='listado'),
    path('guardar_fotos/<int:propiedad_id>/', views.guardar_foto, name='guardar_foto'),
    path('editar_foto_perfil/<int:usuario_id>/', views.editar_foto_perfil, name='editar_foto_perfil'),
    path('eliminar_foto/<int:foto_id>/', views.eliminar_foto, name='eliminar_foto'),
    path('eliminar_propiedad/<int:propiedad_id>/', views.eliminar_propiedad, name='eliminar_propiedad'),
    path('eliminar_foto_perfil/<int:usuario_id>/', views.eliminar_foto_perfil, name='eliminar_foto_perfil'),

]