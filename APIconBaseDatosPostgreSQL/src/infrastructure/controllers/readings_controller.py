# src/infrastructure/controllers/readings_controller.py
"""
Controlador REST para gestión de lecturas de sensores.
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any, List
import logging
from datetime import datetime, timedelta

from src.application.use_cases.registrar_lectura_aire import RegistrarLecturaAire
from src.infrastructure.repositories.lectura_calidad_aire_repository import LecturaCalidadAireRepository
from src.infrastructure.repositories.dispositivo_repository import DispositivoRepository
from src.infrastructure.services.telegram_service import TelegramService
from src.infrastructure.middleware.auth_middleware import (
    token_required,
    device_token_required,
    role_required
)

logger = logging.getLogger(__name__)

# Crear blueprint
readings_bp = Blueprint('readings', __name__, url_prefix='/api/readings')


@readings_bp.route('/air-quality', methods=['GET'])
@token_required
def get_air_quality_readings():
    """
    Obtener lecturas de calidad del aire.

    Query parameters:
    - device_id: ID del dispositivo
    - sala_id: ID de la sala
    - limit: Número máximo de lecturas (default: 100)
    - fecha_inicio: Fecha de inicio (ISO format)
    - fecha_fin: Fecha de fin (ISO format)

    Returns:
        JSON con lista de lecturas
    """
    try:
        # Obtener parámetros de consulta
        device_id = request.args.get('device_id', type=int)
        sala_id = request.args.get('sala_id', type=int)
        limit = request.args.get('limit', 100, type=int)
        fecha_inicio_str = request.args.get('fecha_inicio')
        fecha_fin_str = request.args.get('fecha_fin')

        # Validar límite
        if limit > 1000:
            limit = 1000  # Máximo 1000 lecturas

        lectura_repo = LecturaCalidadAireRepository()

        # Convertir fechas si se proporcionan
        fecha_inicio = None
        fecha_fin = None
        if fecha_inicio_str:
            fecha_inicio = datetime.fromisoformat(fecha_inicio_str.replace('Z', '+00:00'))
        if fecha_fin_str:
            fecha_fin = datetime.fromisoformat(fecha_fin_str.replace('Z', '+00:00'))

        # Obtener lecturas según parámetros
        if device_id and fecha_inicio and fecha_fin:
            readings = lectura_repo.find_by_rango_fechas(device_id, fecha_inicio, fecha_fin)
        elif device_id:
            readings = lectura_repo.find_by_dispositivo(device_id, limit)
        elif sala_id:
            readings = lectura_repo.find_by_sala(sala_id, limit)
        else:
            # Obtener lecturas problemáticas de las últimas 24 horas
            readings = lectura_repo.get_lecturas_problematicas(24)

        # Verificar permisos de acceso
        current_user = request.current_user
        if current_user['role'] != 'administrador':
            # Filtrar lecturas solo de la universidad del usuario
            dispositivo_repo = DispositivoRepository()
            devices_in_universidad = dispositivo_repo.find_by_universidad(
                current_user.get('universidad_id', 0)
            )
            allowed_device_ids = [d.id for d in devices_in_universidad]
            readings = [r for r in readings if r.dispositivo_id in allowed_device_ids]

        # Convertir a diccionarios
        result = []
        for reading in readings:
            result.append({
                'id': reading.id,
                'dispositivo_id': reading.dispositivo_id,
                'valor_pm1': reading.valor_pm1,
                'valor_pm2_5': reading.valor_pm2_5,
                'valor_pm10': reading.valor_pm10,
                'etiqueta': reading.etiqueta,
                'fecha_lectura': reading.fecha_lectura.isoformat() if reading.fecha_lectura else None
            })

        logger.info(f"Obtenidas {len(result)} lecturas de calidad del aire")
        return jsonify({
            'readings': result,
            'total': len(result)
        }), 200

    except Exception as e:
        logger.error(f"Error al obtener lecturas de calidad del aire: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al obtener las lecturas'
        }), 500


@readings_bp.route('/air-quality', methods=['POST'])
@device_token_required
def create_air_quality_reading():
    """
    Registrar una nueva lectura de calidad del aire desde un dispositivo.

    Headers requeridos:
    Authorization: Bearer <device_token>

    Body esperado:
    {
        "pm1": 15.2,
        "pm2_5": 25.8,
        "pm10": 35.4,
        "etiqueta": "ambiente"
    }

    Returns:
        JSON con datos de la lectura creada
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Datos requeridos',
                'message': 'Se requiere body JSON con los valores de calidad del aire'
            }), 400

        # Validar que al menos uno de los valores PM esté presente
        pm_values = ['pm1', 'pm2_5', 'pm10']
        if not any(key in data for key in pm_values):
            return jsonify({
                'error': 'Datos insuficientes',
                'message': 'Se requiere al menos uno de: pm1, pm2_5, pm10'
            }), 400

        # Obtener información del dispositivo del token
        device_info = request.current_device
        device_id = device_info['id']

        # Inicializar dependencias
        lectura_repo = LecturaCalidadAireRepository()
        dispositivo_repo = DispositivoRepository()
        telegram_service = TelegramService()

        registrar_lectura = RegistrarLecturaAire(
            lectura_repo,
            dispositivo_repo,
            telegram_service
        )

        # Ejecutar caso de uso
        result = registrar_lectura.execute(
            dispositivo_id=device_id,
            valor_pm1=data.get('pm1'),
            valor_pm2_5=data.get('pm2_5'),
            valor_pm10=data.get('pm10'),
            etiqueta=data.get('etiqueta', 'ambiente')
        )

        if result['success']:
            logger.info(f"Lectura de calidad del aire registrada para dispositivo {device_id}")

            response_data = {
                'message': 'Lectura registrada exitosamente',
                'reading': {
                    'id': result['reading']['id'],
                    'dispositivo_id': result['reading']['dispositivo_id'],
                    'valor_pm1': result['reading']['valor_pm1'],
                    'valor_pm2_5': result['reading']['valor_pm2_5'],
                    'valor_pm10': result['reading']['valor_pm10'],
                    'etiqueta': result['reading']['etiqueta'],
                    'fecha_lectura': result['reading']['fecha_lectura']
                }
            }

            # Agregar información de alerta si se generó
            if result.get('alert_triggered'):
                response_data['alert'] = {
                    'triggered': True,
                    'level': result.get('alert_level'),
                    'message': 'Se ha enviado una alerta por calidad del aire deficiente'
                }

            return jsonify(response_data), 201
        else:
            logger.warning(f"Fallo al registrar lectura para dispositivo {device_id}: {result['message']}")
            return jsonify({
                'error': 'Error al registrar lectura',
                'message': result['message']
            }), 400

    except Exception as e:
        logger.error(f"Error al registrar lectura de calidad del aire: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al registrar la lectura'
        }), 500


