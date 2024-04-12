from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_propiedades, name='lista'),
    path('propiedad/<int:propiedad_id>/', views.detalle_propiedad, name='detalle_propiedad'),
    path('fotos/', views.mi_vista, name='mi_vista'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.register_view, name='registro'),
]