# src/infrastructure/controllers/devices_controller.py
"""
Controlador REST para gestión de dispositivos IoT.
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any, List
import logging

from src.application.use_cases.registrar_dispositivo import RegistrarDispositivo
from src.infrastructure.repositories.dispositivo_repository import DispositivoRepository
from src.infrastructure.repositories.usuario_repository import UsuarioRepository
from src.infrastructure.services.jwt_service import JWTService
from src.infrastructure.middleware.auth_middleware import (
    token_required,
    role_required,
    device_token_required,
    universidad_required
)

logger = logging.getLogger(__name__)

# Crear blueprint
devices_bp = Blueprint('devices', __name__, url_prefix='/api/devices')


@devices_bp.route('', methods=['GET'])
@token_required
def get_devices():
    """
    Obtener lista de dispositivos.

    Query parameters:
    - sala_id: Filtrar por sala
    - universidad_id: Filtrar por universidad
    - estado: Filtrar por estado ('conectado', 'desconectado')

    Returns:
        JSON con lista de dispositivos
    """
    try:
        # Obtener parámetros de consulta
        sala_id = request.args.get('sala_id', type=int)
        universidad_id = request.args.get('universidad_id', type=int)
        estado = request.args.get('estado')

        dispositivo_repo = DispositivoRepository()

        # Aplicar filtros según permisos del usuario
        current_user = request.current_user
        user_role = current_user['role']

        if sala_id:
            devices = dispositivo_repo.find_by_sala(sala_id)
        elif universidad_id:
            # Verificar permisos para acceder a universidad
            if (user_role != 'administrador' and
                current_user.get('universidad_id') != universidad_id):
                return jsonify({
                    'error': 'Acceso denegado',
                    'message': f'No tienes acceso a dispositivos de la universidad {universidad_id}'
                }), 403
            devices = dispositivo_repo.find_by_universidad(universidad_id)
        else:
            # Si no hay filtros específicos, obtener todos (solo para admin)
            if user_role == 'administrador':
                devices = dispositivo_repo.get_all()
            else:
                # Para otros roles, solo dispositivos de su universidad
                user_universidad_id = current_user.get('universidad_id')
                if user_universidad_id:
                    devices = dispositivo_repo.find_by_universidad(user_universidad_id)
                else:
                    devices = []

        # Filtrar por estado si se especifica
        if estado:
            devices = [d for d in devices if d.estado == estado]

        # Convertir a diccionarios
        result = []
        for device in devices:
            result.append({
                'id': device.id,
                'sala_id': device.sala_id,
                'modelo_id': device.modelo_id,
                'mac_address': device.mac_address,
                'fecha_instalacion': device.fecha_instalacion.isoformat() if device.fecha_instalacion else None,
                'ultimo_mantenimiento': device.ultimo_mantenimiento.isoformat() if device.ultimo_mantenimiento else None,
                'estado': device.estado,
                'ultima_vez_visto': device.ultima_vez_visto.isoformat() if device.ultima_vez_visto else None
            })

        logger.info(f"Obtenidos {len(result)} dispositivos")
        return jsonify({
            'devices': result,
            'total': len(result)
        }), 200

    except Exception as e:
        logger.error(f"Error al obtener dispositivos: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al obtener los dispositivos'
        }), 500


@devices_bp.route('/<int:device_id>', methods=['GET'])
@token_required
def get_device(device_id: int):
    """
    Obtener un dispositivo específico por ID.

    Args:
        device_id: ID del dispositivo

    Returns:
        JSON con datos del dispositivo
    """
    try:
        dispositivo_repo = DispositivoRepository()
        device = dispositivo_repo.find_by_id(device_id)

        if not device:
            return jsonify({
                'error': 'Dispositivo no encontrado',
                'message': f'No se encontró un dispositivo con ID {device_id}'
            }), 404

        # Verificar permisos de acceso
        current_user = request.current_user
        if current_user['role'] != 'administrador':
            # Verificar que el dispositivo pertenezca a la universidad del usuario
            # Esto requiere una consulta adicional para obtener la universidad del dispositivo
            devices_in_user_universidad = dispositivo_repo.find_by_universidad(
                current_user.get('universidad_id', 0)
            )
            device_ids_in_universidad = [d.id for d in devices_in_user_universidad]

            if device_id not in device_ids_in_universidad:
                return jsonify({
                    'error': 'Acceso denegado',
                    'message': 'No tienes acceso a este dispositivo'
                }), 403

        result = {
            'id': device.id,
            'sala_id': device.sala_id,
            'modelo_id': device.modelo_id,
            'mac_address': device.mac_address,
            'fecha_instalacion': device.fecha_instalacion.isoformat() if device.fecha_instalacion else None,
            'ultimo_mantenimiento': device.ultimo_mantenimiento.isoformat() if device.ultimo_mantenimiento else None,
            'estado': device.estado,
            'ultima_vez_visto': device.ultima_vez_visto.isoformat() if device.ultima_vez_visto else None
        }

        logger.info(f"Dispositivo {device_id} obtenido exitosamente")
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error al obtener dispositivo {device_id}: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al obtener el dispositivo'
        }), 500


@devices_bp.route('', methods=['POST'])
@token_required
@role_required(['administrador', 'operador'])
def create_device():
    """
    Registrar un nuevo dispositivo.

    Body esperado:
    {
        "sala_id": 1,
        "modelo_id": 1,
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "fecha_instalacion": "2024-01-15"
    }

    Returns:
        JSON con datos del dispositivo creado
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Datos requeridos',
                'message': 'Se requiere body JSON con los datos del dispositivo'
            }), 400

        # Validar campos requeridos
        required_fields = ['sala_id', 'modelo_id', 'mac_address']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Campo requerido',
                    'message': f'El campo {field} es obligatorio'
                }), 400

        # Verificar permisos: operadores solo pueden registrar en su universidad
        current_user = request.current_user
        if current_user['role'] == 'operador':
            # Aquí se debería verificar que la sala pertenezca a la universidad del operador
            # Por simplicidad, asumimos que la validación se hace en el caso de uso
            pass

        # Inicializar dependencias
        dispositivo_repo = DispositivoRepository()
        usuario_repo = UsuarioRepository()
        jwt_service = JWTService()
        registrar_dispositivo = RegistrarDispositivo(dispositivo_repo, usuario_repo, jwt_service)

        # Ejecutar caso de uso
        result = registrar_dispositivo.execute(
            sala_id=data['sala_id'],
            modelo_id=data['modelo_id'],
            mac_address=data['mac_address'],
            fecha_instalacion=data.get('fecha_instalacion'),
            registrado_por_usuario_id=current_user['id']
        )

        if result['success']:
            logger.info(f"Dispositivo {data['mac_address']} registrado exitosamente")
            return jsonify({
                'message': 'Dispositivo registrado exitosamente',
                'device': {
                    'id': result['device']['id'],
                    'sala_id': result['device']['sala_id'],
                    'modelo_id': result['device']['modelo_id'],
                    'mac_address': result['device']['mac_address'],
                    'api_token': result['api_token'],
                    'estado': result['device']['estado']
                }
            }), 201
        else:
            logger.warning(f"Fallo al registrar dispositivo {data['mac_address']}: {result['message']}")
            return jsonify({
                'error': 'Error al registrar dispositivo',
                'message': result['message']
            }), 400

    except Exception as e:
        logger.error(f"Error al registrar dispositivo: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al registrar el dispositivo'
        }), 500


