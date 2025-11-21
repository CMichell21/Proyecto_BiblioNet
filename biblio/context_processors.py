from .models import Cliente

def cliente_data(request):
    """
    Inyecta datos cruciales del cliente (ID y Estado) en el contexto de la plantilla 
    para ser usados en botones condicionales y URLs.
    """
    
    cliente_info = {
        'cliente_id': None,
        'cliente_activo': False,
    }

    if request.user.is_authenticated:
        # Asumimos que request.user es el objeto Usuario logueado.
        # Si NO estás usando AUTH_USER_MODEL, necesitarás cambiar request.user.pk 
        # por el método que uses para obtener el ID de tu Usuario.
        
        try:
            # Buscamos la relación de Cliente usando el ID del Usuario logueado.
            # Nota: Usamos 'usuario_id' para buscar por la FK.
            cliente = Cliente.objects.get(usuario_id=request.user.pk)
            
            # El ID del cliente (primary key de la tabla 'clientes')
            cliente_info['cliente_id'] = cliente.pk 
            
            # El estado es el campo que necesitamos verificar
            if cliente.estado and cliente.estado.lower() == 'activo':
                cliente_info['cliente_activo'] = True
                
        except Cliente.DoesNotExist:
            # El usuario está logueado pero no tiene un registro de cliente asociado (e.g., es un administrador o un usuario sin perfil)
            pass
            
    return cliente_info