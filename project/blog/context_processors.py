from .models import *
from .forms import *
from tagging.models import Tag, TaggedItem
import random
import datetime
from django.core.urlresolvers import resolve
from django.http import Http404
from django.utils.safestring import mark_safe
from django.conf import settings

def login(request):
  login = Login()
  usuario_logueado = request.user
  if request.user.is_anonymous():
    usuario_logueado = False  
  return {'login': login,'dominio': settings.SITE_URL, "disqus_url":settings.DISQUS_URL,'usuario_logueado': usuario_logueado}

#Gustavo comentalo
def categorias(request):
  categorias = Categoria.objects.all()
  mitad = len(categorias)/2
  categorias_primeras =  Categoria.objects.all()[0:mitad]
  categorias_segundas =  Categoria.objects.all()[mitad:len(categorias)]
  return {"categorias_blog": Categoria.objects.all(), "categorias_primeras":categorias_primeras, "categorias_segundas":categorias_segundas}

#15 tagas random para el home
def tags_random(request):
  try: 
    tag = random.sample(Tag.objects.all(),15)
  except:
    tag = Tag.objects.all()
  return {"tag_blog": tag}


#Que lo comente gustavo hasta que lo entienda
def tab(request):
  tabs = {
    'inicio': ('home', ),
    'categorias': (
      'categorias',
      'categoria',
    ),
    'blog': (
      # 'post',
      'crear_post',
    ),
    'tags': (
      'tag',
      'tags',
    ),
    'contacto':(
      'contacto'
      )
  }
  try:
    m = resolve(request.path)
    for tab, url_names in tabs.iteritems():
      if m.url_name in url_names:
        return {tab.upper(): mark_safe('class="active"')}
  except Http404: pass

  return {}

#Los posts mas recientes aparecen en el footer
def recent_posts(request):
  try:
    return {"recent_posts": Post.objects.all().order_by('-id')[0:5]}
  except:
    return {}


#Posts mas leidos que apareceran a un costado en el home
def posts_mas_leidos(request):
  try:
    hoy = datetime.datetime.now()
    semana_pasada = datetime.datetime.now() - datetime.timedelta(days=7)
    los_mas_leidos = Post.objects.filter(fecha_creado__lte=hoy, fecha_creado__gte=semana_pasada).order_by('-vistas')[0:5]
    return {"posts_mas_leidos": los_mas_leidos}
  except:
    return {}
  return {}

#Posts tal vez te interese que apareceran en cada articulo
def talvez_te_interese(request):
  path_resolved = resolve(request.path)
  try:
    if path_resolved.url_name == "post" and ('slug' in path_resolved.kwargs):
      post_viendo = Post.objects.get(slug=path_resolved.kwargs['slug'])
      semana_pasada = datetime.datetime.now() - datetime.timedelta(days=30)
      post_tal_vez_te_interese = TaggedItem.objects.get_related(post_viendo, Post.objects.filter(fecha_creado__gte=semana_pasada, fecha_creado__lt=datetime.datetime.now()), 5)
      return {"talvez_te_interese": post_tal_vez_te_interese}
  except Exception as e:
    return {}
  return {}
