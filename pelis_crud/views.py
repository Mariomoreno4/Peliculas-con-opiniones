from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.db.models import Q
from .models import Pelicula, Comentario, Usuario
from django.contrib.auth.decorators import login_required
from .forms import ComentarioForm, PeliculaForm



@login_required(login_url='/login')
def home(request):
    #consultar las 8 primeras peliculas aleatorias
    peliculas = Pelicula.objects.order_by('?')[:8]
    return render(request, 'home.html', {'peliculas': peliculas})

def registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crea una instancia de Usuario relacionada con el nuevo usuario
            usuario = Usuario(usuario=user)
            usuario.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Iniciar sesión
            user = form.get_user()
            login(request, user)
            # Redirigir a la página deseada después del inicio de sesión
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required(login_url='/login')
def buscar_pelicula(request):
    query = request.GET.get("q")
    
    peliculas = []
    
    if query:
        peliculas=Pelicula.objects.filter(
            Q(director__icontains=query)|
            Q(titulo__icontains=query)
        ).distinct()
        
    
    return render(request, 'search.html', {'peliculas': peliculas})

def cerrar_sesion(request):
    logout(request)
    return redirect('home')

#vista indivual de pelicula
@login_required(login_url='/login')
def pelicula(request, id):
    comentarios = Comentario.objects.filter(pelicula=id)

    pelicula = Pelicula.objects.get(pk=id)
    return render(request, 'pelicula.html', {'pelicula': pelicula, 'comentarios': comentarios})

@login_required(login_url='/login')
def comentar(request, id):
    
    if request.method == 'POST':
        texto = request.POST.get('comentario')
        if texto:
            pelicula = Pelicula.objects.get(pk=id)
            comentario = Comentario(usuario=request.user.usuario, pelicula=pelicula, texto=texto)
            comentario.save()
            return redirect('pelicula', id=id)
    else:
        return redirect('pelicula', id=id)
    
@login_required(login_url='/login')
def eliminar_comentario(request, id):
    comentario = Comentario.objects.get(pk=id)
    
    if request.user.usuario == comentario.usuario:
        comentario.delete()
        
    return redirect('pelicula', id=comentario.pelicula.id)

@login_required(login_url='/login')
def editar_comentario(request, id):
    comentario = get_object_or_404(Comentario, pk=id)


    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('pelicula', id=comentario.pelicula.id)
    else:
        form = ComentarioForm(instance=comentario)

    return render(request, 'partials/editar_comentario.html', {'form': form, 'comentario': comentario})

@login_required(login_url='/login')
def agregar_pelicula(request):
    
    if request.method == 'POST':
        # Procesar el formulario si se ha enviado
        form = PeliculaForm(request.POST)  # Usar un formulario para agregar películas
        if form.is_valid():
            form.instance.usuario = request.user.usuario
            form.save()
            return redirect('home')  # Redirigir a la página de inicio u otra vista
    else:
        # Mostrar el formulario en caso contrario
        form = PeliculaForm()  # Usar un formulario para agregar películas

    return render(request, 'agregar_pelicula.html', {'form': form})
    
@login_required(login_url='/login')
def eliminar_pelicula(request, id):
    
    pelicula = get_object_or_404(Pelicula, pk=id)
    
    if request.user.usuario == pelicula.usuario:
        pelicula.delete()
        
    return redirect('home')

def ver_perfil(request):
    usuario = request.user.usuario
    peliculas = Pelicula.objects.filter(usuario=usuario)
    comentarios = Comentario.objects.filter(usuario=usuario)
    
    return render(request, 'perfil.html', {'usuario': usuario, 'peliculas': peliculas, 'comentarios': comentarios})