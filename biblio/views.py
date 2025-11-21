from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse

from django.contrib import messages

from django.contrib.auth.hashers import make_password, check_password

from django.utils import timezone

from django.db import transaction

from django.views.decorators.csrf import csrf_protect

from django.core.paginator import Paginator

from django.db.models import Q

from datetime import timedelta



# Importar todos los modelos necesarios

try:

    # Intenta importar todos los modelos necesarios. Si Categoria o Estado no existen,

    # la lógica dentro de catalogo manejará la excepción (NameError o ImportError).

    from .models import Usuarios, Roles, Clientes, Libros, Reservas, ReglasPrestamo

    # Estos modelos se importan aquí para evitar errores en las funciones que los usan directamente.

    # Si Categoria y Estado existen, se deben añadir a la lista de importación.

except ImportError:

    # Manejo de la importación si los modelos no están en la ruta esperada.

    from biblio.models import Usuarios, Roles, Clientes, Libros, Reservas, ReglasPrestamo

    # Nota: Si Categoria y Estado son necesarios, deben ser accesibles aquí.



# --- FUNCIONES AUXILIARES ---

def obtener_cliente_logueado(request):
    print(f"\n--- DEBUG SESIÓN EN {request.path} ---")
    print(f"cliente_id en session: {request.session.get('cliente_id')}")

    if "cliente_id" not in request.session:
        print("Resultado: NO HAY ID en la sesión, REDIRIGIENDO.")
        messages.error(request, "Debes iniciar sesión para realizar esta acción.")
        return None, redirect("inicio_sesion_cliente")
   

    try:

        cliente = Clientes.objects.get(id=request.session["cliente_id"])

        return cliente, None

    except Clientes.DoesNotExist:

        messages.error(request, "Perfil de cliente no encontrado. Sesión inválida.")

        # Limpieza de sesión

        if "cliente_id" in request.session:

            del request.session["cliente_id"]

        return None, redirect("inicio_sesion_cliente")





# --- VISTAS PÚBLICAS ---

# ----------------------------------------------------------------------



def inicio(request):

    """Renderiza la página de inicio pública."""

    return render(request, "publico/pagina_inicio.html")



def catalogo(request):

    """Vista del catálogo público (sin sesión requerida)."""

    q = (request.GET.get("q") or "").strip()

    categoria_nombre = (request.GET.get("categoria") or "").strip()

    estado = (request.GET.get("estado") or "").strip()

    orden = (request.GET.get("orden") or "recientes").strip()



    libros_qs = Libros.objects.all()



    # Base: Muestra todos los libros



    # Buscar por título o autor

    if q:

        libros_qs = (

            libros_qs.filter(Q(titulo__icontains=q) |

                             Q(autor__icontains=q)) # Asumiendo que 'autor' es CharField en Libros

        ).distinct()



    # Filtrar por categoría (Asume que categoria tiene un campo 'nombre' o se compara con el CharField de Libros)

    if categoria_nombre:

        libros_qs = libros_qs.filter(categoria__icontains=categoria_nombre) # Asumiendo que 'categoria' es CharField en Libros



    # Filtrar por estado usando stock_total directo

    if estado == "disponible":

        libros_qs = libros_qs.filter(stock_total__gt=0)

    elif estado == "prestado":

        libros_qs = libros_qs.filter(stock_total__lte=0)



    # Orden

    if orden == "titulo_asc":

        libros_qs = libros_qs.order_by("titulo")

    elif orden == "titulo_desc":

        libros_qs = libros_qs.order_by("-titulo")

    elif orden == "autor_asc":

        libros_qs = libros_qs.order_by("autor", "titulo")

    elif orden == "antiguos":

        libros_qs = libros_qs.order_by("anio_publicacion", "titulo")

    else:

        libros_qs = libros_qs.order_by("-fecha_registro", "titulo")



    paginator = Paginator(libros_qs, 9)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

   

    # Intenta obtener categorías y estados, si los modelos están disponibles

    all_categorias = []

    all_estados = []

    try:

        from .models import Categoria, Estado

        all_categorias = Categoria.objects.all()

        all_estados = Estado.objects.all()

    except (ImportError, NameError):

        pass





    ctx = {

        "libros": page_obj.object_list,

        "page_obj": page_obj,

        "total_libros": paginator.count,

        "q": q,

        "categoria": categoria_nombre,

        "estado": estado,

        "orden": orden,

        "all_categorias": all_categorias,

        "all_estados": all_estados,

    }



    return render(request, "publico/catalogo.html", ctx)