@readings_bp.route('/air-quality/stats', methods=['GET'])
@token_required
def get_air_quality_stats():
    """
    Obtener estadísticas de calidad del aire.

    Query parameters:
    - device_id: ID del dispositivo (requerido)
    - hours: Horas para calcular estadísticas (default: 24)

    Returns:
        JSON con estadísticas de calidad del aire
    """
    try:
        device_id = request.args.get('device_id', type=int)
        hours = request.args.get('hours', 24, type=int)

        if not device_id:
            return jsonify({
                'error': 'Parámetro requerido',
                'message': 'Se requiere el parámetro device_id'
            }), 400

        # Validar rango de horas
        if hours < 1 or hours > 168:  # Máximo 1 semana
            return jsonify({
                'error': 'Parámetro inválido',
                'message': 'hours debe estar entre 1 y 168'
            }), 400

        # Verificar permisos de acceso al dispositivo
        current_user = request.current_user
        if current_user['role'] != 'administrador':
            dispositivo_repo = DispositivoRepository()
            devices_in_universidad = dispositivo_repo.find_by_universidad(
                current_user.get('universidad_id', 0)
            )
            device_ids_in_universidad = [d.id for d in devices_in_universidad]

            if device_id not in device_ids_in_universidad:
                return jsonify({
                    'error': 'Acceso denegado',
                    'message': 'No tienes acceso a este dispositivo'
                }), 403

        lectura_repo = LecturaCalidadAireRepository()
        stats = lectura_repo.get_promedio_calidad_aire(device_id, hours)

        if stats:
            logger.info(f"Estadísticas obtenidas para dispositivo {device_id}")
            return jsonify({
                'device_id': device_id,
                'stats': stats
            }), 200
        else:
            return jsonify({
                'error': 'Sin datos',
                'message': f'No hay suficientes datos para el dispositivo {device_id} en las últimas {hours} horas'
            }), 404

    except Exception as e:
        logger.error(f"Error al obtener estadísticas de calidad del aire: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al obtener las estadísticas'
        }), 500


