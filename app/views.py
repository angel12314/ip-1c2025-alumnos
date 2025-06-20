# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from app.layers.services import services
from django.contrib.auth import authenticate, login #Autenticar inicio de cesion 
from .form import RegistroForm
from app.layers.persistence.repositories import save_user 
from django.contrib.auth.models import User
from django.contrib import messages

def index_page(request):
    return render(request, 'index.html')
def login(request):
    return render(request, 'index.html')
    
def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user=type('User', (), {})()
            user.username=form.cleaned_data["username"]
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.password = form.cleaned_data['password1']

            if User.objects.filter(username=user.username).exists():
                messages.error(request, "El nombre de usuario ya está en uso.")
            elif User.objects.filter(email=user.email).exists():
                messages.error(request, "El email ya está registrado.")
            else:
                save_user(user) 
                messages.success(request, "Usuario creado correctamente. Ahora podés iniciar sesión.")
                return redirect('login')
    else:
        form = RegistroForm()

    return render(request, 'registration/register.html', {'form': form})




# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages()
    favourite_list = []

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images = services.filterByCharacter(name) #Usamos la función de filtro por nombre.
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '')

    if type != '':
        images = services.filterByType(type) # Usamos la función de filtro por tipo.
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

#funcion para iniciar cesion como usuario 
def my_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(home)  # redirecciona a otra pagina 
   
    else:
        print(request, 'Usuario o contraseña incorrectos')
        # Return an 'invalid login' error message.
    return render(request, 'login.html')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    pass

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('home')
