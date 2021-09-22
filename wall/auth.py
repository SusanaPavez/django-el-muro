from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .models import *
from core.models import *
from core.decorators import login_required


def registro(request):
    if request.method == "POST":

        errors = User.objects.validador_basico(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            
            request.session['register_name'] =  request.POST['name']
            request.session['register_email'] =  request.POST['email']

        else:
            request.session['register_name'] = ""
            request.session['register_email'] = ""

            password_encrypt = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email=request.POST['email'],
                password=password_encrypt,
            )

            messages.success(request, "El usuario fue agregado con exito.")
            

            user = {
                "id" : usuario_nuevo.id,
                "first_name": f"{usuario_nuevo}",
                "email": usuario_nuevo.email,

            }

            request.session['usuario'] = user
            return redirect("/")

        return redirect("/registro")
    else:
        return render(request, 'registro.html')


def login(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

                user = {
                    "id" : log_user.id,
                    "first_name": f"{log_user}",
                    "email": log_user.email,
                }

                request.session['usuario'] = user
                messages.success(request, "Logueado correctamente.")
                return redirect("/")
            else:
                messages.error(request, "Password o Email  incorrectos.")
        else:
            messages.error(request, "Email o password incorrectos.")
        return redirect("/login")
    else:
        return render(request, 'login.html')


@login_required
def mensaje(request):
    print(request.POST)

    errors = Mensaje.objects.validador_mensaje(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/wall")
    else:
        mensaje_creado = request.POST['mensaje']
        user_id_creador = request.session['usuario']['id']

        mensaje = Mensaje.objects.create(
            mensaje=mensaje_creado,
            user=User.objects.get(id=user_id_creador),
        )
        messages.success(request, "Mensaje agregado")

        return redirect(f"/wall")


@login_required
def comentario(request):
    print(request.POST)

    errors = Comentario.objects.validador_comentario(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/wall")
    else:
        comentario_creado = request.POST['comentario']
        id_mensaje = request.POST['id_mensaje_comentario']
        comentario_user_id = request.session['usuario']['id']

        comentario = Comentario.objects.create(
            comentario=comentario_creado,
            user=User.objects.get(id=comentario_user_id),
            mensaje=Mensaje.objects.get(id=id_mensaje),
        )
        messages.success(request, "Comentario agregado")

        return redirect(f"/wall")


@login_required
def borrar(request, id):
    print(request.GET)
    eliminar = Comentario.objects.get(id=id)
    eliminar.delete()

    return redirect("/wall")

@login_required
def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    
    return redirect("/login")
    






