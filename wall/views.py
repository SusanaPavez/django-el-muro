from django.contrib import messages
from django.shortcuts import redirect, render
from core.decorators import login_required
from .models import *
from core.models import *


@login_required
def wall(request):

    context = {
        'mensajes': Mensaje.objects.all(),
        'comentarios': Comentario.objects.all(),

    }
    return render(request, 'wall/wall.html', context)