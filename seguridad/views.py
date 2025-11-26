from functools import wraps
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import logout as auth_logout
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
import random, re
from django.urls import reverse
from django.db import DatabaseError


from biblio.models import (
    Usuarios,
    Roles,
    Libros,
    Prestamos,
    Bitacora,
    ReglasPrestamo,
    Clientes,
    Ejemplares,
    Compras,
    Proveedores,
    DetalleCompras
)

# ---------- Helpers de sesión / roles ----------
def _usuario_autenticado(request):
    return request.session.get("id_usuario") is not None


def _obtener_rol_usuario(request):
    return request.session.get("rol_usuario")


def requerir_rol(*roles_permitidos):
    """Redirige a login si no hay sesión o si el rol no está permitido."""
    def decorador(vista):
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            if not _usuario_autenticado(request):
                return redirect("inicio_sesion")
            if _obtener_rol_usuario(request) not in roles_permitidos:
                return redirect("inicio_sesion")
            return vista(request, *args, **kwargs)
        return envoltura
    return decorador


# ---------- Login / Logout (empleados/admin) ----------
def _redirigir_segun_rol(rol):
    if rol == "administrador":
        return redirect("panel_administrador")
    else:
        return redirect("panel_bibliotecario")

@csrf_protect
def iniciar_sesion_empleado(request):
    # LIMPIAR MENSAJES PREVIOS
    storage = messages.get_messages(request)
    for message in storage:
        pass

    contexto = {"error": None}

    if request.method == "POST":
        correo = (request.POST.get("email") or "").strip().lower()
        contrasena = request.POST.get("password", "")
        recordar_sesion = request.POST.get("remember", "")

        # Validación básica
        if not correo or not contrasena:
            contexto["error"] = "Completa correo y contraseña."
            return render(request, "seguridad/login_empleados.html", contexto)

        try:
            # Buscar usuario activo que sea administrador o bibliotecario
            usuario = Usuarios.objects.select_related("rol").get(
                email=correo,
                estado="activo",
                rol__nombre__in=["administrador", "bibliotecario"],
            )
        except Usuarios.DoesNotExist:
            contexto["error"] = "Credenciales incorrectas. Intenta nuevamente."
            return render(request, "seguridad/login_empleados.html", contexto)
        except Usuarios.MultipleObjectsReturned:
            contexto["error"] = (
                "Existen múltiples cuentas asociadas a este correo. "
                "Contacta al administrador del sistema."
            )
            return render(request, "seguridad/login_empleados.html", contexto)

        # Verificar contraseña (soporta hasheadas y planas viejas)
        contrasena_bd = usuario.clave or ""
        if contrasena_bd.startswith(("pbkdf2_", "argon2$", "bcrypt$")):
            coincide = check_password(contrasena, contrasena_bd)
        else:
            coincide = (contrasena == contrasena_bd)

        if not coincide:
            contexto["error"] = "Credenciales incorrectas. Intenta nuevamente."
            return render(request, "seguridad/login_empleados.html", contexto)

        # Login exitoso → guardar datos básicos en sesión
        request.session["id_usuario"] = usuario.id
        request.session["correo_usuario"] = usuario.email
        request.session["rol_usuario"] = usuario.rol.nombre

        # Recordar sesión (14 días) o sesión normal (hasta cerrar navegador)
        request.session.set_expiry(
            60 * 60 * 24 * 14 if recordar_sesion == "on" else 0
        )

        # SI ES PRIMER INGRESO Y ES ADMIN/BIBLIOTECARIO → obligar a cambiar contraseña
        if usuario.primer_ingreso and usuario.rol.nombre in ("administrador", "bibliotecario"):
            request.session["primer_ingreso"] = True
            url_recuperar = reverse("recuperar_contrasena_empleado")
            # Mandamos SOLO el correo + flag de primer ingreso
            return redirect(f"{url_recuperar}?email={usuario.email}&primer_ingreso=1")

        # Si no es primer ingreso → flujo normal según rol
        if usuario.rol.nombre == "administrador":
            return redirect("panel_administrador")
        else:
            return redirect("panel_bibliotecario")

    # GET → mostrar formulario
    return render(request, "seguridad/login_empleados.html", contexto)


def cerrar_sesion_empleado(request):
    # Por si en algún momento se usa el sistema de auth de Django
    auth_logout(request)

    # Borrar claves específicas que usamos para empleados
    for key in ["id_usuario", "correo_usuario", "rol_usuario"]:
        if key in request.session:
            del request.session[key]

    # Vaciar por completo la sesión y regenerar la cookie
    request.session.flush()

    return redirect("inicio_sesion")


# ---------- Paneles ----------
@requerir_rol("administrador")
def panel_administrador(request):
    try:
        usuario_actual = Usuarios.objects.select_related("rol").get(
            id=request.session.get("id_usuario")
        )
    except Usuarios.DoesNotExist:
        return redirect("cerrar_sesion")

    total_libros = Libros.objects.count()

    # Cantidad de empleados activos (badge azul)
    empleados_activos = Usuarios.objects.filter(
        rol__nombre__in=["administrador", "bibliotecario"],
        estado__iexact="activo",
    ).count()

    # Parámetros de búsqueda y filtro
    query = (request.GET.get("q") or "").strip()
    estado_filtro = (request.GET.get("estado") or "").lower()

    # Query base: solo admins y bibliotecarios
    empleados_qs = Usuarios.objects.select_related("rol").filter(
        rol__nombre__in=["administrador", "bibliotecario"]
    )

    # Buscar por nombre
    if query:
        empleados_qs = empleados_qs.filter(nombre__icontains=query)

    # Filtrar por estado (activo / inactivo)
    if estado_filtro in ["activo", "inactivo"]:
        empleados_qs = empleados_qs.filter(estado__iexact=estado_filtro)

    empleados_qs = empleados_qs.order_by("-fecha_creacion")

    # Paginación: 5 empleados por página
    paginator = Paginator(empleados_qs, 5)
    page_number = request.GET.get("page")
    empleados_page = paginator.get_page(page_number)

    contexto = {
        "usuario_actual": usuario_actual,
        "total_libros": total_libros,
        "ventas_mensuales": None,
        "empleados_activos": empleados_activos,
        "empleados": empleados_page,
        "query": query,
        "estado_filtro": estado_filtro,
    }
    return render(request, "seguridad/admin_home.html", contexto)


