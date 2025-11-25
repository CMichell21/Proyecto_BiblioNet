from django.test import TransactionTestCase
from django.urls import reverse
# Importa todos los modelos que uses en tus vistas y tests
from biblio.models import Libros, Clientes, Usuarios, Roles 
from django.db import connection
from datetime import datetime
from django.contrib.auth.hashers import make_password 
import warnings

# Ignorar warnings que suelen aparecer con la manipulación manual del esquema
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Lista de modelos que tienen managed=False y deben ser creados para el test
MODELS_TO_MANAGE = [Roles, Usuarios, Clientes, Libros]

class VistasGeneralesTest(TransactionTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # 1. Forzar managed=True e INTENTO MANUAL DE CREAR LAS TABLAS
        with connection.schema_editor() as schema_editor:
            for Model in MODELS_TO_MANAGE:
                # 1. Sobrescribir managed=False a True para la prueba
                Model._meta.managed = True
                
                # 2. Crear la tabla manualmente
                if Model._meta.db_table not in connection.introspection.table_names():
                     schema_editor.create_model(Model)

        # 2. Ahora que las tablas existen, podemos crear los datos de prueba
        cls.setUpTestData() 
    
    @classmethod
    def tearDownClass(cls):
        # 1. Eliminar las tablas que creamos manualmente
        with connection.schema_editor() as schema_editor:
            for Model in reversed(MODELS_TO_MANAGE): 
                schema_editor.delete_model(Model)
            
            # 2. Restaurar managed=False
            Model._meta.managed = False
            
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        # --- CREACIÓN DE ROLES (Necesarios por dependencias de Clientes) ---
        cls.rol_cliente, _ = Roles.objects.get_or_create(nombre="cliente")
        cls.rol_empleado, _ = Roles.objects.get_or_create(nombre="empleado")
        
        # --- CREACIÓN DE LIBROS BASE ---
        Libros.objects.create(
            id=1, isbn="111-AAA", titulo="Libro Disponible", 
            autor="Autor Test", categoria="Ficción", stock_total=5, 
            fecha_registro=datetime(2025, 1, 1)
        )
        
    # -----------------------------------------------------------
    # 🧪 TESTS DE CARGA DE PÁGINAS PÚBLICAS (CORREGIDOS)
    # -----------------------------------------------------------

    def test_02_acerca_de_carga_correctamente(self):
        """Verifica que la vista 'acerca de' carga sin errores."""
        # ⚠️ CORREGIDO: Usando 'acerca_de'
        response = self.client.get(reverse('acerca_de')) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publico/acerca_de.html')