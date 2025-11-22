from django.test import TransactionTestCase
from django.urls import reverse
from biblio.models import Libros
from datetime import datetime
from django.db import connection, transaction
import warnings

# Ignorar el RuntimeWarning sobre la zona horaria
warnings.filterwarnings(
    "ignore",
    message="DateTimeField Libros.fecha_registro received a naive datetime",
    category=RuntimeWarning,
)

class CatalogoTest(TransactionTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # 1. Forzar managed=True para el modelo
        Libros._meta.managed = True
        
        # 2. INTENTO MANUAL DE CREAR LA TABLA
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(Libros)

        # 3. Llama a setUpTestData para crear los objetos
        cls.setUpTestData() 
    
    @classmethod
    def tearDownClass(cls):
        # 1. Eliminar la tabla que creamos manualmente
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(Libros)
            
        # 2. Restaurar managed=False
        Libros._meta.managed = False
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        # Crear libros de prueba con diferentes campos
        Libros.objects.create(
            id=1, isbn="111-AAA", titulo="El Silencio del Bosque", 
            autor="Ana García", categoria="Misterio", stock_total=5, 
            fecha_registro=datetime(2025, 1, 1)
        )
        Libros.objects.create(
            id=2, isbn="222-BBB", titulo="Romance en la Nieve", 
            autor="Pedro López", categoria="Romance", stock_total=0,
            fecha_registro=datetime(2025, 1, 5)
        )
        Libros.objects.create(
            id=3, isbn="333-CCC", titulo="Aventura Galáctica", 
            autor="Ana García", categoria="Ciencia Ficción", stock_total=10,
            fecha_registro=datetime(2025, 1, 10)
        )

    # ESTE TEST DEBE PASAR SI TU VISTA BASE NO TIENE FILTROS APLICADOS
    def test_01_catalogo_carga_y_muestra_todos_los_libros(self):
        """Verifica que la página carga y muestra los 3 libros creados."""
        url = reverse('catalogo')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        # Verifica que se hayan pasado 3 libros al contexto
        self.assertEqual(response.context['total_libros'], 3)
        self.assertContains(response, "El Silencio del Bosque")
        self.assertTemplateUsed(response, 'publico/catalogo.html')