def acerca_de(request):

    """Vista 'Acerca de' pública."""

    clientes_activos = Clientes.objects.filter(estado__iexact="activo").count()



    contexto = {

        'clientes_activos': clientes_activos

    }

    return render(request, "publico/acerca_de.html", contexto)





def registro_cliente(request):

    """Registro de nuevos clientes."""

    if request.method == "POST":

        nombre = request.POST.get("nombre","").strip().lower()

        apellido = request.POST.get("apellido","").strip().lower()

        email = request.POST.get("email","").strip().lower()

        password = request.POST.get("password","")

        confirm = request.POST.get("confirm_password","")



        # Validaciones mínimas

        if not all([nombre, apellido, email, password, confirm]):

            messages.error(request, "Completa todos los campos obligatorios.")

            return render(request, "publico/registro_cliente.html", {"form": request.POST.copy()})

       

        if len(password) < 8:

            messages.error(request, "La contraseña debe tener al menos 8 caracteres.")

            return render(request, "publico/registro_cliente.html", {"form": request.POST.copy()})

       

        if password != confirm:

            messages.error(request, "Las contraseñas no coinciden.")

            return render(request, "publico/registro_cliente.html", {"form": request.POST.copy()})

       

        if Usuarios.objects.filter(email=email).exists():

            messages.error(request, "Ya existe una cuenta con ese correo.")

            return render(request, "publico/registro_cliente.html", {"form": request.POST.copy()})



        # Crear usuario cliente

        try:

            with transaction.atomic():

                rol, _ = Roles.objects.get_or_create(nombre="cliente")

               

                usuario = Usuarios.objects.create(

                    rol=rol,

                    nombre=nombre,

                    apellido=apellido,

                    email=email,

                    clave=make_password(password),

                    estado="activo",

                    fecha_creacion=timezone.now()

                )

               

                cliente = Clientes.objects.create(

                    usuario=usuario,

                    dni="", # Campo obligatorio, debe completarse

                    direccion="",

                    telefono="",

                    estado="activo"

                )



            # Sesión

            request.session["cliente_id"] = cliente.id

            request.session["cliente_email"] = usuario.email

            messages.success(request, "¡Cuenta creada con éxito! Ahora puedes iniciar sesión.")

            return redirect("inicio_sesion_cliente")

           

        except Exception as e:

            messages.error(request, f"Error al crear la cuenta: {str(e)}")

            return render(request, "publico/registro_cliente.html", {"form": request.POST.copy()})



    return render(request, "publico/registro_cliente.html")





@csrf_protect

def inicio_sesion_cliente(request):

    """Maneja el inicio de sesión de clientes."""

    ctx = {}

    if request.method == "POST":

        email = request.POST.get("email","").strip().lower()

        password = request.POST.get("password","")



        try:

            user = Usuarios.objects.select_related("rol").get(

                email=email, rol__nombre="cliente", estado="activo"

            )

            cliente = Clientes.objects.get(usuario=user)



        except (Usuarios.DoesNotExist, Clientes.DoesNotExist):

            ctx["error"] = "Usuario o contraseña incorrectos."

            return render(request, "publico/login_cliente.html", ctx)

       

        # Validación de contraseña

        ok = check_password(password, user.clave)



        if not ok:

            ctx["error"] = "Usuario o contraseña incorrectos."

            return render(request, "publico/login_cliente.html", ctx)



        # Inicio de sesión exitoso

        request.session["cliente_id"] = cliente.id

        request.session["cliente_email"] = user.email
        # ⬇️ AGREGA ESTO PARA VER EL PROBLEMA REAL
        print("LOGIN DEBUG → cliente.id:", cliente.id)
        print("LOGIN DEBUG → session cliente_id:", request.session.get("cliente_id"))

        return redirect("pantalla_inicio_cliente")



    return render(request, "publico/login_cliente.html")



