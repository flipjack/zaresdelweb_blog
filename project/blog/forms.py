#encoding: utf-8
from django_summernote.widgets import SummernoteWidget
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
Usuario = get_user_model()
from django import forms
from tagging.forms import TagField
from .models import Categoria

class CrearPost(forms.Form):
    nombre = forms.CharField(error_messages={'required': 'Por favor dale un nombre al post', "min_length": "El post debe tener minimo 6 letras"},min_length=6,required=True, widget=forms.TextInput(attrs={"placeholder": "Nombre del Post", "class": "search-input span5"}))
    contenido = forms.CharField(widget=SummernoteWidget(attrs={"class": "span11"}), required=True ,error_messages={'required': 'Escribe algo en el post'})
    foto_portada = forms.ImageField(required=True, error_messages={'required': 'Por favor dale una portada al post'})
    tags = TagField(widget=forms.TextInput(attrs={"placeholder": "Separados por una coma", "class": "search-input span6", "name":"tags", "id":"form-field-tags"}), required=True, error_messages={'required': 'Al menos un Tag'})
    categorias = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={"data-placeholder": "Categorias para el post", "class": "width-80 chosen-select tag-input-style"}), queryset=Categoria.objects.all(), required=True, error_messages={'required': 'Al menos una categoria'})
    principal = forms.BooleanField(initial=True, required=False)


class EditarPost(forms.Form):
    nombre = forms.CharField(error_messages={'required': 'Por favor dale un nombre al post', "min_length": "El post debe tener minimo 6 letras"},min_length=6,required=True, widget=forms.TextInput(attrs={"placeholder": "Nombre del Post", "class": "search-input span5"}))
    contenido = forms.CharField(widget=SummernoteWidget(attrs={"class": "span11"}), required=True ,error_messages={'required': 'Escribe algo en el post'})
    foto_portada = forms.ImageField(required=False, error_messages={'required': 'Por favor dale una portada al post'})
    tags = TagField(widget=forms.TextInput(attrs={"placeholder": "Separados por una coma", "class": "search-input span6", "name":"tags", "id":"form-field-tags"}), required=True, error_messages={'required': 'Al menos un Tag'})
    categorias = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={"data-placeholder": "Categorias para el post", "class": "width-80 chosen-select tag-input-style"}), queryset=Categoria.objects.all(), required=True, error_messages={'required': 'Al menos una categoria'})
    principal = forms.BooleanField(initial=True, required=False)



class CrearusuarioForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Verifica contraseña", widget=forms.PasswordInput) 
    class Meta:
        model = Usuario
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2
    def save(self, commit=True):
        user = super(CrearusuarioForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CambiarusuarioForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="<a href='password/'>Cambiar contraseña</a>")
    class Meta:
        model = Usuario
    def clean_password(self):
        return self.initial['password']

class Login(forms.Form):
    usuario = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Usuario o email', 'type':'text', 'class':'span2'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder':'Password','type':'password', 'class':'span2'}))

class Contacto(forms.Form):
    nombre = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Tu nombre', 'type':'text', 'class':'span12 search-input'}))
    email = forms.EmailField(required=True,  widget=forms.TextInput(attrs={'class':'span12 search-input', 'placeholder':'Ingresa tu email'})) 
    mensaje = forms.CharField(label='Escriba aqui su mensaje',required=True, widget=forms.Textarea(attrs={'class':'span12', 'placeholder':'Escribenos aqui', 'cols':'5', 'rows':'6'}))

   
