from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .models import User
from .decorators import login_required,admin_requerido




def registro(request):
    if request.method == "POST":

        errors = User.objects.validador_basico(request.POST)
        # print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                # print("DESDE EL FOR: ",key, value)
            
            request.session['register_name'] =  request.POST['name']
            request.session['register_email'] =  request.POST['email']

        else:
            request.session['register_name'] = ""
            request.session['register_email'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = User.objects.create(
                name = request.POST['name'],
                email=request.POST['email'],
                password=password_encryp,
                role=request.POST['role']
            )

            messages.success(request, "El usuario fue agregado con exito")
            

            user = {
                "id" : usuario_nuevo.id,
                "name": usuario_nuevo.name,
                "email": usuario_nuevo.email,
                "role": usuario_nuevo.role
            }

            request.session['usuario'] = user
            return redirect("/dashboard")

        return redirect("/login")
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
                    "name": log_user.name,
                    "email": log_user.email,
                    "role": log_user.role
                }

                request.session['usuario'] = user
                messages.success(request, "Logueado correctamente.")
                return redirect("/")
            else:
                messages.error(request, "Password o Email  incorrectos.")
        else:
            messages.error(request, "Email o password incorrectos.")



        return redirect("/dashboard")
    else:
        return render(request, 'login.html')


@login_required
def dashboard(request):  # quiero que aquí exista opción de cambiar contraseña cuando pueda mejorar el resto :P

    # Esto refleja la pagina tal cual
    if request.method == 'GET':
        context = {}
        return render(request, 'dashboard.html', context)

@login_required
def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    
    return redirect("/login")
