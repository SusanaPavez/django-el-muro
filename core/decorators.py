from django.shortcuts import redirect
from django.contrib import messages


def login_required(function):

    def wrapper(request, *args):
        if 'usuario' not in request.session:
            messages.error(request, "Error, tu no estás logueado")
            return redirect('/login')
        resp = function(request, *args)
        return resp

    return wrapper


def admin_requerido(function):

    def wrapper(request, *args):
        #CODIGO DE MI PROPIO DECORADOR
        if 'usuario' in request.session:
            if request.session['usuario']['role'] != 'admin':
                messages.error(
                    request, "No tienes permisos de admin")
                return redirect('/')
        else:
            messages.error(request, "Usuario no ha ingresado")
            return redirect('/login')

        resp = function(request, *args)
        return resp

    return wrapper