# --- VISTAS PRIVADAS DE CLIENTES ---

# ----------------------------------------------------------------------



def pantalla_inicio_cliente(request):

    """Vista de inicio después del login del cliente."""

    cliente, response = obtener_cliente_logueado(request)

    if response:

        return response

   

    context = {

        "cliente": cliente,

        "usuario": cliente.usuario,

    }

    return render(request, "clientes/pantalla_inicio_cliente.html", context)





def catalogo_cliente(request):

    """Vista del catálogo privado para clientes logueados."""

   

    cliente, response = obtener_cliente_logueado(request)

    if response:

        return response

       

    # --- INICIO DE LA LÓGICA DEL CATÁLOGO ---

    q = (request.GET.get("q") or "").strip()

    categoria_id = request.GET.get("categoria")

    orden = request.GET.get("orden", "titulo")



    # 3. CONSULTA INICIAL: Solo libros con stock disponible (>0)

    libros_qs = Libros.objects.filter(stock_total__gt=0)



    # 4. APLICAR FILTROS Y BÚSQUEDA

    if q:

        libros_qs = libros_qs.filter(

            Q(titulo__icontains=q) |

            Q(autor__icontains=q) # Asumiendo que 'autor' es CharField en Libros

        ).distinct()



    if categoria_id:

        # Filtrar por categoría (asumiendo que Libros tiene una FK a Categoria)

        # Si Categoria es CharField, usar: libros_qs = libros_qs.filter(categoria__iexact=categoria_id)

        libros_qs = libros_qs.filter(categoria=categoria_id)



    # 5. ORDENAMIENTO

    if orden == "titulo":

        libros_qs = libros_qs.order_by("titulo")

    elif orden == "autor":

        libros_qs = libros_qs.order_by("autor")

    elif orden == "fecha":

        libros_qs = libros_qs.order_by("-fecha_registro")

    else:

        libros_qs = libros_qs.order_by("titulo")



    # 6. PAGINACIÓN

    paginator = Paginator(libros_qs, 9)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)



    # 7. OBTENER filtros (si Categoria existe como modelo)

    all_categorias = []

    try:

        from .models import Categoria

        all_categorias = Categoria.objects.all()

    except (ImportError, NameError):

        pass



    # 8. CONTEXTO PARA EL TEMPLATE

    ctx = {

        "libros": page_obj.object_list,

        "page_obj": page_obj,

        "total_libros": paginator.count,

        "q": q,

        "categoria": categoria_id,

        "orden": orden,

        "all_categorias": all_categorias,

    }



    # 9. RENDERIZADO DEL TEMPLATE PRIVADO

    return render(request, "clientes/catalogo_cliente.html", ctx)





@csrf_protect
@transaction.atomic
def reservar_libro(request, libro_id):

    """

    Vista que maneja la solicitud POST para crear una reserva desde el catálogo.

    """

    cliente, response = obtener_cliente_logueado(request)

    if response:

        return response

       

    if request.method == 'POST':

        libro = get_object_or_404(Libros, id=libro_id)



        # 1. Validaciones

        if (libro.stock_total or 0) <= 0:

            messages.error(request, f"El libro '{libro.titulo}' no tiene ejemplares disponibles para reservar.")

            return redirect("catalogo_cliente")



        if Reservas.objects.filter(cliente=cliente, libro=libro, estado='activa').exists():

            messages.warning(request, f"Ya tienes una reserva activa para '{libro.titulo}'.")

            return redirect("catalogo_cliente")



        # c. Obtener la regla de préstamo para calcular la fecha de vencimiento

        try:

            regla = ReglasPrestamo.objects.latest('fecha_actualizacion')

            plazo_reserva_dias = 3 # Plazo fijo para recoger, o usar campo de ReglasPrestamo

        except ReglasPrestamo.DoesNotExist:

            plazo_reserva_dias = 3 # Valor por defecto si no hay reglas



        # 2. Creación de la Reserva

        try:

            fecha_vencimiento = timezone.now() + timedelta(days=plazo_reserva_dias)

           

            Reservas.objects.create(

                cliente=cliente,

                libro=libro,

                fecha_reserva=timezone.now(),

                fecha_vencimiento=fecha_vencimiento,

                estado='activa' # Estado inicial de la reserva

            )

           

            # 3. Actualización de Stock (Se asume que la reserva "reserva" una unidad)

            libro.stock_total = (libro.stock_total or 0) - 1

            libro.save()



            messages.success(request, f"¡'{libro.titulo}' reservado con éxito! Tienes hasta el **{fecha_vencimiento.strftime('%d/%m/%Y')}** para recogerlo.")

           

        except Exception as e:

            messages.error(request, f"Error al reservar: {str(e)}")



    return redirect("lista_reservas_clientes") # Redirigir a la lista de reservas



