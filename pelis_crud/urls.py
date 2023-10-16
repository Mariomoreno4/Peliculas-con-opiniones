from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro', views.registrar, name='registrar'),
    path('login', views.iniciar_sesion, name='login' ),
    path('buscar', views.buscar_pelicula, name='buscar'),
    path('logout', views.cerrar_sesion, name='logout'),
    path('pelicula/<int:id>', views.pelicula, name='pelicula'),
    path('comentar/<int:id>', views.comentar, name='comentar'),
    path('eliminar/<int:id>', views.eliminar_comentario, name='eliminar_comentario'),
    path('editar/<int:id>', views.editar_comentario, name='editar_comentario'),
    path('agregar', views.agregar_pelicula, name='agregar_pelicula'),
    path('eliminar_pelicula/<int:id>', views.eliminar_pelicula, name='eliminar_pelicula'),
    path('perfil', views.ver_perfil, name='ver_perfil'),
]
