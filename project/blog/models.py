# -*- coding: utf-8 -*-
from django.db import models
import os
import shutil
from .managers import UsuarioManager
from tagging.fields import TagField
from tagging.models import Tag
from utils import  slughifi, borrar_fotos_anteriores_usuario, ver_si_existe
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, _user_has_perm, PermissionsMixin, _user_has_module_perms
from random import randint
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.conf import settings

class Usuario(AbstractBaseUser, PermissionsMixin):

    def image(self, filename):
        upload_to = "FotosPerfil/%s/%s" % (self.usuario, filename)
        borrar_fotos_anteriores_usuario(self.usuario)
        return upload_to

    def perfil():
        avatar = ('avatar-1.png','avatar-2.png','avatar-3.png','avatar-4.png')
        return "FotosPerfil/default/%s" % (avatar[randint(0,3)])

    usuario = models.CharField(max_length=100, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True, help_text='Activa un usuario para poder usar el sistema')
    administrador = models.BooleanField(default=False, help_text='Que usuarios se les permite entrar al administrador')
    profile_picture = models.ImageField(upload_to=image, null=True, default=perfil, blank=True)
    biografia = models.TextField(blank=True)
    objects = UsuarioManager()
    facebook = models.URLField(null=True,blank=True)
    twitter = models.URLField(null=True, blank=True)
    gplus = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True,blank=True)
    github = models.URLField(null=True,blank=True)

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido_paterno']
    
    def get_full_name(self):
        return self.nombre + ' ' + self.apellido_paterno + ' ' + self.apellido_materno
    def get_short_name(self):
        return self.nombre + ' ' + self.apellido_paterno
    def __unicode__(self):
        return self.usuario
    def has_perm(self, perm, obj=None):
        if self.is_superuser and self.activo:
            return True
        return _user_has_perm(self, perm, obj=obj)
    def has_module_perms(self, app_label):
        if self.is_superuser and self.activo:
            return True
        return _user_has_module_perms(self, app_label)
    @property
    def is_staff(self):
        return self.administrador
    @property
    def is_active(self):
        return self.activo
    def url_entradas(self):
        return reverse('blog.views.por_usuario', args=[str(self.usuario), 1])

######################### SEÑALES DE USUARIO ##################
@receiver(pre_delete, sender=Usuario)
def borrar_carpeta_media_usuario_fotos_antes_de_borrar_usuario(sender, instance, *args, **kwargs):
    try:
        usuario = instance.usuario
        media = settings.MEDIA_ROOT
        media_usuario = os.path.join(media, "FotosPerfil/%s" % usuario)
        shutil.rmtree(media_usuario)
    except: pass


###############################################################
class Post(models.Model):
        def image(self, filename):
            existe = ver_si_existe(filename)
            if not existe:
                upload_to = "FotosPosts/%s" % filename
                return upload_to
            else:
                return existe

        nombre = models.CharField(max_length=100, unique=True)
        slug = models.SlugField(max_length=100, null=True, blank=True)
        contenido = models.TextField()
        tags = TagField()
        categorias = models.ManyToManyField('Categoria', through='Categorias')
        foto_portada = models.ImageField(upload_to=image)
        fecha_creado = models.DateTimeField(auto_now_add=True)
        usuario = models.ForeignKey('Usuario')
        vistas = models.BigIntegerField(null=True, default=0)
        principal = models.BooleanField(default=False)
        def __unicode__(self):
            return self.nombre
        def get_tags(self):
            return Tag.objects.get_for_object(self)
        def save(self, *args, **kwargs):
            self.slug = slughifi(self.nombre)
            self.slug = self.slug.lower()
            super(Post, self).save(*args, **kwargs)
        def get_absolute_url(self):
            return reverse('blog.views.post', args=[str(self.slug)])
        def get_categorias(self):
            return self.categorias.all()
        def editar_post(self):
            return reverse('blog.views.editar_post', args=[str(self.slug)])
            
        class Meta:
			ordering = ["-id"]

@receiver(pre_delete, sender=Post)
def borrar_foto_post(sender, instance, *args, **kwargs):
    try:
        os.unlink(instance.foto_portada.name)
    except Exception as e:
        pass
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)
    def __unicode__(self):
        return self.nombre
    def save(self, *args, **kwargs):
        self.slug = slughifi(self.nombre)
        self.slug = self.slug.lower()
        super(Categoria, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('blog.views.por_categoria', args=[str(self.slug), 1])

class Categorias(models.Model):
    post = models.ForeignKey(Post, related_name='Post')
    categoria = models.ForeignKey(Categoria)
    class Meta:
        verbose_name=u'Categorias relacionadas con un Post'
    def __unicode__(self):
        return self.post.nombre + "|" + self.categoria.nombre

