from django.urls import path
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
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('crea_propiedad/', views.crear_propiedad, name='crear_propiedad'),
    path('listado/', views.lista_propiedades_propietario, name='listado'),
]