# -*- coding: utf-8 -*-
from django.contrib.auth.models import BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, email, nombre, apellido_paterno ,password=None):
        if not usuario:
            raise ValueError('Debes elegir un nombre de usuario')
        user = self.model(usuario=usuario, nombre=nombre, apellido_paterno=apellido_paterno, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, email, nombre, apellido_paterno, password):
        user = self.create_user(usuario, email, nombre, apellido_paterno, password)
        user.administrador = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