def editar_empleado(request, empleado_id):
    empleado = get_object_or_404(
        Usuarios,
        id=empleado_id,
        rol__nombre__in=["administrador", "bibliotecario"],
    )

    if request.method == "POST":
        nombre = (request.POST.get("nombre") or "").strip()
        apellido = (request.POST.get("apellido") or "").strip()
        email = (request.POST.get("email") or "").strip()
        estado = (request.POST.get("estado") or "").strip().lower()

        if not (nombre and apellido and email):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect("panel_administrador")

        empleado.nombre = nombre
        empleado.apellido = apellido
        empleado.email = email

        if estado in ["activo", "inactivo"]:
            empleado.estado = estado

        empleado.save()

        messages.success(
            request,
            f"Empleado {empleado.nombre} {empleado.apellido} actualizado correctamente.",
        )

    return redirect("panel_administrador")


@requerir_rol("bibliotecario")
def panel_bibliotecario(request):
    try:
        usuario_actual = Usuarios.objects.select_related("rol").get(
            id=request.session.get("id_usuario")
        )
    except Usuarios.DoesNotExist:
        return redirect("cerrar_sesion")

    hoy = timezone.localdate()

    # Solo préstamos vencidos: sin devolución y con fecha_fin menor a hoy
    prestamos_vencidos_qs = Prestamos.objects.select_related(
        "ejemplar__libro",
        "cliente__usuario",
    ).filter(
        fecha_devolucion__isnull=True,
        fecha_fin__lt=hoy,
    ).order_by("fecha_fin")

    # Agregar días de retraso a cada préstamo
    prestamos_lista = []
    for p in prestamos_vencidos_qs:
        p.dias_retraso = (hoy - p.fecha_fin).days
        prestamos_lista.append(p)

    # Paginación: 5 por página
    paginator = Paginator(prestamos_lista, 5)
    page_number = request.GET.get("page")
    prestamos_retraso_page = paginator.get_page(page_number)

    contexto = {
        "usuario_actual": usuario_actual,
        "prestamos_retraso": prestamos_retraso_page,
        "prestamos_vencidos": prestamos_vencidos_qs.count(),  # solo esto se usa en el HTML
    }
    return render(request, "seguridad/bibliotecario_home.html", contexto)


@requerir_rol("administrador")
@csrf_protect
def registrar_empleado(request):
    roles_disponibles = [
        {
            "nombre_formulario": "admin",
            "nombre_bd": "administrador",
            "nombre_mostrar": "Administrador",
        },
        {
            "nombre_formulario": "bibliotecario",
            "nombre_bd": "bibliotecario",
            "nombre_mostrar": "Bibliotecario",
        },
    ]

    contexto = {
        "exito": None,
        "error": None,
        "roles": roles_disponibles,
        "usuario_actual": Usuarios.objects.get(id=request.session.get("id_usuario")),
    }

    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip().lower()
        apellido = request.POST.get("apellido", "").strip().lower()
        correo = request.POST.get("email", "").strip()
        contrasena = request.POST.get("clave", "")
        rol_formulario = request.POST.get("rol", "")
        estado = request.POST.get("estado", "activo")

        # Validaciones
        if not all([nombre, apellido, correo, contrasena, rol_formulario]):
            contexto["error"] = "Completa todos los campos obligatorios."
            return render(request, "seguridad/registrar_empleados.html", contexto)

        if len(contrasena) < 8:
            contexto["error"] = "La contraseña debe tener al menos 8 caracteres."
            return render(request, "seguridad/registrar_empleados.html", contexto)

        # Mapear rol formulario a base de datos
        mapeo_roles = {"admin": "administrador", "bibliotecario": "bibliotecario"}
        rol_bd = mapeo_roles.get(rol_formulario)

        if not rol_bd:
            contexto["error"] = "Rol inválido."
            return render(request, "seguridad/registrar_empleados.html", contexto)

        try:
            objeto_rol = Roles.objects.get(nombre=rol_bd)
        except Roles.DoesNotExist:
            contexto["error"] = f"No existe el rol '{rol_bd}' en la base de datos."
            return render(request, "seguridad/registrar_empleados.html", contexto)

        if Usuarios.objects.filter(email=correo).exists():
            contexto["error"] = "Ya existe un usuario con ese correo."
            return render(request, "seguridad/registrar_empleados.html", contexto)

        # Crear el usuario
        try:
            Usuarios.objects.create(
                rol=objeto_rol,
                nombre=nombre,
                apellido=apellido,
                email=correo,
                clave=make_password(contrasena),
                estado=estado,
                fecha_creacion=timezone.localtime(),
            )

            Bitacora.objects.create(
                usuario=contexto["usuario_actual"],
                accion=f"REGISTRO EMPLEADO: {correo} como {rol_bd}",
                fecha=timezone.now(),
            )

            contexto["exito"] = (
                f"Empleado {nombre} {apellido} creado exitosamente."
            )

        except Exception as error:
            contexto["error"] = f"Error al crear el usuario: {str(error)}"

    return render(request, "seguridad/registrar_empleados.html", contexto)


