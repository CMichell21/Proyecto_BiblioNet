from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings

class Roles(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrador'
    EMPLEADO = 'EMPLEADO', 'Empleado'

class Permission(models.Model):
    code = models.CharField(max_length=100, unique=True)  # ej: 'catalog.create_book'
    name = models.CharField(max_length=150)
    module = models.CharField(max_length=50)              # 'catalog', 'loans', etc.
    action = models.CharField(max_length=50)              # 'create','update','delete','view'
    def __str__(self): return self.code

class Role(models.Model):
    code = models.CharField(max_length=30, unique=True)   # 'ADMIN','EMPLEADO'
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, blank=True, related_name="roles")
    def __str__(self): return self.code

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.EMPLEADO)
    roles = models.ManyToManyField(Role, blank=True, related_name="users")  # múltiples roles opcionales
    def __str__(self): return self.username

class UserAuditLog(models.Model):
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="+")
    target = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="+")
    action = models.CharField(max_length=50)  # create, update, deactivate
    detail = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

# accounts/models.py
from django.conf import settings

class Client(models.Model):
    ESTADOS = (
        ('ACTIVO', 'Activo'),
        ('BLOQUEADO', 'Bloqueado'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cliente')
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='ACTIVO')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email} ({self.dni})"
