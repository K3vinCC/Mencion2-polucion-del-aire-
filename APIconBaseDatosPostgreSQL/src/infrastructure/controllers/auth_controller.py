# src/infrastructure/controllers/auth_controller.py
"""
Controlador REST para autenticación de usuarios y dispositivos.
"""

from flask import Blueprint, request, jsonify, current_app
from typing import Dict, Any
import logging

from src.application.use_cases.autenticar_usuario import AutenticarUsuario
from src.infrastructure.repositories.usuario_repository import UsuarioRepository
from src.infrastructure.services.jwt_service import JWTService

logger = logging.getLogger(__name__)

# Crear blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint para autenticación de usuarios.

    Body esperado:
    {
        "email": "usuario@ejemplo.com",
        "password": "contraseña"
    }

    Returns:
        JSON con token de acceso o error
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Datos requeridos',
                'message': 'Se requiere body JSON con email y password'
            }), 400

        email = data.get('email')
        password = data.get('password')

        # Compatibilidad con documento maestro: aceptar 'clave' además de 'password'
        password = password or data.get('clave')
        
        if not email or not password:
            return jsonify({
                'error': 'Campos requeridos',
                'message': 'Email y password/clave son obligatorios'
            }), 400

        # Inicializar dependencias
        usuario_repo = UsuarioRepository()
        jwt_service = JWTService()
        autenticar_usuario = AutenticarUsuario(usuario_repo, jwt_service)

        # Ejecutar caso de uso
        result = autenticar_usuario.execute(email, password)

        if result['success']:
            logger.info(f"Usuario {email} autenticado exitosamente")
            return jsonify({
                'access_token': result['access_token'],
                'token_type': 'Bearer',
                'expires_in': current_app.config['JWT_EXPIRATION_HOURS'] * 3600,
                'user': {
                    'id': result['user']['id'],
                    'email': result['user']['email'],
                    'role': result['user']['role'],
                    'universidad_id': result['user']['universidad_id']
                }
            }), 200
        else:
            logger.warning(f"Fallo de autenticación para {email}: {result['message']}")
            return jsonify({
                'error': 'Credenciales inválidas',
                'message': result['message']
            }), 401

    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error inesperado'
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """
    Endpoint para refrescar token JWT.

    Headers requeridos:
    Authorization: Bearer <token_actual>

    Returns:
        JSON con nuevo token o error
    """
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'error': 'Token requerido',
                'message': 'Se requiere header Authorization con Bearer token'
            }), 401

        token = auth_header.split(' ')[1]

        # Validar y refrescar token
        jwt_service = JWTService()
        new_token = jwt_service.refresh_token(token)

        if new_token:
            logger.info("Token refrescado exitosamente")
            return jsonify({
                'access_token': new_token,
                'token_type': 'Bearer',
                'expires_in': current_app.config['JWT_EXPIRATION_HOURS'] * 3600
            }), 200
        else:
            logger.warning("Fallo al refrescar token")
            return jsonify({
                'error': 'Token inválido',
                'message': 'El token no es válido o ha expirado'
            }), 401

    except Exception as e:
        logger.error(f"Error al refrescar token: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error inesperado'
        }), 500


@auth_bp.route('/verify', methods=['GET'])
def verify_token():
    """
    Endpoint para verificar si un token es válido.

    Headers requeridos:
    Authorization: Bearer <token>

    Returns:
        JSON con información del usuario si el token es válido
    """
    try:
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

        if payload:
            logger.info(f"Token verificado para usuario {payload['email']}")
            return jsonify({
                'valid': True,
                'user': {
                    'id': payload['user_id'],
                    'email': payload['email'],
                    'role': payload['role'],
                    'universidad_id': payload.get('universidad_id')
                },
                'expires_at': payload['exp']
            }), 200
        else:
            logger.warning("Token inválido en verificación")
            return jsonify({
                'valid': False,
                'error': 'Token inválido o expirado'
            }), 401

    except Exception as e:
        logger.error(f"Error al verificar token: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error inesperado'
        }), 500


@auth_bp.route('/device/login', methods=['POST'])
def device_login():
    """
    Endpoint para autenticación de dispositivos IoT.

    Body esperado:
    {
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "api_token": "token_del_dispositivo"
    }

    Returns:
        JSON con token de dispositivo o error
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Datos requeridos',
                'message': 'Se requiere body JSON con mac_address y api_token'
            }), 400

        mac_address = data.get('mac_address')
        api_token = data.get('api_token')

        if not mac_address or not api_token:
            return jsonify({
                'error': 'Campos requeridos',
                'message': 'mac_address y api_token son obligatorios'
            }), 400

        # Buscar dispositivo por MAC
        dispositivo_repo = DispositivoRepository()
        dispositivo = dispositivo_repo.find_by_mac(mac_address)

        if not dispositivo:
            logger.warning(f"Dispositivo no encontrado: {mac_address}")
            return jsonify({
                'error': 'Dispositivo no encontrado',
                'message': 'No se encontró un dispositivo con esa dirección MAC'
            }), 404

        # Validar token API
        jwt_service = JWTService()
        if not jwt_service.validate_api_token(dispositivo.api_token_hash, api_token):
            logger.warning(f"Token API inválido para dispositivo {mac_address}")
            return jsonify({
                'error': 'Token inválido',
                'message': 'El token API proporcionado no es válido'
            }), 401

        # Actualizar estado del dispositivo a conectado
        dispositivo_repo.update_estado(dispositivo.id, 'conectado')

        # Generar token JWT para dispositivo
        device_token = jwt_service.create_device_token(dispositivo.id, mac_address)

        logger.info(f"Dispositivo {mac_address} autenticado exitosamente")
        return jsonify({
            'device_token': device_token,
            'token_type': 'Bearer',
            'device': {
                'id': dispositivo.id,
                'mac_address': dispositivo.mac_address,
                'sala_id': dispositivo.sala_id,
                'modelo_id': dispositivo.modelo_id
            },
            'expires_in': 24 * 3600  # 24 horas
        }), 200

    except Exception as e:
        logger.error(f"Error en autenticación de dispositivo: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error inesperado'
        }), 500


# Importar aquí para evitar circular imports
from src.infrastructure.repositories.dispositivo_repository import DispositivoRepository