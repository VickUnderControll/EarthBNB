from django.urls import path
from . import views

urlpatterns = [
    path('', views.mi_vista, name='mi_vista'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.register_view, name='registro'),
]