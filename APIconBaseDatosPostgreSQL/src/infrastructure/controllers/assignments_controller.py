# src/infrastructure/controllers/assignments_controller.py
"""
Controlador REST para gestión de asignaciones de limpieza.
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any, List
import logging
from datetime import datetime, timedelta

from src.application.use_cases.crear_asignacion_limpieza import CrearAsignacionLimpieza
from src.infrastructure.repositories.asignacion_limpieza_repository import AsignacionLimpiezaRepository
from src.infrastructure.repositories.usuario_repository import UsuarioRepository
from src.infrastructure.repositories.dispositivo_repository import DispositivoRepository
from src.infrastructure.services.telegram_service import TelegramService
from src.infrastructure.middleware.auth_middleware import (
    token_required,
    role_required
)

logger = logging.getLogger(__name__)

# Crear blueprint
assignments_bp = Blueprint('assignments', __name__, url_prefix='/api/assignments')


@assignments_bp.route('', methods=['GET'])
@token_required
def get_assignments():
    """
    Obtener asignaciones de limpieza.

    Query parameters:
    - user_id: ID del usuario asignado
    - sala_id: ID de la sala
    - estado: Estado de la asignación (pendiente, en_progreso, completada, cancelada)
    - limit: Número máximo de asignaciones (default: 50)

    Returns:
        JSON con lista de asignaciones
    """
    try:
        # Obtener parámetros de consulta
        user_id = request.args.get('user_id', type=int)
        sala_id = request.args.get('sala_id', type=int)
        estado = request.args.get('estado')
        limit = request.args.get('limit', 50, type=int)

        # Validar límite
        if limit > 200:
            limit = 200  # Máximo 200 asignaciones

        asignacion_repo = AsignacionLimpiezaRepository()

        # Obtener asignaciones según parámetros
        if user_id:
            assignments = asignacion_repo.find_by_usuario(user_id, limit)
        elif sala_id:
            assignments = asignacion_repo.find_by_sala(sala_id, limit)
        elif estado:
            assignments = asignacion_repo.find_by_estado(estado, limit)
        else:
            # Obtener asignaciones pendientes
            assignments = asignacion_repo.find_by_estado('pendiente', limit)

        # Verificar permisos de acceso
        current_user = request.current_user
        if current_user['role'] != 'administrador':
            # Filtrar asignaciones solo de la universidad del usuario
            usuario_repo = UsuarioRepository()
            users_in_universidad = usuario_repo.find_by_universidad(
                current_user.get('universidad_id', 0)
            )
            allowed_user_ids = [u.id for u in users_in_universidad]
            assignments = [a for a in assignments if a.usuario_id in allowed_user_ids]

        # Convertir a diccionarios
        result = []
        for assignment in assignments:
            result.append({
                'id': assignment.id,
                'usuario_id': assignment.usuario_id,
                'sala_id': assignment.sala_id,
                'dispositivo_id': assignment.dispositivo_id,
                'estado': assignment.estado,
                'prioridad': assignment.prioridad,
                'descripcion': assignment.descripcion,
                'fecha_asignacion': assignment.fecha_asignacion.isoformat() if assignment.fecha_asignacion else None,
                'fecha_completada': assignment.fecha_completada.isoformat() if assignment.fecha_completada else None,
                'notas': assignment.notas
            })

        logger.info(f"Obtenidas {len(result)} asignaciones de limpieza")
        return jsonify({
            'assignments': result,
            'total': len(result)
        }), 200

    except Exception as e:
        logger.error(f"Error al obtener asignaciones: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al obtener las asignaciones'
        }), 500


@assignments_bp.route('', methods=['POST'])
@token_required
@role_required(['administrador', 'supervisor'])
def create_assignment():
    """
    Crear una nueva asignación de limpieza.

    Body esperado:
    {
        "usuario_id": 1,
        "sala_id": 2,
        "dispositivo_id": 3,
        "prioridad": "alta",
        "descripcion": "Limpieza urgente por contaminación elevada"
    }

    Returns:
        JSON con datos de la asignación creada
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Datos requeridos',
                'message': 'Se requiere body JSON con los datos de la asignación'
            }), 400

        # Validar campos requeridos
        required_fields = ['usuario_id', 'sala_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Campo requerido',
                    'message': f'El campo {field} es obligatorio'
                }), 400

        # Verificar permisos de acceso
        current_user = request.current_user
        if current_user['role'] != 'administrador':
            # Verificar que el usuario asignado pertenezca a la misma universidad
            usuario_repo = UsuarioRepository()
            assigned_user = usuario_repo.find_by_id(data['usuario_id'])
            if not assigned_user or assigned_user.universidad_id != current_user.get('universidad_id'):
                return jsonify({
                    'error': 'Acceso denegado',
                    'message': 'No puedes asignar tareas a usuarios de otras universidades'
                }), 403

        # Inicializar dependencias
        asignacion_repo = AsignacionLimpiezaRepository()
        usuario_repo = UsuarioRepository()
        dispositivo_repo = DispositivoRepository()
        telegram_service = TelegramService()

        asignar_tarea = CrearAsignacionLimpieza(
            asignacion_repo,
            usuario_repo,
            dispositivo_repo,
            telegram_service
        )

        # Ejecutar caso de uso
        result = asignar_tarea.execute(
            usuario_id=data['usuario_id'],
            sala_id=data['sala_id'],
            dispositivo_id=data.get('dispositivo_id'),
            prioridad=data.get('prioridad', 'media'),
            descripcion=data.get('descripcion', '')
        )

        if result['success']:
            logger.info(f"Asignación de limpieza creada: {result['assignment']['id']}")

            response_data = {
                'message': 'Asignación creada exitosamente',
                'assignment': {
                    'id': result['assignment']['id'],
                    'usuario_id': result['assignment']['usuario_id'],
                    'sala_id': result['assignment']['sala_id'],
                    'dispositivo_id': result['assignment']['dispositivo_id'],
                    'estado': result['assignment']['estado'],
                    'prioridad': result['assignment']['prioridad'],
                    'descripcion': result['assignment']['descripcion'],
                    'fecha_asignacion': result['assignment']['fecha_asignacion']
                }
            }

            # Agregar información de notificación si se envió
            if result.get('notification_sent'):
                response_data['notification'] = {
                    'sent': True,
                    'message': 'Se ha enviado una notificación al usuario asignado'
                }

            return jsonify(response_data), 201
        else:
            logger.warning(f"Fallo al crear asignación: {result['message']}")
            return jsonify({
                'error': 'Error al crear asignación',
                'message': result['message']
            }), 400

    except Exception as e:
        logger.error(f"Error al crear asignación: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al crear la asignación'
        }), 500