@requerir_rol("administrador")
@csrf_protect
def configurar_reglas_prestamo(request):
    """
    Vista para que el administrador configure las reglas generales de préstamo.
    Usa la última regla registrada o crea una nueva si no existe.
    """
    try:
        usuario_actual = Usuarios.objects.select_related("rol").get(
            id=request.session.get("id_usuario")
        )
    except Usuarios.DoesNotExist:
        return redirect("cerrar_sesion")

    # Tomamos la última regla (puede ser la única) o None si no existe
    regla = ReglasPrestamo.objects.order_by("-fecha_actualizacion").first()

    if request.method == "POST":
        plazo_dias = request.POST.get("plazo_dias")
        limite_prestamos = request.POST.get("limite_prestamos")
        tarifa_mora_diaria = request.POST.get("tarifa_mora_diaria")
        # si después quieres descripción adicional, la agregamos; por ahora lo simplificamos
        descripcion = "Reglas generales de préstamo"

        if not plazo_dias or not limite_prestamos or not tarifa_mora_diaria:
            messages.error(request, "Completa todos los campos.")
        else:
            try:
                if regla is None:
                    regla = ReglasPrestamo()

                regla.plazo_dias = int(plazo_dias)
                regla.limite_prestamos = int(limite_prestamos)
                regla.tarifa_mora_diaria = tarifa_mora_diaria
                regla.descripcion = descripcion
                regla.fecha_actualizacion = timezone.now()
                regla.save()

                Bitacora.objects.create(
                    usuario=usuario_actual,
                    accion=(
                        f"ACTUALIZÓ REGLAS DE PRÉSTAMO: "
                        f"plazo={regla.plazo_dias} días, "
                        f"límite={regla.limite_prestamos}, "
                        f"mora={regla.tarifa_mora_diaria}"
                    ),
                    fecha=timezone.now(),
                )

                messages.success(
                    request, "Reglas de préstamo actualizadas correctamente."
                )
                return redirect("configurar_reglas_prestamo")

            except Exception as e:
                messages.error(request, f"Error al guardar las reglas: {str(e)}")

    contexto = {
        "usuario_actual": usuario_actual,
        "regla": regla,
    }
    return render(request, "seguridad/reglas.html", contexto)


