# capa DAO de acceso/persistencia de datos.

from sqlite3 import IntegrityError
from app.models import Favourite
from django.contrib.auth.models import User


def save_user(user):
    try:
        create_user=User.objects.create_user(
                    username=user.username,
                    email=user.email,
                    password=user.password,
                    first_name=user.first_name,
                    last_name=user.last_name
                )
        return create_user
    except IntegrityError as e:
        print(f"Error de integridad al guardar el usuario: {e}")
        return None
    except KeyError as e:
        print(f"Error de datos al guardar el usurio: Falta el campo {e}")
        return None
        
        
        
def save_favourite(fav):
    try:
        fav = Favourite.objects.create(
            name=fav.name,  # Nombre del personaje
            id=fav.id,
            types=fav.types,  # tipos
            height=fav.height,  # altura
            weight=fav.weight,  # peso
            image=fav.image,  # Imagen
            user=fav.user  # Usuario autenticado
        )
        return fav
    except IntegrityError as e:
        print(f"Error de integridad al guardar el favorito: {e}")
        return None
    except KeyError as e:
        print(f"Error de datos al guardar el favorito: Falta el campo {e}")
        return None


def get_all_favourites(user):
    return list(Favourite.objects.filter(user=user).values(
        'id', 'name', 'height', 'weight', 'types','base_experience', 'image'
    ))


def delete_favourite(fav_id):
    try:
        favourite = Favourite.objects.get(id=fav_id)
        favourite.delete()
        return True
    except Favourite.DoesNotExist:
        print(f"El favorito con ID {fav_id} no existe o no pertenece al usuario.")
        return False
    except Exception as e:
        print(f"Error al eliminar el favorito: {e}")
        return False
