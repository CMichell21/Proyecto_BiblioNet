from django.db import models

class LoanRules(models.Model):
    plazo_dias = models.PositiveIntegerField(default=7)
    max_prestamos_por_cliente = models.PositiveIntegerField(default=3)
    mora_diaria = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Reglas(plazo={self.plazo_dias}, max={self.max_prestamos_por_cliente}, mora={self.mora_diaria})"
