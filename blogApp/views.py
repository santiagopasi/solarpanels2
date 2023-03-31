from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm,RegistroCustom,PostForm,TagsForm,MessageForm,ComentariosForm
from .models import Post,Tag,Message,Comentarios,Panels
from django.contrib.auth.models import User
from .scraping import get_panels

#get panels

def list_panels(request):
    Panels.objects.all().delete()
    data = get_panels()
    panel_titles = data['panel_titles']
    panel_prices = data['panel_prices']
    panel_links = data['panel_links']
    i=0
    for title in panel_titles:
        nuevo_panel = Panels(panel_title=title,panel_price=panel_prices[i],panel_link=panel_links[i])
        nuevo_panel.save()
        i+=1  
    panels = Panels.objects.all().order_by('panel_price')      
    return render(request,'panels.html',{'panels':panels})

# mensajes entre users
def mensajes(request):
    form = MessageForm(initial={'sender': request.user})
    if request.method == 'POST':
        form = MessageForm(request.POST,initial={'sender': request.user})
        if form.is_valid():
            form.save()
            inbox=Message.objects.filter(reciever=request.user).order_by('-created_at')
            form=MessageForm(initial={'sender': request.user})
            return render(request, 'inbox.html', {'mensaje':f"Mensaje enviado correctamente",'inbox':inbox,'form':form})
        else:
            form=MessageForm(initial={'sender': request.user})
            inbox=Message.objects.filter(reciever=request.user).order_by('-created_at')
            return render(request, 'inbox.html', {'mensaje':f"Datos Incorrectos","form":form,'inbox':inbox})

    else:
        inbox=Message.objects.filter(reciever=request.user).order_by('-created_at')
        return render(request, 'inbox.html', {'form': form,'inbox':inbox})
    
def crear_tags(request):
    nuevo_tag=TagsForm()
    if request.method == 'POST':
        nuevo_tag=TagsForm(request.POST)
        
        if nuevo_tag.is_valid():
            
            tag, created=Tag.objects.get_or_create(tag=request.POST.get('tag',False))
            
            if created:
                return render(request, 'tags.html', {'mensaje':f"Tag creado correctamente"})
            else:
                return render(request, 'tags.html', {'mensaje':f"Tag ya existe"})
            
        else:
            return render(request, 'tags.html', {'mensaje':f"Datos Incorrectos","nuevo_tag":nuevo_tag})

    return render(request, 'tags.html', {'nuevo_tag':nuevo_tag})

def crear_post(request):
    nuevo_post=PostForm(initial={'creado_por': request.user})
    
    if request.method == 'POST':
        nuevo_post=PostForm(request.POST,request.FILES,initial={'creado_por': request.user})
        if nuevo_post.is_valid():
            nuevo_post.save()
            return render(request, 'posts.html', {'mensaje':f"Post creado correctamente"})
        else:
            return render(request, 'crear_post.html', {'mensaje':f"Datos Incorrectos",'nuevo_post':nuevo_post})
    
    
    return render(request, 'crear_post.html', {'nuevo_post':nuevo_post})

def editar_post(request,id):
    post=Post.objects.get(id=id)
    form=PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return render(request, 'posts.html', {'mensaje':f"Post editado correctamente"})
        else:
            return render(request, 'editar_post.html', {'mensaje':f"Datos Incorrectos","form":form})

    else:
        return render(request, 'editar_post.html', {'form': form})

def posts(request):
    posts = Post.objects.all().order_by('-creado')
    
    return render(request, 'posts.html', {'posts':posts,'nombre_user':request.user.username})

def post_individual(request,id):
    post=Post.objects.get(id=id)
    comentarios = Comentarios.objects.filter(creado_en=post)
    
    crear_comentario=ComentariosForm(initial={'creado_por': request.user,'creado_en':post})
    if request.method == 'POST':
        crear_comentario=ComentariosForm(request.POST,initial={'creado_por': request.user,'creado_en':post})
        crear_comentario.save()
        return render(request, 'post.html', {'mensaje':f"Comentario creado correctamente","post":post,"comentarios":comentarios,"crear_comentario":crear_comentario})
    else:
        return render(request,'post.html',{'post':post,'comentarios':comentarios,'crear_comentario':crear_comentario})


    
def eliminar_post(request,id):
    post = Post.objects.get(id=id)
    post.delete()
    return render(request, 'eliminar_post.html', {'mensaje':f"Post eliminado correctamente"})
def inicio(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroCustom(request.POST)
        
        if form.is_valid() :
            form.save()
            
            return redirect('Login')
        else:
            form=RegistroCustom()
            
            return render(request, 'registro.html', {'mensaje':f"Datos Incorrectos","form":form})
    else:
        form = RegistroCustom()
        
        
        return render(request, 'registro.html', {'form': form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                posts = Post.objects.all()
                return render(request, 'posts.html', {'mensaje':f"Bienvenido {username}",'posts':posts})
            else:
                form=AuthenticationForm()
                return render(request, 'login.html', {'mensaje':f"Datos Incorrectos","form":form})
        else:
            form=AuthenticationForm()
            return render(request, 'login.html', {'mensaje':f"Datos Incorrectos","form":form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def logout_request(request):
    
    logout(request)
    mensaje = "Has cerrado sesión"
    return render(request, 'index.html', {'mensaje':mensaje})

def perfil(request):
    return render(request, 'perfil.html')

#decorador que hace que solo pueda acceder a la vista si esta logueado
@login_required
def editar_perfil(request):

    username=request.user.username
    
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data
            request.user.email = info['email']
            psw = info['password1']
            request.user.set_password(psw)
            request.user.save()

            return render(request, 'perfil.html', {'mensaje':f"Usuario {username} modificado correctamente"})

    else:
        formulario = UserEditForm(initial={'email':request.user.email})
        
        return render(request, 'editar_perfil.html',{'formulario':formulario,'username':username})
    
    

