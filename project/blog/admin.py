#encoding: utf-8
from django.contrib import admin
from .models import *
from tagging.models import Tag
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission, Group
from .forms import CrearusuarioForm, CambiarusuarioForm
from django_summernote.admin import SummernoteModelAdmin

class PermissionInline(admin.StackedInline):
  model = Permission
  extra = 1

class ContentTypeAdmin(admin.ModelAdmin):
  list_display = ('name', 'app_label', 'model',)
  search_fields = ['name', 'permission__name']
  inlines = [PermissionInline,]


class UsuarioAdmin(UserAdmin, SummernoteModelAdmin):
    form = CambiarusuarioForm
    add_form = CrearusuarioForm

    list_display = ('nombre', 'usuario','email',)
    list_filter = ('email','nombre' )
    
    fieldsets = (
                (None, {'fields': ('email', 'password')}),
                ('Perfil', {'fields': ('usuario','nombre','apellido_paterno','apellido_materno', 'profile_picture', 'biografia')}),
                ('Redes sociales', {'fields': ('facebook','twitter','gplus','youtube', 'github')}),
                ('Permisos', {'fields': ('administrador', 'activo', 'user_permissions', "groups")}),
    )
    add_fieldsets = (
                    (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2',)}),
    )
    search_fields = ('nombre',)
    ordering = ('nombre',)
    filter_horizontal = ("groups",'user_permissions',)
    exclude = ['is_superuser']

admin.site.register(Post)
admin.site.register(Categoria)
admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(Categorias)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Permission)