@readings_bp.route('/temperature', methods=['GET'])
@token_required
def get_temperature_readings():
    """
    Obtener lecturas de temperatura.

    Query parameters:
    - device_id: ID del dispositivo
    - limit: Número máximo de lecturas (default: 100)

    Returns:
        JSON con lista de lecturas de temperatura
    """
    try:
        device_id = request.args.get('device_id', type=int)
        limit = request.args.get('limit', 100, type=int)

        if not device_id:
            return jsonify({
                'error': 'Parámetro requerido',
                'message': 'Se requiere el parámetro device_id'
            }), 400

        # Validar límite
        if limit > 1000:
            limit = 1000

        # Verificar permisos de acceso
        current_user = request.current_user
        if current_user['role'] != 'administrador':
            dispositivo_repo = DispositivoRepository()
            devices_in_universidad = dispositivo_repo.find_by_universidad(
                current_user.get('universidad_id', 0)
            )
            device_ids_in_universidad = [d.id for d in devices_in_universidad]

            if device_id not in device_ids_in_universidad:
                return jsonify({
                    'error': 'Acceso denegado',
                    'message': 'No tienes acceso a este dispositivo'
                }), 403

        # Para esta implementación simplificada, retornamos datos simulados
        # En una implementación completa, se usaría LecturaTemperaturaRepository
        logger.info(f"Solicitud de lecturas de temperatura para dispositivo {device_id}")

        return jsonify({
            'message': 'Endpoint de temperatura - Implementación pendiente',
            'device_id': device_id,
            'limit': limit
        }), 200

    except Exception as e:
        logger.error(f"Error al obtener lecturas de temperatura: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al obtener las lecturas de temperatura'
        }), 500


@readings_bp.route('/humidity', methods=['GET'])
@token_required
def get_humidity_readings():
    """
    Obtener lecturas de humedad.

    Query parameters:
    - device_id: ID del dispositivo
    - limit: Número máximo de lecturas (default: 100)

    Returns:
        JSON con lista de lecturas de humedad
    """
    try:
        device_id = request.args.get('device_id', type=int)
        limit = request.args.get('limit', 100, type=int)

        if not device_id:
            return jsonify({
                'error': 'Parámetro requerido',
                'message': 'Se requiere el parámetro device_id'
            }), 400

        # Validar límite
        if limit > 1000:
            limit = 1000

        # Verificar permisos de acceso
        current_user = request.current_user
        if current_user['role'] != 'administrador':
            dispositivo_repo = DispositivoRepository()
            devices_in_universidad = dispositivo_repo.find_by_universidad(
                current_user.get('universidad_id', 0)
            )
            device_ids_in_universidad = [d.id for d in devices_in_universidad]

            if device_id not in device_ids_in_universidad:
                return jsonify({
                    'error': 'Acceso denegado',
                    'message': 'No tienes acceso a este dispositivo'
                }), 403

        # Para esta implementación simplificada, retornamos datos simulados
        # En una implementación completa, se usaría LecturaHumedadRepository
        logger.info(f"Solicitud de lecturas de humedad para dispositivo {device_id}")

        return jsonify({
            'message': 'Endpoint de humedad - Implementación pendiente',
            'device_id': device_id,
            'limit': limit
        }), 200

    except Exception as e:
        logger.error(f"Error al obtener lecturas de humedad: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al obtener las lecturas de humedad'
        }), 500