@devices_bp.route('/<int:device_id>', methods=['PUT'])
@token_required
@role_required(['administrador', 'operador'])
def update_device(device_id: int):
    """
    Actualizar un dispositivo existente.

    Args:
        device_id: ID del dispositivo a actualizar

    Body esperado:
    {
        "sala_id": 2,
        "modelo_id": 1,
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "estado": "conectado",
        "ultimo_mantenimiento": "2024-01-20"
    }

    Returns:
        JSON con datos del dispositivo actualizado
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Datos requeridos',
                'message': 'Se requiere body JSON con los datos a actualizar'
            }), 400

        dispositivo_repo = DispositivoRepository()
        device = dispositivo_repo.find_by_id(device_id)

        if not device:
            return jsonify({
                'error': 'Dispositivo no encontrado',
                'message': f'No se encontró un dispositivo con ID {device_id}'
            }), 404

        # Verificar permisos de acceso
        current_user = request.current_user
        if current_user['role'] != 'administrador':
            # Verificar que el dispositivo pertenezca a la universidad del usuario
            devices_in_user_universidad = dispositivo_repo.find_by_universidad(
                current_user.get('universidad_id', 0)
            )
            device_ids_in_universidad = [d.id for d in devices_in_user_universidad]

            if device_id not in device_ids_in_universidad:
                return jsonify({
                    'error': 'Acceso denegado',
                    'message': 'No tienes acceso a este dispositivo'
                }), 403

        # Actualizar campos permitidos
        if 'sala_id' in data:
            device.sala_id = data['sala_id']
        if 'modelo_id' in data:
            device.modelo_id = data['modelo_id']
        if 'mac_address' in data:
            device.mac_address = data['mac_address']
        if 'fecha_instalacion' in data:
            from datetime import datetime
            device.fecha_instalacion = datetime.fromisoformat(data['fecha_instalacion'])
        if 'ultimo_mantenimiento' in data:
            from datetime import datetime
            device.ultimo_mantenimiento = datetime.fromisoformat(data['ultimo_mantenimiento'])
        if 'estado' in data:
            if data['estado'] not in ['conectado', 'desconectado']:
                return jsonify({
                    'error': 'Estado inválido',
                    'message': 'El estado debe ser "conectado" o "desconectado"'
                }), 400
            device.estado = data['estado']

        updated_device = dispositivo_repo.update(device)

        result = {
            'id': updated_device.id,
            'sala_id': updated_device.sala_id,
            'modelo_id': updated_device.modelo_id,
            'mac_address': updated_device.mac_address,
            'fecha_instalacion': updated_device.fecha_instalacion.isoformat() if updated_device.fecha_instalacion else None,
            'ultimo_mantenimiento': updated_device.ultimo_mantenimiento.isoformat() if updated_device.ultimo_mantenimiento else None,
            'estado': updated_device.estado,
            'ultima_vez_visto': updated_device.ultima_vez_visto.isoformat() if updated_device.ultima_vez_visto else None
        }

        logger.info(f"Dispositivo {device_id} actualizado exitosamente")
        return jsonify({
            'message': 'Dispositivo actualizado exitosamente',
            'device': result
        }), 200

    except ValueError as e:
        logger.warning(f"Error de validación al actualizar dispositivo {device_id}: {str(e)}")
        return jsonify({
            'error': 'Error de validación',
            'message': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error al actualizar dispositivo {device_id}: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al actualizar el dispositivo'
        }), 500


@devices_bp.route('/<int:device_id>', methods=['DELETE'])
@token_required
@role_required(['administrador'])
def delete_device(device_id: int):
    """
    Eliminar un dispositivo.

    Args:
        device_id: ID del dispositivo a eliminar

    Returns:
        JSON con mensaje de confirmación
    """
    try:
        dispositivo_repo = DispositivoRepository()
        device = dispositivo_repo.find_by_id(device_id)

        if not device:
            return jsonify({
                'error': 'Dispositivo no encontrado',
                'message': f'No se encontró un dispositivo con ID {device_id}'
            }), 404

        success = dispositivo_repo.delete(device_id)

        if success:
            logger.info(f"Dispositivo {device_id} eliminado exitosamente")
            return jsonify({
                'message': 'Dispositivo eliminado exitosamente'
            }), 200
        else:
            return jsonify({
                'error': 'Dispositivo no encontrado',
                'message': f'No se pudo eliminar el dispositivo con ID {device_id}'
            }), 404

    except ValueError as e:
        logger.warning(f"Error de validación al eliminar dispositivo {device_id}: {str(e)}")
        return jsonify({
            'error': 'Error de validación',
            'message': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error al eliminar dispositivo {device_id}: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al eliminar el dispositivo'
        }), 500


@devices_bp.route('/register', methods=['POST'])
@device_token_required
def device_register():
    """
    Endpoint especial para que dispositivos se registren automáticamente.

    Headers requeridos:
    Authorization: Bearer <device_token>

    Body esperado:
    {
        "ubicacion": "Sala 101, Edificio Ingeniería"
    }

    Returns:
        JSON con confirmación de registro
    """
    try:
        # El middleware device_token_required ya validó el token y agregó current_device
        device_info = request.current_device

        # Aquí se podría implementar lógica adicional para registro automático
        # Por ahora, solo confirmamos que el dispositivo está autorizado

        logger.info(f"Dispositivo {device_info['mac_address']} se registró exitosamente")

        return jsonify({
            'message': 'Dispositivo registrado exitosamente',
            'device_id': device_info['id'],
            'mac_address': device_info['mac_address'],
            'status': 'authorized'
        }), 200

    except Exception as e:
        logger.error(f"Error en registro de dispositivo: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error en el registro del dispositivo'
        }), 500