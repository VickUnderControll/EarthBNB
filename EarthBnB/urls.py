from django.urls import path
from . import views

urlpatterns = [
    path('', views.mi_vista, name='mi_vista'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('registro/', views.registro, name='registro'),
]