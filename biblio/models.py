from django.db import models


class Roles(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class Permisos(models.Model):
    modulo = models.CharField(max_length=100)
    accion = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permisos'


class Usuarios(models.Model):
    rol = models.ForeignKey(Roles, models.DO_NOTHING)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=150)
    clave = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'


class Bitacora(models.Model):
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, blank=True, null=True)
    accion = models.CharField(max_length=255)
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bitacora'


class Clientes(models.Model):
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, blank=True, null=True)
    dni = models.CharField(unique=True, max_length=20)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientes'


class Libros(models.Model):
    isbn = models.CharField(unique=True, max_length=20)
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    editorial = models.CharField(max_length=150, blank=True, null=True)
    anio_publicacion = models.TextField(blank=True, null=True)  
    stock_total = models.IntegerField(blank=True, null=True)
    portada = models.CharField(max_length=255, blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'libros'


class Ejemplares(models.Model):
    libro = models.ForeignKey(Libros, models.DO_NOTHING)
    codigo_interno = models.CharField(unique=True, max_length=50, blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ejemplares'


class ReglasPrestamo(models.Model):
    plazo_dias = models.IntegerField()
    limite_prestamos = models.IntegerField()
    tarifa_mora_diaria = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reglas_prestamo'


class Prestamos(models.Model):
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING)
    ejemplar = models.ForeignKey(Ejemplares, models.DO_NOTHING)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_devolucion = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prestamos'


class Reservas(models.Model):
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING)
    libro = models.ForeignKey(Libros, models.DO_NOTHING)
    fecha_reserva = models.DateTimeField(blank=True, null=True)
    fecha_vencimiento = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservas'

class CatalogoPublico(models.Model):
    id_libro = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100, null=True, blank=True)
    editorial = models.CharField(max_length=150, null=True, blank=True)
    anio_publicacion = models.IntegerField(null=True, blank=True)  
    portada = models.CharField(max_length=255, null=True, blank=True)
    total_ejemplares = models.IntegerField()
    disponibles = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'catalogo_publico'