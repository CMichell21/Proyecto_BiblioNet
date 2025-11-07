from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    isbn = models.CharField(max_length=20, unique=True)
    stock_total = models.PositiveIntegerField(default=0)
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)
    def __str__(self): return f"{self.title} ({self.isbn})"

class CopyStatus(models.TextChoices):
    DISPONIBLE = "DISPONIBLE", "Disponible"
    PRESTADO = "PRESTADO", "Prestado"
    RESERVADO = "RESERVADO", "Reservado"
    DANIADO = "DANIADO", "Dañado"

class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="copies")
    code = models.CharField(max_length=50, unique=True)  # INV-0001
    status = models.CharField(max_length=20, choices=CopyStatus.choices, default=CopyStatus.DISPONIBLE)
    location = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self): return f"{self.book.title} ({self.code})"
