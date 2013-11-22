#encoding: utf-8
####### DJANGO ################
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.core.mail import send_mail, EmailMultiAlternatives 

######### USUARIO ###########
User = get_user_model()
##### PROYECTO #############
from tagging.models import Tag, TaggedItem
from .models import Post, Categoria, Categorias
from .forms import *
############## PYTHON O TERCEROS ###########
import json

def index(request, page=1):
    if "q" in request.GET:
        posts = buscar_posts(request.GET['q'])
    else:
        posts = Post.objects.filter(principal=True)
    entradas = Paginator(posts,10)
    if 'page' in request.GET:
        try:
            page = int(request.GET['page'])
        except:
            page = request.GET['page']
    try:
        paginator_posts = entradas.page(page)
    except PageNotAnInteger:
        paginator_posts = entradas.page(1)
    except EmptyPage:
        paginator_posts = entradas.page(entradas.num_pages)
    return render(request, "blog.html", locals())

def buscar_posts(query):
    if query.strip() == "":
        return Post.objects.all()
    categorias_search = Categoria.objects.filter(Q(nombre__icontains=query)|Q(slug__icontains=query)).\
    values_list('id', flat=True)
    return Post.objects.filter(Q(nombre__icontains=query) |Q(slug__icontains=query)|\
        Q(usuario__email__icontains=query)|Q(usuario__nombre__icontains=query)|\
        Q(usuario__apellido_materno__icontains=query)|Q(usuario__apellido_paterno__icontains=query)|\
        Q(tags__icontains=query)| Q(categorias__id__in=categorias_search))

def post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        if post.vistas >= 0:
            post.vistas = post.vistas + 1
            post.save()
        elif post.vistas is None:
            post.vistas = 1
            post.save()
    except Exception as e:
        raise Http404
    return render(request, "articulo.html", locals())

def por_categoria(request, slug, page=1):
    categorias = Categoria.objects.filter(slug=slug)
    if not categorias:
        raise Http404
    posts = Post.objects.filter(categorias__in=categorias)
    entradas = Paginator(posts,4)
    try:
        paginator_posts = entradas.page(page)
    except PageNotAnInteger:
        url  = "/categoria/%s/pagina/1" % categorias[0].slug
        return HttpResponseRedirect(url)
    except EmptyPage:
        url  = "/categoria/%s/pagina/1" % categorias[0].slug
        return HttpResponseRedirect(url)
    return render(request, "blog.html", locals())

def categorias(request):
    todas_las_categorias = Categoria.objects.all()
    return render(request, "categorias.html", locals())

@user_passes_test(lambda u: u.is_authenticated(), login_url="/")
def crear_post(request):
    todos_los_tags = Tag.objects.values_list('name', flat=True)
    tags = json.dumps([str(tag) for tag  in todos_los_tags])
    form = CrearPost()
    if request.method == "POST":
        form = CrearPost(request.POST, request.FILES)
        if form.is_valid():
            nuevo_post = Post()
            nuevo_post.disqus_url = request.get_host()
            nuevo_post.nombre = form.cleaned_data['nombre']
            nuevo_post.contenido = form.cleaned_data['contenido']
            nuevo_post.tags = form.cleaned_data['tags'].lower()
            nuevo_post.usuario = request.user
            nuevo_post.foto_portada = form.cleaned_data['foto_portada']
            nuevo_post.save()
            for categoria in form.cleaned_data['categorias']:
               Categorias.objects.create(post=nuevo_post, categoria=categoria)
            nuevo_post.principal = form.cleaned_data['principal']
            nuevo_post.save()
            return HttpResponse(mimetype="application/json", content=json.dumps({"url": nuevo_post.get_absolute_url()}))
        else:
            response = {"errores":form.errors} 
            content = json.dumps(response)
            http_response = HttpResponse(content, mimetype="application/json")
            http_response.status_code= 500
            http_response.content = content
            return http_response
    return render(request, "crear_post.html", locals())

def perfil(request, usuario):
    usuario = get_object_or_404(User, usuario=usuario)
    return render(request, "perfil.html", locals())
def tags(request):
    todos_los_tags = Tag.objects.all()
    return render(request, "tags.html", locals())

def por_tag(request, name, page=1):
    tag = get_object_or_404(Tag, name=name)
    posts = TaggedItem.objects.get_by_model(Post, tag)
    entradas = Paginator(posts,4)
    try:
        paginator_posts = entradas.page(page)
    except PageNotAnInteger:
        url  = "/tag/%s/pagina/1" % tag.name
        return HttpResponseRedirect(url)
    except EmptyPage:
        url  = "/tag/%s/pagina/1" % tag.name
        return HttpResponseRedirect(url)
    return render(request, "blog.html", locals())

