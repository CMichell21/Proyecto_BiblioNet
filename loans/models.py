from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.conf import settings
from catalog.models import BookCopy, CopyStatus

class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    dni = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    def __str__(self): return f"{self.full_name} ({self.dni})"

class LoanStatus(models.TextChoices):
    ACTIVO = "ACTIVO", "Activo"
    CERRADO = "CERRADO", "Cerrado"

class Loan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="loans")
    copy = models.ForeignKey(BookCopy, on_delete=models.PROTECT, related_name="loans")
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=LoanStatus.choices, default=LoanStatus.ACTIVO)
    def __str__(self): return f"Prestamo #{self.id} - {self.member} - {self.copy}"
