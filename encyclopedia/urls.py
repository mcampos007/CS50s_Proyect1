from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),                        # Vista principal
    path("wiki/<str:title>/", views.title, name="title"),       # Visualización del página
    path("search/", views.search, name="search"),               # Ruta de búsqueda
    path("new/", views.new_page, name="new_page"),              # Ruta hacia Nueva página
    path("wiki/<str:title>/edit/", views.edit_page, name="edit_page"),    # Nueva ruta para editar
    path("random/", views.random_page, name="random_page"),  # Nueva ruta
    # otras rutas

]
