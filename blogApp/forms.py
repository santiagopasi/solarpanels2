from .models import Post,Tag,Message,Comentarios
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#creacion de posts
class PostForm(ModelForm):
    #De esta manera hago que no se pueda editar el user que creó el post
    def __init__(self, *args, **kwargs): 
        super(PostForm, self).__init__(*args, **kwargs)                       
        self.fields['creado_por'].disabled = True
    class Meta:
        model = Post
        fields = "__all__"

#mensajes entre users
class MessageForm(ModelForm):
    def __init__(self, *args, **kwargs): 
        super(MessageForm, self).__init__(*args, **kwargs)                       
        self.fields['sender'].disabled = True
    class Meta:
        model = Message
        fields = "__all__"
    

class TagsForm(ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

#me creo un custom registro para agregarle email
class RegistroCustom(UserCreationForm):

    email = forms.EmailField(label="email")
    

    class Meta:
        model=User
        fields=['email','username','password2']
        help_text={k:"" for k in fields}

class UserEditForm(UserCreationForm):
   
    
    email = forms.EmailField(label="email")
    password1=forms.CharField(label="Contraseña",widget=forms.PasswordInput)
    password2=forms.CharField(label="Repetir Contraseña",widget=forms.PasswordInput)

#definen permisos , asociar datos a alguna tabla se crea una class meta
    class Meta:
        model=User
        fields=['email','password1','password2']
        help_text={k:"" for k in fields}

class ComentariosForm(ModelForm):
    class Meta:
        model = Comentarios
        fields = "__all__"
    def __init__(self, *args, **kwargs): 
        super(ComentariosForm, self).__init__(*args, **kwargs)                       
        self.fields['creado_en'].disabled = True
        self.fields['creado_por'].disabled = True