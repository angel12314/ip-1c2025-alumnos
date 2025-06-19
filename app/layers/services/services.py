# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from app.layers.transport import transport
from app.layers.utilities.translator import fromRequestIntoCard
# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon

def getAllImages():
    pokemons = transport.getAllImages() #trae listado de imagenes crudas
    card_list = []
    for p in pokemons:
        card = fromRequestIntoCard(p) #crea cada imagen en una card (desde translator)
        card_list.append(card)       #se añade a una lista y retorna las card encontradas
    return card_list
    # debe ejecutar los siguientes pasos:
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    # 2) convertir cada img. en una card.
    # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.
    pass
# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():  #Recorremos las cards obtenidas de la API.
        if name.lower() in card.name.lower(): #Comprobamos si el texto "name" está dentro del nombre de la card.
            filtered_cards.append(card) #Si coincide se agrega a la lista filtrada.
        
    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages(): #Recorremos las cards obtenidas.
        for t in card.types:
            if t.lower() == type_filter.lower():
                filtered_cards.append(card) #Si coincide la agregamos a la lista filtrada.

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)