@transaction.atomic

def cancelar_reserva(request, reserva_id):

    """

    Permite al cliente cancelar una reserva activa desde la lista de reservas.

    """

    cliente, response = obtener_cliente_logueado(request)

    if response:

        return response



    reserva = get_object_or_404(Reservas, id=reserva_id, cliente=cliente)



    if reserva.estado != 'activa':

        messages.warning(request, "Esta reserva ya no está activa y no puede cancelarse.")

        return redirect("lista_reservas_clientes")



    if request.method == 'POST':

        try:

            libro = reserva.libro

           

            # 1. Actualizar Stock: Devolver la unidad al stock disponible del libro

            libro.stock_total = (libro.stock_total or 0) + 1

            libro.save()

           

            # 2. Actualizar Estado de la Reserva

            reserva.estado = 'cancelada'

            reserva.save()



            messages.success(request, f"La reserva de '{libro.titulo}' ha sido cancelada correctamente.")

           

        except Exception as e:

            messages.error(request, f"Error al cancelar la reserva: {str(e)}")



    return redirect("lista_reservas_clientes")





def lista_reservas_clientes(request):

    """Vista de lista de reservas del cliente (Requiere login)."""

    cliente, response = obtener_cliente_logueado(request)

    if response:

        return response # Redirige a inicio de sesión si es None



    # Obtener todas las reservas del cliente, incluyendo activas y vencidas

    reservas = Reservas.objects.filter(

        cliente=cliente,

        estado__in=['activa', 'vencida']

    ).order_by('-fecha_reserva').select_related('libro')

   

    context = {

        'reservas': reservas,

    }

    return render(request, 'clientes/lista_reservas_clientes.html', context)





def cerrar_sesion_cliente(request):

    """Cierra la sesión del cliente."""

    # Limpiar la sesión

    if "cliente_id" in request.session:

        del request.session["cliente_id"]

    if "cliente_email" in request.session:

        del request.session["cliente_email"]

   

    messages.success(request, "Sesión cerrada correctamente")

    return redirect("inicio_sesion_cliente")


def confirmar_reserva(request, libro_id):
    """
    Vista GET: Muestra la información del libro y pide confirmación al cliente.
    """
    # 1. Comprobación de Sesión (Si falla, redirige al login)
    cliente, response = obtener_cliente_logueado(request)
    if response:
        return response

    # 2. Obtener Libro y Validaciones
    libro = get_object_or_404(Libros, id=libro_id)

    if (libro.stock_total or 0) <= 0:
        messages.error(request, f"El libro '{libro.titulo}' no tiene ejemplares disponibles para reservar.")
        return redirect("catalogo_cliente")

    # Validación extra: Si ya tiene reserva activa
    if Reservas.objects.filter(cliente=cliente, libro=libro, estado='activa').exists():
        messages.warning(request, f"Ya tienes una reserva activa para '{libro.titulo}'.")
        return redirect("catalogo_cliente")

    # 3. Renderizar página de confirmación
    context = {
        'libro': libro,
        'cliente': cliente,
        'plazo_reserva_dias': 3 # Puedes obtener esto de ReglasPrestamo si lo necesitas
    }
    return render(request, "clientes/confirmar_reserva.html", context)
