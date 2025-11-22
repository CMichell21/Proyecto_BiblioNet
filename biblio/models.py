# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class Empleados(models.Model):
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING)
    cargo = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    fecha_ingreso = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empleados'


class HistorialLibros(models.Model):
    libro = models.ForeignKey(Libros, models.DO_NOTHING)
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, blank=True, null=True)
    campo_modificado = models.CharField(max_length=100, blank=True, null=True)
    valor_anterior = models.TextField(blank=True, null=True)
    valor_nuevo = models.TextField(blank=True, null=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historial_libros'


class MovimientosInventario(models.Model):
    TIPO_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
    ]
    libro = models.ForeignKey(Libros, models.DO_NOTHING)
    tipo_movimiento = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movimientos_inventario'


# Correcciones para Prestamos y Reservas
class Prestamos(models.Model):
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING)
    ejemplar = models.ForeignKey(Ejemplares, models.DO_NOTHING)
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_devolucion = models.DateField(blank=True, null=True)
    dias_mora = models.IntegerField(blank=True, null=True)
    multa_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prestamos'


class Reservas(models.Model):
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING)
    libro = models.ForeignKey(Libros, models.DO_NOTHING)
    posicion_cola = models.IntegerField(blank=True, null=True)
    fecha_reserva = models.DateTimeField(blank=True, null=True)
    fecha_vencimiento = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reservas'



