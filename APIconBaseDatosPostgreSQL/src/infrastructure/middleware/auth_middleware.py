# src/infrastructure/middleware/auth_middleware.py
"""
Middleware para autenticación y autorización de usuarios.
"""

from functools import wraps
from flask import request, jsonify, current_app
from typing import List, Optional
import logging

from src.infrastructure.services.jwt_service import JWTService

logger = logging.getLogger(__name__)


def token_required(f):
    """
    Decorador que requiere un token JWT válido.

    Verifica que el header Authorization contenga un Bearer token válido
    y agrega la información del usuario al request.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'error': 'Token requerido',
                'message': 'Se requiere header Authorization con Bearer token'
            }), 401

        token = auth_header.split(' ')[1]

        # Validar token
        jwt_service = JWTService()
        payload = jwt_service.validate_user_token(token)

        if not payload:
            return jsonify({
                'error': 'Token inválido',
                'message': 'El token no es válido o ha expirado'
            }), 401

        # Agregar información del usuario al request
        request.current_user = {
            'id': payload['user_id'],
            'email': payload['email'],
            'role': payload['role'],
            'universidad_id': payload.get('universidad_id')
        }

        return f(*args, **kwargs)

    return decorated_function


def role_required(allowed_roles: List[str]):
    """
    Decorador que requiere que el usuario tenga uno de los roles especificados.

    Args:
        allowed_roles: Lista de roles permitidos (ej: ['administrador', 'operador'])

    Debe usarse después de @token_required
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'current_user'):
                return jsonify({
                    'error': 'Usuario no autenticado',
                    'message': 'Se requiere autenticación previa'
                }), 401

            user_role = request.current_user.get('role')
            if user_role not in allowed_roles:
                return jsonify({
                    'error': 'Acceso denegado',
                    'message': f'Se requiere uno de los siguientes roles: {", ".join(allowed_roles)}'
                }), 403

            return f(*args, **kwargs)

        return decorated_function
    return decorator


def device_token_required(f):
    """
    Decorador que requiere un token de dispositivo válido.

    Verifica que el header Authorization contenga un Bearer token de dispositivo válido
    y agrega la información del dispositivo al request.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'error': 'Token de dispositivo requerido',
                'message': 'Se requiere header Authorization con Bearer token de dispositivo'
            }), 401

        token = auth_header.split(' ')[1]

        # Validar token de dispositivo
        jwt_service = JWTService()
        payload = jwt_service.validate_device_token(token)

        if not payload:
            return jsonify({
                'error': 'Token de dispositivo inválido',
                'message': 'El token de dispositivo no es válido o ha expirado'
            }), 401

        # Agregar información del dispositivo al request
        request.current_device = {
            'id': payload['device_id'],
            'mac_address': payload['mac_address']
        }

        return f(*args, **kwargs)

    return decorated_function


def universidad_required(f):
    """
    Decorador que verifica que el usuario tenga acceso a la universidad especificada.

    Para administradores: acceso total
    Para operadores: acceso solo a su universidad
    Para limpiadores: acceso solo a su universidad

    Espera que el parámetro 'universidad_id' esté presente en la URL o en el body.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(request, 'current_user'):
            return jsonify({
                'error': 'Usuario no autenticado',
                'message': 'Se requiere autenticación previa'
            }), 401

        current_user = request.current_user
        user_role = current_user.get('role')
        user_universidad_id = current_user.get('universidad_id')

        # Administradores tienen acceso total
        if user_role == 'administrador':
            return f(*args, **kwargs)

        # Obtener universidad_id de diferentes fuentes
        universidad_id = None

        # De parámetros de URL
        if 'universidad_id' in kwargs:
            universidad_id = kwargs['universidad_id']

        # De parámetros de query
        if not universidad_id:
            universidad_id = request.args.get('universidad_id', type=int)

        # De body JSON
        if not universidad_id:
            data = request.get_json(silent=True)
            if data and 'universidad_id' in data:
                universidad_id = data['universidad_id']

        # Si no se especifica universidad, permitir (para listados generales)
        if universidad_id is None:
            return f(*args, **kwargs)

        # Verificar acceso
        if user_universidad_id != universidad_id:
            return jsonify({
                'error': 'Acceso denegado',
                'message': f'No tienes acceso a la universidad con ID {universidad_id}'
            }), 403

        return f(*args, **kwargs)

    return decorated_function


def log_request(f):
    """
    Decorador que registra las peticiones HTTP para auditoría.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        method = request.method
        path = request.path
        user_info = ""

        if hasattr(request, 'current_user'):
            user_info = f" - User: {request.current_user['email']}"
        elif hasattr(request, 'current_device'):
            user_info = f" - Device: {request.current_device['mac_address']}"

        logger.info(f"{method} {path}{user_info}")

        # Llamar a la función original
        response = f(*args, **kwargs)

        # Si response es una tupla (response, status), extraer status
        status_code = 200
        if isinstance(response, tuple) and len(response) == 2:
            status_code = response[1]

        logger.info(f"Response: {status_code}")
        return response

    return decorated_function


def rate_limit(limit: int = 100, window: int = 60):
    """
    Decorador para limitar la tasa de peticiones.

    Args:
        limit: Número máximo de peticiones permitidas
        window: Ventana de tiempo en segundos

    Nota: Esta es una implementación básica. En producción se debería usar Redis.
    """
    # Almacenamiento simple en memoria (no recomendado para producción)
    requests_log = {}

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Obtener identificador del cliente (IP o user_id)
            client_id = request.remote_addr
            if hasattr(request, 'current_user'):
                client_id = str(request.current_user['id'])

            current_time = request.environ.get('REQUEST_TIME', 0)

            # Limpiar entradas antiguas
            cutoff_time = current_time - window
            if client_id in requests_log:
                requests_log[client_id] = [
                    t for t in requests_log[client_id] if t > cutoff_time
                ]

            # Verificar límite
            if client_id not in requests_log:
                requests_log[client_id] = []

            if len(requests_log[client_id]) >= limit:
                return jsonify({
                    'error': 'Límite de tasa excedido',
                    'message': f'Máximo {limit} peticiones por {window} segundos'
                }), 429

            # Registrar petición
            requests_log[client_id].append(current_time)

            return f(*args, **kwargs)

        return decorated_function
    return decorator