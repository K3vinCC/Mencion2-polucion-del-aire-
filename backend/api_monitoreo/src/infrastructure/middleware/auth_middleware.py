# src/infrastructure/middleware/auth_middleware.py
import jwt
from functools import wraps
from flask import request, current_app, g
from src.infrastructure.dependencies import container
from src.application.errors.exceptions import TokenInvalidoError, PermisosInsuficientesError

def token_required(f):
    """
    Decorador que requiere un token JWT válido.
    Extrae el usuario del token y lo guarda en el contexto global de Flask (g).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Extraer token del header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            raise TokenInvalidoError("Token de acceso requerido")

        try:
            # Decodificar el token
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            usuario_id = payload['sub']

            # Obtener el usuario de la base de datos
            obtener_usuario_use_case = container.obtener_usuario_use_case
            usuario = obtener_usuario_use_case.ejecutar(usuario_id)

            if not usuario:
                raise TokenInvalidoError("Usuario no encontrado")

            # Guardar el usuario en el contexto global
            g.usuario = usuario

        except jwt.ExpiredSignatureError:
            raise TokenInvalidoError("Token expirado")
        except jwt.InvalidTokenError:
            raise TokenInvalidoError("Token inválido")

        return f(*args, **kwargs)
    return decorated_function

def device_token_required(f):
    """
    Decorador que requiere un token de dispositivo válido.
    Extrae el dispositivo del token y lo guarda en el contexto global.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Extraer token del header X-Device-Token
        if 'X-Device-Token' in request.headers:
            token = request.headers['X-Device-Token']

        if not token:
            raise TokenInvalidoError("Token de dispositivo requerido")

        try:
            # Buscar el dispositivo por token
            dispositivo_repository = container.dispositivo_repository
            dispositivo = dispositivo_repository.find_by_token(token)

            if not dispositivo:
                raise TokenInvalidoError("Dispositivo no encontrado")

            # Guardar el dispositivo en el contexto global
            g.dispositivo = dispositivo

        except Exception:
            raise TokenInvalidoError("Token de dispositivo inválido")

        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorador que requiere permisos de administrador.
    Debe usarse junto con token_required.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'usuario'):
            raise TokenInvalidoError("Usuario no autenticado")

        if g.usuario.rol != 'administrador':
            raise PermisosInsuficientesError("Se requieren permisos de administrador")

        return f(*args, **kwargs)
    return decorated_function

def conserje_required(f):
    """
    Decorador que requiere permisos de conserje o administrador.
    Debe usarse junto con token_required.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'usuario'):
            raise TokenInvalidoError("Usuario no autenticado")

        if g.usuario.rol not in ['administrador', 'conserje']:
            raise PermisosInsuficientesError("Se requieren permisos de conserje o administrador")

        return f(*args, **kwargs)
    return decorated_function