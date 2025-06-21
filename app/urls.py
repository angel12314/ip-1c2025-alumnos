from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index_page, name='index-page'),
    path('login/', views.index_page, name='login'),
    path('home/', views.home, name='home'),
    
    path('register/', views.register, name='register'),
    path('buscar/', views.search, name='buscar'),
    
    
    path('subscribe/', views.subscribe, name='subscribe'),
    
    path('filter_by_type/', views.filter_by_type, name='filter_by_type'),

    path('favourites/', views.getAllFavouritesByUser, name='favoritos'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),

    path('exit/', views.exit, name='exit'),
]