from django.test import TransactionTestCase
from django.urls import reverse
from biblio.models import Roles, Usuarios, Clientes # Asegúrate de que estos modelos existan y tengan managed=False en biblio/models.py
from django.db import connection, transaction
import warnings

# Ignorar warnings que suelen aparecer con la manipulación manual del esquema
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Lista de modelos que tienen managed=False y deben ser creados para el test
MODELS_TO_MANAGE = [Roles, Usuarios, Clientes]

class AutenticacionClienteTest(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # 1. Forzar managed=True e INTENTO MANUAL DE CREAR LAS TABLAS
        for Model in MODELS_TO_MANAGE:
            # Asegura que Django sepa que debe manejarlo en la prueba
            Model._meta.managed = True
            
            # Crea la tabla en la BD de prueba usando el Schema Editor
            with connection.schema_editor() as schema_editor:
                # Comprueba si la tabla ya existe para evitar errores
                if not Model._meta.db_table in connection.introspection.table_names():
                    schema_editor.create_model(Model)

        # 2. Ahora que las tablas existen, podemos crear los datos
        cls.setUpTestData() 
    
    @classmethod
    def tearDownClass(cls):
        # 1. Eliminar las tablas que creamos manualmente
        for Model in reversed(MODELS_TO_MANAGE): # Eliminar en orden inverso (por dependencias)
            with connection.schema_editor() as schema_editor:
                schema_editor.delete_model(Model)
            
            # 2. Restaurar managed=False
            Model._meta.managed = False
            
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        # Crear Roles
        cls.rol_cliente, _ = Roles.objects.get_or_create(nombre="cliente")
        cls.rol_empleado, _ = Roles.objects.get_or_create(nombre="empleado")
        
        # Creación de Usuario/Cliente de prueba
        # Nota: Django necesita un email para crear un superuser, usa create_user para un usuario normal.
        cls.usuario = Usuarios.objects.create_user(
            username='testuser', 
            password='testpassword123',
            is_active=True
        )
        cls.cliente = Clientes.objects.create(
            usuario=cls.usuario,
            rol=cls.rol_cliente,
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@test.com",
            telefono="12345678"
        )
        cls.login_data = {'username': 'testuser', 'password': 'testpassword123'}

    # ------------------ TESTS DE AUTENTICACIÓN (LOS MÁS PROBABLES A FUNCIONAR) ------------------

    def test_01_vista_login_carga_correctamente(self):
        """Verifica que la página de login carga y usa la plantilla correcta."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publico/login.html')

    def test_02_login_cliente_exitoso(self):
        """Verifica que un cliente puede iniciar sesión correctamente."""
        response = self.client.post(reverse('login'), self.login_data, follow=True)
        # Verifica que la redirección fue exitosa y llegó a la página de inicio (código 200)
        self.assertEqual(response.status_code, 200) 
        # Si usas messages en Django, descomenta:
        # self.assertContains(response, 'Sesión iniciada con éxito') 
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_03_login_fallido_credenciales_incorrectas(self):
        """Verifica que el login falla con credenciales incorrectas."""
        data_erronea = {'username': 'testuser', 'password': 'password_incorrecta'}
        response = self.client.post(reverse('login'), data_erronea, follow=True)
        
        # Debe fallar y el usuario NO debe estar autenticado
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        # Verifica que se mantiene en la plantilla de login o usa un mensaje de error
        self.assertTemplateUsed(response, 'publico/login.html') 
        # self.assertContains(response, 'Credenciales inválidas') # Ajustar al mensaje real

    def test_04_logout_exitoso(self):
        """Verifica que el usuario puede cerrar sesión correctamente."""
        # 1. Iniciar sesión primero
        self.client.post(reverse('login'), self.login_data)
        
        # 2. Cerrar sesión
        response = self.client.get(reverse('logout'), follow=True)
        
        self.assertEqual(response.status_code, 200)
        # Verifica que se haya redirigido al home o al login después del logout
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        # self.assertContains(response, 'Sesión cerrada con éxito') # Ajustar al mensaje real
        
    def test_05_vista_registro_carga_correctamente(self):
        """Verifica que la página de registro carga y usa la plantilla correcta."""
        response = self.client.get(reverse('registro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'publico/registro.html')
    