
from django.db import models
from django.contrib.auth.models import User


from .tests import validar_texto

class Panels(models.Model):
    panel_title=models.CharField(max_length=4000)
    panel_price=models.FloatField(max_length=200)
    panel_link=models.CharField(max_length=4000)

#mensajes entre users
class Message(models.Model):
     sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender")
     reciever = models.ForeignKey(User, on_delete=models.CASCADE,related_name="reciever")
     msg_content = models.CharField(max_length=400)
     created_at = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    tag = models.CharField(max_length=100,validators=[validar_texto])
     

    def __str__(self):
        return self.tag


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    cuerpo = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    image=models.ImageField(blank=True)
    creado_por = models.ForeignKey(User ,on_delete=models.CASCADE)
    tags=models.ManyToManyField('Tag',blank=True)

    def __str__(self):
        return self.titulo
    class TipoPost(models.TextChoices):
        monocrystalline = 'Monocrystalline'
        polycrystalline='Polycrystalline'
        
    
    tipo_post = models.CharField(choices= TipoPost.choices, max_length=40)

class Comentarios(models.Model):
    comentario = models.TextField(max_length=500)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,related_name='creado_por')
    creado = models.DateTimeField(auto_now_add=True)
    creado_en=models.ForeignKey(Post, on_delete=models.CASCADE,related_name='creado_en')

    def __str__(self):
        return self.comentario