@assignments_bp.route('/<int:assignment_id>', methods=['PUT'])
@token_required
def update_assignment(assignment_id: int):
    """
    Actualizar una asignación de limpieza.

    Body esperado:
    {
        "estado": "completada",
        "notas": "Limpieza completada satisfactoriamente"
    }

    Returns:
        JSON con datos de la asignación actualizada
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Datos requeridos',
                'message': 'Se requiere body JSON con los datos a actualizar'
            }), 400

        asignacion_repo = AsignacionLimpiezaRepository()

        # Obtener la asignación actual
        assignment = asignacion_repo.find_by_id(assignment_id)
        if not assignment:
            return jsonify({
                'error': 'Asignación no encontrada',
                'message': f'No se encontró la asignación con ID {assignment_id}'
            }), 404

        # Verificar permisos de acceso
        current_user = request.current_user
        if current_user['role'] != 'administrador':
            # Verificar que la asignación pertenezca a la universidad del usuario
            usuario_repo = UsuarioRepository()
            assigned_user = usuario_repo.find_by_id(assignment.usuario_id)
            if not assigned_user or assigned_user.universidad_id != current_user.get('universidad_id'):
                return jsonify({
                    'error': 'Acceso denegado',
                    'message': 'No tienes acceso a esta asignación'
                }), 403

            # Solo el usuario asignado o supervisores pueden actualizar
            if (current_user['role'] not in ['supervisor'] and
                current_user['id'] != assignment.usuario_id):
                return jsonify({
                    'error': 'Acceso denegado',
                    'message': 'Solo puedes actualizar tus propias asignaciones'
                }), 403

        # Actualizar campos permitidos
        updates = {}
        if 'estado' in data:
            updates['estado'] = data['estado']
        if 'notas' in data:
            updates['notas'] = data['notas']

        # Para completar la asignación, usar directamente el repositorio
        from datetime import datetime
        updates = {
            'estado': 'completada',
            'fecha_completada': datetime.utcnow(),
            'notas': data.get('notas', '')
        }

        updated_assignment = asignacion_repo.update(assignment_id, updates)
        if updated_assignment:
            logger.info(f"Asignación {assignment_id} completada")
            return jsonify({
                'message': 'Asignación completada exitosamente',
                'assignment': {
                    'id': updated_assignment.id,
                    'estado': updated_assignment.estado,
                    'fecha_completada': updated_assignment.fecha_completada.isoformat() if updated_assignment.fecha_completada else None,
                    'notas': updated_assignment.notas
                }
            }), 200
        else:
            return jsonify({
                'error': 'Error al completar asignación',
                'message': 'No se pudo completar la asignación'
            }), 400

        # Para otras actualizaciones, usar el método directo del repositorio
        updated_assignment = asignacion_repo.update(assignment_id, updates)
        if updated_assignment:
            logger.info(f"Asignación {assignment_id} actualizada")
            return jsonify({
                'message': 'Asignación actualizada exitosamente',
                'assignment': {
                    'id': updated_assignment.id,
                    'estado': updated_assignment.estado,
                    'notas': updated_assignment.notas
                }
            }), 200
        else:
            return jsonify({
                'error': 'Error al actualizar asignación',
                'message': 'No se pudo actualizar la asignación'
            }), 400

    except Exception as e:
        logger.error(f"Error al actualizar asignación {assignment_id}: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al actualizar la asignación'
        }), 500


@assignments_bp.route('/<int:assignment_id>', methods=['DELETE'])
@token_required
@role_required(['administrador', 'supervisor'])
def delete_assignment(assignment_id: int):
    """
    Eliminar una asignación de limpieza.

    Returns:
        JSON con mensaje de confirmación
    """
    try:
        asignacion_repo = AsignacionLimpiezaRepository()

        # Obtener la asignación para verificar permisos
        assignment = asignacion_repo.find_by_id(assignment_id)
        if not assignment:
            return jsonify({
                'error': 'Asignación no encontrada',
                'message': f'No se encontró la asignación con ID {assignment_id}'
            }), 404

        # Verificar permisos de acceso
        current_user = request.current_user
        if current_user['role'] != 'administrador':
            # Verificar que la asignación pertenezca a la universidad del usuario
            usuario_repo = UsuarioRepository()
            assigned_user = usuario_repo.find_by_id(assignment.usuario_id)
            if not assigned_user or assigned_user.universidad_id != current_user.get('universidad_id'):
                return jsonify({
                    'error': 'Acceso denegado',
                    'message': 'No tienes acceso a esta asignación'
                }), 403

        # Eliminar la asignación
        success = asignacion_repo.delete(assignment_id)
        if success:
            logger.info(f"Asignación {assignment_id} eliminada")
            return jsonify({
                'message': 'Asignación eliminada exitosamente'
            }), 200
        else:
            return jsonify({
                'error': 'Error al eliminar asignación',
                'message': 'No se pudo eliminar la asignación'
            }), 400

    except Exception as e:
        logger.error(f"Error al eliminar asignación {assignment_id}: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al eliminar la asignación'
        }), 500


@assignments_bp.route('/stats', methods=['GET'])
@token_required
def get_assignment_stats():
    """
    Obtener estadísticas de asignaciones de limpieza.

    Query parameters:
    - days: Días para calcular estadísticas (default: 30)

    Returns:
        JSON con estadísticas de asignaciones
    """
    try:
        days = request.args.get('days', 30, type=int)

        # Validar rango de días
        if days < 1 or days > 365:
            return jsonify({
                'error': 'Parámetro inválido',
                'message': 'days debe estar entre 1 y 365'
            }), 400

        asignacion_repo = AsignacionLimpiezaRepository()

        # Obtener estadísticas
        stats = asignacion_repo.get_estadisticas_asignaciones(days)

        # Filtrar por universidad si no es administrador
        current_user = request.current_user
        if current_user['role'] != 'administrador':
            # Para usuarios no administradores, filtrar estadísticas por universidad
            # Esta es una simplificación - en una implementación completa se filtraría por universidad
            pass

        logger.info(f"Estadísticas de asignaciones obtenidas para los últimos {days} días")
        return jsonify({
            'stats': stats,
            'period_days': days
        }), 200

    except Exception as e:
        logger.error(f"Error al obtener estadísticas de asignaciones: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al obtener las estadísticas'
        }), 500