def por_usuario(request, usuario, page=1):
    usuario = get_object_or_404(User, usuario=usuario)
    posts = Post.objects.filter(usuario=usuario)
    entradas = Paginator(posts,4)
    try:
        paginator_posts = entradas.page(page)
    except PageNotAnInteger:
        url  = "/articulos/%s/pagina/1" % usuario.usuario
        return HttpResponseRedirect(url)
    except EmptyPage:
        url  = "/articulos/%s/pagina/1" % usuario.usuario
        return HttpResponseRedirect(url)
    return render(request, "blog.html", locals())

def contacto(request):
	if request.method == "POST":
		contacto = Contacto(request.POST)		
		if contacto.is_valid():
			datos = contacto.cleaned_data
			mensaje = datos['mensaje'].lower()
			if mensaje.find("puto") >= 0 or mensaje.find("pendejo") >= 0 or mensaje.find("verga") >= 0 or mensaje.find("idiota") >= 0 or mensaje.find("estupito") >= 0:
				mensaje = "Es una pésima idea insultar a un zar del web :/"
				contacto = Contacto()
				return render(request, "contacto.html", locals()) 
			subject, from_email, to = 'Solicitud de contacto del blog', 'contacto@zaresdelweb.com', 'contacto@zaresdelweb.com'
			text_content = 'Solicitud de contacto del blog'
			html_content = 'Solicitud de contacto del blog: <br>' + str(contacto)
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			mensaje = "Tu mensaje fue enviado gracias :)"
		else:
			mensaje = "Errores en el formulario :/"
	else:
		contacto = Contacto()
	return render(request, "contacto.html", locals())

def dinicio(request):
    return render(request, "documentacion/get_started.html", locals())
def scaffolding(request):
    return render(request, "documentacion/scaffolding.html", locals())
def basecss(request):
    return render(request, "documentacion/base_css.html", locals())
def components(request):
    return render(request, "documentacion/components.html", locals())
def javascript(request):
    return render(request, "documentacion/javascript.html", locals())

def loguear_usuario(request):
    usuario = request.POST['usuario']
    password = request.POST['password']       
    acceso = authenticate(username=str(usuario), password=str(password))
    if acceso is not None:          
        if acceso.is_active:
            login(request, acceso)
            datos = {'recargar':True}
            http_response = HttpResponse(json.dumps(datos),mimetype='application/json') 
            return http_response
        else:
            mensaje="Tu usuario esta desactivado"       
    else:
        mensaje="Usuario o contraseña incorrecta"
    datos = {'mensaje':mensaje}
    http_response = HttpResponse(json.dumps(datos),mimetype='application/json') 
    return http_response

def borrar_post(request):
    Post.objects.filter(id = request.POST['post']).delete()
    datos = {}
    usados = [id_tag.id  for id_tag in Tag.objects.usage_for_model(Post)]
    try:
        Tag.objects.all().exclude(id__in=usados).delete()
    except:
        pass
    http_response = HttpResponse(json.dumps(datos),mimetype='application/json') 
    return http_response

def salir(request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))

@user_passes_test(lambda u: u.is_authenticated(), login_url="/")
def editar_post(request, slug):
    if request.method == "POST":
        slug = slug[0:-1]
        post = get_object_or_404(Post, slug=slug, usuario=request.user)
        form = EditarPost(request.POST, request.FILES)
        tags_a_buscar = post.tags
        if form.is_valid():
            post.nombre = form.cleaned_data['nombre']
            post.contenido = form.cleaned_data['contenido']
            tags_para_el_post= Tag.objects.update_tags(post, form.cleaned_data['tags'].lower())
            post.tags = tags_para_el_post
            usados = [id_tag.id  for id_tag in Tag.objects.usage_for_model(Post)]
            try:
                Tag.objects.all().exclude(id__in=usados).delete()
            except:
                pass
            if form.cleaned_data['foto_portada']:
                post.foto_portada = form.cleaned_data['foto_portada']
            post.save()
            for categoria in form.cleaned_data['categorias']:
               Categorias.objects.get_or_create(post=post, categoria=categoria)
            post.principal = form.cleaned_data['principal']
            post.save()
            return HttpResponse(mimetype="application/json", content=json.dumps({"url": post.get_absolute_url()}))
        else:
            response = {"errores":form.errors} 
            content = json.dumps(response)
            http_response = HttpResponse(content, mimetype="application/json")
            http_response.status_code= 500
            http_response.content = content
            return http_response
    else:
        todos_los_tags = Tag.objects.values_list('name', flat=True)
        tags = json.dumps([str(tag) for tag  in todos_los_tags])
        post_query = get_object_or_404(Post, slug=slug)
        post = model_to_dict(post_query, fields=[], exclude=[])
        form = EditarPost(post)
        foto_anterior = post['foto_portada'].name
        return render(request, "editar_post.html", locals())


