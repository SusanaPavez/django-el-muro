from django.db import models
from core.models import *

# Create your models here.

class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')
        

        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "nombre debe tener al menos 2 caracteres de largo";
        if len(postData['last_name']) < 2:
            errors['last_name'] = "nombre debe tener al menos 2 caracteres de largo";
        if not SOLO_LETRAS.match(postData['first_name']):
            errors['solo_letras_first_name'] = "solo letras en nombre"
        if not SOLO_LETRAS.match(postData['last_name']):
            errors['solo_letras_last_name'] = "solo letras en apellido"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido"
        if len(postData['password']) < 8:
            errors['password'] = "contraseña debe tener al menos 8 caracteres";

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales."        
        return errors


class Wall(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    message = models.TextField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.message} {self.created_at} {self.updated_at}"

    def __repr__(self):
        return f"{self.message} {self.created_at} {self.updated_at}"


class MensajeManager(models.Manager):
    def validador_mensaje(self, postData):
        errors = {}
        if len(postData['mensaje']) < 2:
            errors['mensaje'] = "El mensaje debe tener al menos 2 caracteres de largo";
        return errors

class Mensaje(models.Model):
    mensaje = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="mensaje_id", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = MensajeManager()

    def __str__(self):
        return f"{self.mensaje}"

    def __repr__(self):
        return f"{self.mensaje}"


class ComentarioManager(models.Manager):
    def validador_comentario(self, postData):
        errors = {}
        if len(postData['comentario']) < 2:
            errors['comentario'] = "El comentario debe tener al menos 2 caracteres de largo";
        return errors

class Comentario(models.Model):
    comentario = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="comentarios", on_delete = models.CASCADE)
    mensaje = models.ForeignKey(Mensaje, related_name="comentarios", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = ComentarioManager()
    def __str__(self):
        return f"{self.comentario}"

    def __repr__(self):
        return f"{self.comentario}"