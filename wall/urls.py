from django.urls import path
from . import views, auth
from django.urls import path
from . import views, auth


urlpatterns = [
    path('', views.wall),
    path('mensaje', auth.mensaje),
    path('mensaje/<int:id>/borrar', auth.borrar),
    path('comentario', auth.comentario),
    path('comentario/<int:id>/borrar', auth.borrar),
]
