from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from blog.views import *
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index, name='home'),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^articulo/(?P<slug>.*)', post, name="post"),
    url(r'^crear_post/$', crear_post, name="crear_post"),
    url(r'^editar_post/(?P<slug>.*)$', editar_post, name="editar_post"),
    url(r'^borrar-post/$', borrar_post, name="borrar_post"),
    url(r'^categorias/', categorias, name="categorias"),
    url(r'^categoria/(?P<slug>.*)/pagina/(?P<page>.*)/$', por_categoria, name="categoria"),
    url(r'^tag/(?P<name>.*)/pagina/(?P<page>.*)/$', por_tag, name="tag"),
    url(r'^tags/', tags, name="tags"),
    url(r'^autor/(?P<usuario>.*)', perfil, name="perfil"),
    url(r'^articulos/(?P<usuario>.*)/pagina/(?P<page>.*)/$', por_usuario, name="por_usuario"),
    url(r'^contacto/', contacto, name="contacto"),
    url(r'^documentacion/inicio/', dinicio, name="dinicio"),
    url(r'^documentacion/scaffolding/', scaffolding, name="scaffolding"),
    url(r'^documentacion/basecss/', basecss, name="basecss"),
    url(r'^documentacion/components/', components, name="components"),
    url(r'^documentacion/javascript/', javascript, name="javascript"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^loguear-usuario/$', loguear_usuario, name='loguear_usuario'),
    url(r'^salir/$', salir, name='salir'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)