@requerir_rol("bibliotecario")
def inventario(request):
    # Usuario logueado
    usuario_actual = Usuarios.objects.select_related("rol").get(
        id=request.session.get("id_usuario")
    )

    # Búsqueda
    query = request.GET.get("q", "").strip()
    if query:
        libros_qs = (
            Libros.objects.filter(titulo__icontains=query)
            | Libros.objects.filter(autor__icontains=query)
            | Libros.objects.filter(isbn__icontains=query)
            | Libros.objects.filter(categoria__icontains=query)
        ).distinct().order_by("autor", "titulo")
    else:
        libros_qs = Libros.objects.all().order_by("titulo")

    # Paginación: 5 libros por página
    paginator = Paginator(libros_qs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # POST: agregar libro
    if request.method == "POST" and "agregar_libro" in request.POST:
        try:
            anio_publicacion = str(request.POST.get("anio_publicacion"))

            portada_file = request.FILES.get("portada")  # puede venir vacío

            libro = Libros(
                isbn=request.POST.get("isbn"),
                titulo=request.POST.get("titulo"),
                autor=request.POST.get("autor"),
                categoria=request.POST.get("categoria"),
                editorial=request.POST.get("editorial"),
                anio_publicacion=anio_publicacion,
                stock_total=request.POST.get("stock", 0),
                portada=portada_file,  # archivo de imagen
                fecha_registro=timezone.now(),  # fecha automática
            )
            libro.save()
            messages.success(request, "Libro agregado correctamente")
            return redirect("inventario")

        except Exception as e:
            messages.error(request, f"Error al agregar el libro: {str(e)}")
            return redirect("inventario")

    # POST: editar libro
    if request.method == "POST" and "editar_libro" in request.POST:
        try:
            libro_id = request.POST.get("libro_id")
            libro = get_object_or_404(Libros, id=libro_id)

            anio_publicacion = str(request.POST.get("anio_publicacion"))

            libro.titulo = request.POST.get("titulo")
            libro.autor = request.POST.get("autor")
            libro.categoria = request.POST.get("categoria")
            libro.editorial = request.POST.get("editorial")
            libro.anio_publicacion = anio_publicacion
            libro.stock_total = request.POST.get("stock", 0)

            # Si viene una nueva portada, la reemplazamos
            portada_file = request.FILES.get("portada")
            if portada_file:
                libro.portada = portada_file

            libro.save()

            Bitacora.objects.create(
                usuario=usuario_actual,
                accion=f"EDITO EL LIBRO: '{libro.titulo}'",
                fecha=timezone.now(),
            )

            messages.success(request, "Libro actualizado correctamente")
            return redirect("inventario")

        except Exception as e:
            messages.error(request, f"Error al actualizar el libro: {str(e)}")
            return redirect("inventario")

    contexto = {
        "usuario_actual": usuario_actual,
        "page_obj": page_obj,
        "query": query,
    }

    return render(request, "seguridad/inventario.html", contexto)



@requerir_rol("bibliotecario")
def gestion_prestamos(request):
    """
    Lista de préstamos activos para el bibliotecario, con buscador y paginación.
    """
    try:
        usuario_actual = Usuarios.objects.select_related("rol").get(
            id=request.session.get("id_usuario")
        )
    except Usuarios.DoesNotExist:
        return redirect("cerrar_sesion")

    query = (request.GET.get("q") or "").strip()

    prestamos_qs = (
        Prestamos.objects.select_related("cliente__usuario", "ejemplar__libro")
        .filter(estado="activo")
        .order_by("-fecha_inicio")
    )

    if query:
        prestamos_qs = prestamos_qs.filter(
            Q(cliente__usuario__nombre__icontains=query) |
            Q(cliente__usuario__apellido__icontains=query) |
            Q(cliente__dni__icontains=query)
        )

    paginator = Paginator(prestamos_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    contexto = {
        "usuario_actual": usuario_actual,
        "prestamos": page_obj,
        "query": query,
    }
    return render(request, "seguridad/gestion_prestamos.html", contexto)

UBICACIONES_PREDEFINIDAS = [
    "Estante A1 - Sección Literatura",
    "Estante B2 - Sección Ciencia",
    "Estante C3 - Sección Historia",
    "Estante D1 - Sección Infantil",
    "Depósito General",
]

def _crear_ejemplar_para_libro(libro):
    """
    Crea un Ejemplar físico para un libro dado, generando:
    - codigo_interno único (EJ-<id_libro>-####)
    - ubicacion aleatoria
    - estado aleatorio: nuevo / usado
    """
    base = f"EJ-{libro.id}-"
    codigo = None

    # Intentamos hasta 10 códigos diferentes para evitar colisión por unique
    for _ in range(10):
        sufijo = random.randint(1000, 9999)
        candidato = f"{base}{sufijo}"
        if not Ejemplares.objects.filter(codigo_interno=candidato).exists():
            codigo = candidato
            break

    # Último recurso si por alguna razón no se encontró libre
    if codigo is None:
        codigo = f"{base}{timezone.now().strftime('%H%M%S')}"

    ubicacion = random.choice(UBICACIONES_PREDEFINIDAS)
    estado = random.choice(["nuevo", "usado"])

    return Ejemplares.objects.create(
        libro=libro,
        codigo_interno=codigo,
        ubicacion=ubicacion,
        estado=estado,
    )


@requerir_rol("bibliotecario")
@csrf_protect
def registrar_prestamo(request):
    """
    Registrar un nuevo préstamo usando las reglas vigentes.
    - Busca cliente por DNI
    - Busca libro por ISBN
    - Crea un Ejemplar físico aleatorio (codigo_interno, ubicacion, estado)
    - Disminuye stock_total del libro
    - Muestra pantalla de detalle del préstamo + ejemplar
    """
    try:
        usuario_actual = Usuarios.objects.select_related("rol").get(
            id=request.session.get("id_usuario")
        )
    except Usuarios.DoesNotExist:
        return redirect("cerrar_sesion")

    regla = ReglasPrestamo.objects.order_by("-fecha_actualizacion").first()
    hoy = timezone.localdate()

    if regla is None:
        messages.error(
            request,
            "No hay reglas de préstamo configuradas. Configúralas primero."
        )
        return redirect("configurar_reglas_prestamo")

    form_data = {"dni": "", "isbn": ""}

    if request.method == "POST":
        dni = (request.POST.get("dni") or "").strip()
        isbn = (request.POST.get("isbn") or "").strip()
        fecha_inicio_str = request.POST.get("fecha_inicio") or hoy.isoformat()

        form_data["dni"] = dni
        form_data["isbn"] = isbn

        # Validar campos obligatorios
        if not dni or not isbn:
            messages.error(request, "Completa todos los campos.")
            return render(
                request,
                "seguridad/registrar_prestamo.html",
                {
                    "usuario_actual": usuario_actual,
                    "regla": regla,
                    "hoy": hoy,
                    "form_data": form_data,
                },
            )

        # Parsear fecha de inicio
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "La fecha de inicio no es válida.")
            return render(
                request,
                "seguridad/registrar_prestamo.html",
                {
                    "usuario_actual": usuario_actual,
                    "regla": regla,
                    "hoy": hoy,
                    "form_data": form_data,
                },
            )

        if fecha_inicio < hoy:
            messages.error(request, "La fecha de inicio no puede ser anterior a hoy.")
            return render(
                request,
                "seguridad/registrar_prestamo.html",
                {
                    "usuario_actual": usuario_actual,
                    "regla": regla,
                    "hoy": hoy,
                    "form_data": form_data,
                },
            )

        # Buscar cliente por DNI
        try:
            cliente = Clientes.objects.select_related("usuario").get(
                dni=dni, estado__iexact="activo"
            )
        except Clientes.DoesNotExist:
            messages.error(request, "No se encontró un cliente activo con ese DNI.")
            return render(
                request,
                "seguridad/registrar_prestamo.html",
                {
                    "usuario_actual": usuario_actual,
                    "regla": regla,
                    "hoy": hoy,
                    "form_data": form_data,
                },
            )

        # Validar límite de préstamos activos
        prestamos_activos_cliente = Prestamos.objects.filter(
            cliente=cliente,
            estado="activo",
        ).count()

        if prestamos_activos_cliente >= regla.limite_prestamos:
            messages.error(
                request,
                f"El cliente ya alcanzó el límite de {regla.limite_prestamos} préstamos activos."
            )
            return render(
                request,
                "seguridad/registrar_prestamo.html",
                {
                    "usuario_actual": usuario_actual,
                    "regla": regla,
                    "hoy": hoy,
                    "form_data": form_data,
                },
            )

        # Buscar libro por ISBN
        try:
            libro = Libros.objects.get(isbn=isbn)
        except Libros.DoesNotExist:
            messages.error(request, "No se encontró un libro con ese ISBN.")
            return render(
                request,
                "seguridad/registrar_prestamo.html",
                {
                    "usuario_actual": usuario_actual,
                    "regla": regla,
                    "hoy": hoy,
                    "form_data": form_data,
                },
            )

        # Validar stock
        if not libro.stock_total or libro.stock_total <= 0:
            messages.error(request, "No hay stock disponible para este libro.")
            return render(
                request,
                "seguridad/registrar_prestamo.html",
                {
                    "usuario_actual": usuario_actual,
                    "regla": regla,
                    "hoy": hoy,
                    "form_data": form_data,
                },
            )

        # Disminuir stock del libro
        libro.stock_total = (libro.stock_total or 0) - 1
        libro.save()

        # Crear ejemplar físico aleatorio (codigo_interno, ubicacion, estado)
        ejemplar = _crear_ejemplar_para_libro(libro)

        # Calcular fecha fin según plazo de la regla
        fecha_fin = fecha_inicio + timedelta(days=regla.plazo_dias)

        # Crear préstamo
        prestamo = Prestamos.objects.create(
            cliente=cliente,
            ejemplar=ejemplar,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado="activo",
        )

        Bitacora.objects.create(
            usuario=usuario_actual,
            accion=(
                f"REGISTRO PRÉSTAMO: cliente={cliente.dni}, "
                f"ejemplar={ejemplar.codigo_interno}, id_prestamo={prestamo.id}"
            ),
            fecha=timezone.now(),
        )

        # En lugar de redirigir, mostramos pantalla con los datos del EJEMPLAR
        messages.success(request, "Préstamo registrado correctamente.")
        return render(
            request,
            "seguridad/detalle_prestamo.html",
            {
                "usuario_actual": usuario_actual,
                "prestamo": prestamo,
                "ejemplar": ejemplar,
                "libro": libro,
                "cliente": cliente,
            },
        )

    # GET: mostrar formulario vacío
    contexto = {
        "usuario_actual": usuario_actual,
        "regla": regla,
        "hoy": hoy,
        "form_data": form_data,
    }
    return render(request, "seguridad/registrar_prestamo.html", contexto)



@requerir_rol("bibliotecario")
@csrf_protect
def devolver_prestamo(request, prestamo_id):
    """
    Marca un préstamo como devuelto.
    """
    if request.method != "POST":
        return redirect("gestion_prestamos")

    prestamo = get_object_or_404(
        Prestamos,
        id=prestamo_id,
        estado="activo",
    )

    prestamo.fecha_devolucion = timezone.localdate()
    prestamo.estado = "devuelto"
    prestamo.save()

    # Opcional: marcar ejemplar como disponible
    # ejemplar = prestamo.ejemplar
    # ejemplar.estado = "disponible"
    # ejemplar.save()

    Bitacora.objects.create(
        usuario=Usuarios.objects.get(id=request.session.get("id_usuario")),
        accion=f"DEVOLVIÓ PRÉSTAMO id={prestamo.id}",
        fecha=timezone.now(),
    )

    messages.success(request, "Libro devuelto.")
    return redirect("gestion_prestamos")


@requerir_rol("bibliotecario")
@csrf_protect
def renovar_prestamo(request, prestamo_id):
    """
    Renueva la fecha fin de un préstamo activo.
    """
    if request.method != "POST":
        return redirect("gestion_prestamos")

    prestamo = get_object_or_404(
        Prestamos,
        id=prestamo_id,
        estado="activo",
    )

    nueva_fecha_str = request.POST.get("nueva_fecha_fin")
    if not nueva_fecha_str:
        messages.error(
            request, "Debes seleccionar una nueva fecha de devolución."
        )
        return redirect("gestion_prestamos")

    try:
        nueva_fecha = datetime.strptime(nueva_fecha_str, "%Y-%m-%d").date()
    except ValueError:
        messages.error(
            request, "La nueva fecha de devolución no es válida."
        )
        return redirect("gestion_prestamos")

    if nueva_fecha <= prestamo.fecha_fin:
        messages.error(
            request,
            "La nueva fecha de devolución debe ser mayor a la fecha actual de devolución.",
        )
        return redirect("gestion_prestamos")

    prestamo.fecha_fin = nueva_fecha
    prestamo.save()

    Bitacora.objects.create(
        usuario=Usuarios.objects.get(id=request.session.get("id_usuario")),
        accion=f"RENOVÓ PRÉSTAMO id={prestamo.id} nueva_fecha={nueva_fecha}",
        fecha=timezone.now(),
    )

    messages.success(request, "El préstamo se renovó correctamente.")
    return redirect("gestion_prestamos")


##########################################################
##-----------------------RECUPERACIÓN DE CONTRASEÑA-------
##########################################################

def recuperar_contrasena_empleado(request):
    """
    Vista principal de recuperación / establecimiento de contraseña.
    """
    # Detectar si viene marcado como primer ingreso (GET o POST)
    primer_ingreso_flag = (
        request.GET.get("primer_ingreso") == "1"
        or request.POST.get("primer_ingreso") == "1"
        or request.session.get("primer_ingreso") is True
    )

    email_precargado = request.GET.get("email", "").strip().lower()

    if request.method == "POST":
        step = request.POST.get("step", "1")
        if step == "1":
            return paso_1_verificar_correo(request)
        elif step == "2":
            return paso_2_nueva_contrasena(request)

    contexto = {"step": 1}

    if primer_ingreso_flag and email_precargado:
        contexto["email"] = email_precargado
        contexto["primer_ingreso"] = True

    return render(request, "seguridad/recuperar_contraseña.html", contexto)


def paso_1_verificar_correo(request):
    """
    Paso 1: verificación de correo.
    """
    email = (request.POST.get("email") or "").strip().lower()
    primer_ingreso_flag = request.POST.get("primer_ingreso") == "1"

    if not email:
        return render(
            request,
            "seguridad/recuperar_contraseña.html",
            {
                "step": 1,
                "email": email,
                "primer_ingreso": primer_ingreso_flag,
                "error": "Por favor, complete el correo electrónico.",
            },
        )

    try:
        
        usuario = (
            Usuarios.objects
            .select_related("rol")
            .filter(
                email=email,
                estado="activo",
                rol__nombre__in=["administrador", "bibliotecario"],
            )
            .first()
        )

        if not usuario:
            return render(
                request,
                "seguridad/recuperar_contraseña.html",
                {
                    "step": 1,
                    "email": email,
                    "primer_ingreso": primer_ingreso_flag,
                    "error": "No se encontró un empleado activo con ese correo.",
                },
            )

        # Correo válido → pasar a paso 2
        return render(
            request,
            "seguridad/recuperar_contraseña.html",
            {
                "step": 2,
                "email": email,
                "primer_ingreso": primer_ingreso_flag,
            },
        )

    except Exception:
        return render(
            request,
            "seguridad/recuperar_contraseña.html",
            {
                "step": 1,
                "email": email,
                "primer_ingreso": primer_ingreso_flag,
                "error": "Error en el sistema. Por favor, intente más tarde.",
            },
        )


def paso_2_nueva_contrasena(request):
    """
    Paso 2: establecer nueva contraseña.
    """
    email = (request.POST.get("email") or "").strip().lower()
    new_password = request.POST.get("new_password", "")
    confirm_password = request.POST.get("confirm_password", "")
    primer_ingreso_flag = request.POST.get("primer_ingreso") == "1"

    # Validar igualdad
    if new_password != confirm_password:
        return render(
            request,
            "seguridad/recuperar_contraseña.html",
            {
                "step": 2,
                "email": email,
                "primer_ingreso": primer_ingreso_flag,
                "error": "Las contraseñas no coinciden.",
            },
        )

    # Validar fortaleza
    if not validar_fortaleza_contrasena(new_password):
        return render(
            request,
            "seguridad/recuperar_contraseña.html",
            {
                "step": 2,
                "email": email,
                "primer_ingreso": primer_ingreso_flag,
                "error": (
                    "La contraseña debe tener al menos 8 caracteres, incluir una letra "
                    "mayúscula, una minúscula, un número y un carácter especial."
                ),
            },
        )

    try:
        # Buscar empleado activo por correo (administrador / bibliotecario)
        usuario = (
            Usuarios.objects
            .select_related("rol")
            .filter(
                email=email,
                estado="activo",
                rol__nombre__in=["administrador", "bibliotecario"],
            )
            .first()
        )

        if not usuario:
            
            return render(
                request,
                "seguridad/recuperar_contraseña.html",
                {
                    "step": 1,
                    "error": "Error en la recuperación. Por favor, inicie el proceso nuevamente.",
                },
            )

        usuario.clave = make_password(new_password)

        # Si era primer ingreso → se marca como ya no primer ingreso
        if primer_ingreso_flag or request.session.get("primer_ingreso"):
            usuario.primer_ingreso = False

        usuario.save()

        # Limpiar flag de primer ingreso de la sesión
        if "primer_ingreso" in request.session:
            del request.session["primer_ingreso"]

        # Paso 3: éxito
        contexto = {"step": 3}
        if primer_ingreso_flag:
            contexto[
                "mensaje_especial"
            ] = "¡Contraseña establecida! Ahora puedes acceder al sistema."

        return render(request, "seguridad/recuperar_contraseña.html", contexto)

    except DatabaseError:
        return render(
            request,
            "seguridad/recuperar_contraseña.html",
            {
                "step": 2,
                "email": email,
                "primer_ingreso": primer_ingreso_flag,
                "error": "Error al guardar la nueva contraseña. Por favor, intente nuevamente.",
            },
        )
    except Exception:
        return render(
            request,
            "seguridad/recuperar_contraseña.html",
            {
                "step": 2,
                "email": email,
                "primer_ingreso": primer_ingreso_flag,
                "error": "Error inesperado. Intente nuevamente.",
            },
        )


def validar_fortaleza_contrasena(password):
    """
    Valida que la contraseña cumpla con los requisitos de seguridad
    """
    if len(password) < 8:
        return False

    # Verificar requisitos de seguridad
    tiene_mayuscula = any(c.isupper() for c in password)
    tiene_minuscula = any(c.islower() for c in password)
    tiene_numero = any(c.isdigit() for c in password)
    tiene_especial = any(not c.isalnum() for c in password)

    return (
        tiene_mayuscula
        and tiene_minuscula
        and tiene_numero
        and tiene_especial
    )

################################################################
####----------------------GESTION DE COMPRAS ------------------
################################################################


def gestion_proveedores(request):
    # Verificar sesión
    try:
        usuario_actual = Usuarios.objects.get(id=request.session.get("id_usuario"))
    except Usuarios.DoesNotExist:
        return redirect("cerrar_sesion")

    query = (request.GET.get("q") or "").strip()

    proveedores_qs = Proveedores.objects.all().order_by("nombre_comercial")

    #--opciones de busqueda

    if query:
        proveedores_qs = proveedores_qs.filter(
            Q(nombre_comercial__icontains=query) |
            Q(rtn__icontains=query)
        )

        #--agregar nuevo proveedor

    if request.method == "POST":
        if "agregar_proveedor" in request.POST:
            nombre_comercial = (request.POST.get("nombre_comercial") or "").strip()
            rtn = (request.POST.get("rtn") or "").strip()
            direccion = (request.POST.get("direccion") or "").strip()
            telefono = (request.POST.get("telefono") or "").strip()
            correo_contacto = (request.POST.get("correo_contacto") or "").strip()
            suministro = (request.POST.get("suministro") or "").strip()
            estado = (request.POST.get("estado") or "").strip() or "activo"

            # Validaciones 
            if not nombre_comercial:
                messages.error(request, "El nombre comercial es obligatorio.")
                return redirect("gestion_proveedores")

            if not rtn:
                messages.error(request, "El RTN es obligatorio.")
                return redirect("gestion_proveedores")

            if not re.fullmatch(r"\d{14}", rtn):
                messages.error(request, "El RTN debe contener exactamente 14 dígitos numéricos.")
                return redirect("gestion_proveedores")

            if telefono:
                if not re.fullmatch(r"[2389]\d{7}", telefono):
                    messages.error(
                        request,
                        "El teléfono debe tener 8 dígitos y comenzar con 2, 3, 8 o 9."
                    )
                    return redirect("gestion_proveedores")

            # Validar RTN único
            if Proveedores.objects.filter(rtn=rtn).exists():
                messages.error(request, "Ya existe un proveedor con ese RTN.")
                return redirect("gestion_proveedores")

            Proveedores.objects.create(
                nombre_comercial=nombre_comercial,
                rtn=rtn,
                direccion=direccion or None,
                telefono=telefono or None,
                correo_contacto=correo_contacto or None,
                suministro=suministro or None,
                estado=estado,
            )

            messages.success(request, "Proveedor agregado correctamente.")
            return redirect("gestion_proveedores")

        if "editar_proveedor" in request.POST:
            proveedor_id = request.POST.get("proveedor_id")
            proveedor = get_object_or_404(Proveedores, id=proveedor_id)

            nombre_comercial = (request.POST.get("nombre_comercial") or "").strip()
            rtn = (request.POST.get("rtn") or "").strip()
            direccion = (request.POST.get("direccion") or "").strip()
            telefono = (request.POST.get("telefono") or "").strip()
            correo_contacto = (request.POST.get("correo_contacto") or "").strip()
            suministro = (request.POST.get("suministro") or "").strip()
            estado = (request.POST.get("estado") or "").strip() or "activo"

            #Validaciones

            if not nombre_comercial:
                messages.error(request, "El nombre comercial es obligatorio.")
                return redirect("gestion_proveedores")

            if not rtn:
                messages.error(request, "El RTN es obligatorio.")
                return redirect("gestion_proveedores")

            if not re.fullmatch(r"\d{14}", rtn):
                messages.error(request, "El RTN debe contener exactamente 14 dígitos numéricos.")
                return redirect("gestion_proveedores")

            if telefono:
                if not re.fullmatch(r"[2389]\d{7}", telefono):
                    messages.error(
                        request,
                        "El teléfono debe tener 8 dígitos y comenzar con 2, 3, 8 o 9."
                    )
                    return redirect("gestion_proveedores")

            if Proveedores.objects.filter(rtn=rtn).exclude(id=proveedor.id).exists():
                messages.error(request, "Ya existe otro proveedor con ese RTN.")
                return redirect("gestion_proveedores")

            proveedor.nombre_comercial = nombre_comercial
            proveedor.rtn = rtn
            proveedor.direccion = direccion or None
            proveedor.telefono = telefono or None
            proveedor.correo_contacto = correo_contacto or None
            proveedor.suministro = suministro or None
            proveedor.estado = estado
            proveedor.save()

            messages.success(request, "Proveedor actualizado correctamente.")
            return redirect("gestion_proveedores")


    paginator = Paginator(proveedores_qs, 10)
    page_number = request.GET.get("page")
    proveedores = paginator.get_page(page_number)

    context = {
        "proveedores": proveedores,
        "query": query,
        "usuario_actual": usuario_actual,
    }
    return render(request, "seguridad/proveedores.html", context)


def gestion_compras(request):
    # Verificar sesión
    try:
        usuario_actual = Usuarios.objects.get(id=request.session.get("id_usuario"))
    except Usuarios.DoesNotExist:
        return redirect("cerrar_sesion")

    query = (request.GET.get("q") or "").strip()
    fecha_desde = (request.GET.get("fecha_desde") or "").strip()
    fecha_hasta = (request.GET.get("fecha_hasta") or "").strip()

    # Base queryset (ya con proveedor, usuario y detalles)
    compras_qs = (
        Compras.objects
        .select_related("proveedor", "usuario")
        .prefetch_related("detalles__libro")
        .all()
        .order_by("-fecha", "-id")
    )

    # Filtros de búsqueda
    if query:
        compras_qs = compras_qs.filter(
            Q(proveedor__nombre_comercial__icontains=query) |
            Q(proveedor__rtn__icontains=query) |
            Q(numero_factura__icontains=query)
        )

    if fecha_desde:
        compras_qs = compras_qs.filter(fecha__date__gte=fecha_desde)

    if fecha_hasta:
        compras_qs = compras_qs.filter(fecha__date__lte=fecha_hasta)

    # ------------------------------
    # POST: crear o editar una compra
    # ------------------------------
    if request.method == "POST":

        # ==========================
        # ➕ AGREGAR COMPRA
        # ==========================
        if "agregar_compra" in request.POST:
            proveedor_nombre = (request.POST.get("proveedor_nombre") or "").strip()
            metodo_pago = (request.POST.get("metodo_pago") or "").strip()

            libro_ids = request.POST.getlist("libro_id[]")
            cantidades = request.POST.getlist("cantidad[]")
            costos = request.POST.getlist("costo_unitario[]")

            # ✅ Validar proveedor (solo activos)
            if not proveedor_nombre:
                messages.error(request, "Debe seleccionar un proveedor.")
                return redirect("gestion_compras")

            try:
                proveedor = Proveedores.objects.get(
                    nombre_comercial=proveedor_nombre,
                    estado="activo"
                )
            except Proveedores.DoesNotExist:
                messages.error(
                    request,
                    "El proveedor indicado no existe o no está activo."
                )
                return redirect("gestion_compras")
            except Proveedores.MultipleObjectsReturned:
                messages.error(
                    request,
                    "Existe más de un proveedor con ese nombre. "
                    "Use nombres únicos o edite los proveedores."
                )
                return redirect("gestion_compras")

            # Validar método de pago
            if not metodo_pago:
                messages.error(request, "Debe seleccionar un método de pago.")
                return redirect("gestion_compras")

            # Validar ítems
            items = []
            for idx, libro_id in enumerate(libro_ids):
                libro_id = (libro_id or "").strip()
                cant = (cantidades[idx] if idx < len(cantidades) else "").strip()
                costo = (costos[idx] if idx < len(costos) else "").strip()

                # Fila completamente vacía → la ignoramos
                if not (libro_id or cant or costo):
                    continue

                if not (libro_id and cant and costo):
                    messages.error(
                        request,
                        "Todas las filas deben tener libro, cantidad y costo unitario. "
                        "Elimine las filas que no vaya a usar."
                    )
                    return redirect("gestion_compras")

                libro = get_object_or_404(Libros, id=libro_id)

                try:
                    cant_int = int(cant)
                    costo_dec = float(costo)
                except ValueError:
                    messages.error(request, "Cantidad y costo unitario deben ser numéricos.")
                    return redirect("gestion_compras")

                if cant_int <= 0:
                    messages.error(request, "La cantidad debe ser mayor que cero.")
                    return redirect("gestion_compras")

                if costo_dec <= 0:
                    messages.error(request, "El costo unitario debe ser mayor que cero.")
                    return redirect("gestion_compras")

                subtotal = cant_int * costo_dec
                items.append({
                    "libro": libro,
                    "cantidad": cant_int,
                    "costo_unitario": costo_dec,
                    "subtotal": subtotal,
                })

            if not items:
                messages.error(request, "Debe agregar al menos un libro a la compra.")
                return redirect("gestion_compras")

            # Número de factura: SIEMPRE automático
            ultima = Compras.objects.order_by("-id").first()
            siguiente = (ultima.id if ultima else 0) + 1
            numero_factura = f"FAC-{siguiente:06d}"

            total_compra = sum(i["subtotal"] for i in items)

            # Guardar SOLO fecha (sin hora)
            fecha_hoy = timezone.now().date()

            try:
                compra = Compras.objects.create(
                    proveedor=proveedor,
                    usuario=usuario_actual,
                    numero_factura=numero_factura,
                    fecha=fecha_hoy,
                    total=total_compra,
                    metodo_pago=metodo_pago,
                )
            except Exception:
                messages.error(
                    request,
                    "Error al registrar la compra. Verifique que los datos sean correctos."
                )
                return redirect("gestion_compras")

            # Crear detalles y actualizar stock
            for item in items:
                DetalleCompras.objects.create(
                    compra=compra,
                    libro=item["libro"],
                    cantidad=item["cantidad"],
                    costo_unitario=item["costo_unitario"],
                    subtotal=item["subtotal"],
                )

                libro = item["libro"]
                libro.stock_total = (libro.stock_total or 0) + item["cantidad"]
                libro.save()

            # Bitácora
            Bitacora.objects.create(
                usuario=usuario_actual,
                accion=(
                    f"REGISTRÓ COMPRA id={compra.id} "
                    f"factura={compra.numero_factura} "
                    f"proveedor={compra.proveedor.nombre_comercial} "
                    f"total={compra.total}"
                ),
                fecha=timezone.now(),
            )

            messages.success(request, "La compra se registró correctamente.")
            return redirect("gestion_compras")

        # ==========================
        # ✏️ EDITAR COMPRA
        # ==========================
        if "editar_compra" in request.POST:
            compra_id = request.POST.get("compra_id")
            proveedor_nombre = (request.POST.get("proveedor_nombre") or "").strip()
            metodo_pago = (request.POST.get("metodo_pago") or "").strip()

            compra = get_object_or_404(Compras, id=compra_id)

            if not proveedor_nombre:
                messages.error(request, "Debe seleccionar un proveedor.")
                return redirect("gestion_compras")

            try:
                proveedor = Proveedores.objects.get(
                    nombre_comercial=proveedor_nombre,
                    estado="activo"
                )
            except Proveedores.DoesNotExist:
                messages.error(
                    request,
                    "El proveedor indicado no existe o no está activo."
                )
                return redirect("gestion_compras")
            except Proveedores.MultipleObjectsReturned:
                messages.error(
                    request,
                    "Existe más de un proveedor con ese nombre. "
                    "Use nombres únicos o edite los proveedores."
                )
                return redirect("gestion_compras")

            if not metodo_pago:
                messages.error(request, "Debe seleccionar un método de pago.")
                return redirect("gestion_compras")

            compra.proveedor = proveedor
            compra.metodo_pago = metodo_pago
            compra.save()

            Bitacora.objects.create(
                usuario=usuario_actual,
                accion=(
                    f"EDITÓ COMPRA id={compra.id} "
                    f"factura={compra.numero_factura} "
                    f"proveedor={compra.proveedor.nombre_comercial} "
                    f"total={compra.total}"
                ),
                fecha=timezone.now(),
            )

            messages.success(request, "La compra se actualizó correctamente.")
            return redirect("gestion_compras")

    # Paginación
    paginator = Paginator(compras_qs, 10)
    page_number = request.GET.get("page")
    compras = paginator.get_page(page_number)

    # 👇 Solo proveedores ACTIVOS para los selects del HTML
    proveedores = Proveedores.objects.filter(estado="activo").order_by("nombre_comercial")
    libros = Libros.objects.all().order_by("titulo")

    context = {
        "compras": compras,
        "query": query,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
        "proveedores": proveedores,
        "libros": libros,
        "usuario_actual": usuario_actual,
    }
    return render(request, "seguridad/gestion_compras.html", context)
#------------comprobante_compra_digital---------------------------
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io

# ...

def comprobante_compra_pdf(request, compra_id):
    # Carga la compra con proveedor, usuario y detalles de libros
    compra = get_object_or_404(
        Compras.objects
        .select_related("proveedor", "usuario")
        .prefetch_related("detalles__libro"),
        id=compra_id,
    )

    # Renderizar el HTML del comprobante
    html = render_to_string("seguridad/comprobante_compra.html", {
        "compra": compra,
    })

    # Preparar respuesta HTTP como PDF descargable
    response = HttpResponse(content_type="application/pdf")
    filename = f"comprobante_{compra.numero_factura}.pdf"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    # Generar PDF desde el HTML
    pisa_status = pisa.CreatePDF(
        src=html,
        dest=response,
        encoding="utf-8",
    )

    if pisa_status.err:
        return HttpResponse("Ocurrió un error al generar el PDF.", status=500)

    return response
