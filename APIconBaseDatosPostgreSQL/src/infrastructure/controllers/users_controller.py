# src/infrastructure/controllers/users_controller.py
"""
Controlador REST para gestión de usuarios.
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any, List
import logging

from src.application.use_cases.registrar_usuario import RegistrarUsuario
from src.infrastructure.repositories.usuario_repository import UsuarioRepository
from src.infrastructure.services.jwt_service import JWTService
from src.infrastructure.middleware.auth_middleware import token_required, role_required

logger = logging.getLogger(__name__)

# Crear blueprint
users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('', methods=['GET'])
@token_required
@role_required(['administrador', 'operador'])
def get_users():
    """
    Obtener lista de usuarios.

    Query parameters:
    - universidad_id: Filtrar por universidad
    - rol: Filtrar por rol

    Returns:
        JSON con lista de usuarios
    """
    try:
        # Obtener parámetros de consulta
        universidad_id = request.args.get('universidad_id', type=int)
        rol = request.args.get('rol')

        usuario_repo = UsuarioRepository()
        users = usuario_repo.get_all()

        # Aplicar filtros
        if universidad_id:
            users = [u for u in users if u.universidad_id == universidad_id]
        if rol:
            users = [u for u in users if usuario_repo.find_by_id(u.id) and
                    usuario_repo.find_by_id(u.id).rol.nombre == rol]

        # Convertir a diccionarios (sin contraseña)
        result = []
        for user in users:
            result.append({
                'id': user.id,
                'email': user.email,
                'nombre_completo': user.nombre_completo,
                'rol_id': user.rol_id,
                'universidad_id': user.universidad_id,
                'campus_id': user.campus_id,
                'fecha_creacion': user.fecha_creacion.isoformat() if user.fecha_creacion else None
            })

        logger.info(f"Obtenidos {len(result)} usuarios")
        return jsonify({
            'users': result,
            'total': len(result)
        }), 200

    except Exception as e:
        logger.error(f"Error al obtener usuarios: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al obtener los usuarios'
        }), 500


@users_bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id: int):
    """
    Obtener un usuario específico por ID.

    Args:
        user_id: ID del usuario

    Returns:
        JSON con datos del usuario
    """
    try:
        usuario_repo = UsuarioRepository()
        user = usuario_repo.find_by_id(user_id)

        if not user:
            return jsonify({
                'error': 'Usuario no encontrado',
                'message': f'No se encontró un usuario con ID {user_id}'
            }), 404

        # Verificar permisos: solo admin puede ver otros usuarios,
        # operadores pueden ver usuarios de su universidad
        current_user = request.current_user
        if (current_user['role'] != 'administrador' and
            current_user['id'] != user_id and
            (current_user['role'] != 'operador' or
             current_user.get('universidad_id') != user.universidad_id)):
            return jsonify({
                'error': 'Acceso denegado',
                'message': 'No tienes permisos para ver este usuario'
            }), 403

        result = {
            'id': user.id,
            'email': user.email,
            'nombre_completo': user.nombre_completo,
            'rol_id': user.rol_id,
            'universidad_id': user.universidad_id,
            'campus_id': user.campus_id,
            'fecha_creacion': user.fecha_creacion.isoformat() if user.fecha_creacion else None
        }

        logger.info(f"Usuario {user_id} obtenido exitosamente")
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error al obtener usuario {user_id}: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al obtener el usuario'
        }), 500


@users_bp.route('', methods=['POST'])
@token_required
@role_required(['administrador'])
def create_user():
    """
    Crear un nuevo usuario.

    Body esperado:
    {
        "email": "usuario@ejemplo.com",
        "password": "contraseña",
        "nombre_completo": "Nombre Completo",
        "rol_id": 1,
        "universidad_id": 1,
        "campus_id": 1
    }

    Returns:
        JSON con datos del usuario creado
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Datos requeridos',
                'message': 'Se requiere body JSON con los datos del usuario'
            }), 400

        # Validar campos requeridos
        required_fields = ['email', 'password', 'nombre_completo', 'rol_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Campo requerido',
                    'message': f'El campo {field} es obligatorio'
                }), 400

        # Inicializar dependencias
        usuario_repo = UsuarioRepository()
        jwt_service = JWTService()
        registrar_usuario = RegistrarUsuario(usuario_repo, jwt_service)

        # Ejecutar caso de uso
        result = registrar_usuario.execute(
            email=data['email'],
            password=data['password'],
            nombre_completo=data['nombre_completo'],
            rol_id=data['rol_id'],
            universidad_id=data.get('universidad_id'),
            campus_id=data.get('campus_id')
        )

        if result['success']:
            logger.info(f"Usuario {data['email']} creado exitosamente")
            return jsonify({
                'message': 'Usuario creado exitosamente',
                'user': {
                    'id': result['user']['id'],
                    'email': result['user']['email'],
                    'nombre_completo': result['user']['nombre_completo'],
                    'rol_id': result['user']['rol_id'],
                    'universidad_id': result['user']['universidad_id'],
                    'campus_id': result['user']['campus_id']
                }
            }), 201
        else:
            logger.warning(f"Fallo al crear usuario {data['email']}: {result['message']}")
            return jsonify({
                'error': 'Error al crear usuario',
                'message': result['message']
            }), 400

    except Exception as e:
        logger.error(f"Error al crear usuario: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al crear el usuario'
        }), 500


@users_bp.route('/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id: int):
    """
    Actualizar un usuario existente.

    Args:
        user_id: ID del usuario a actualizar

    Body esperado:
    {
        "email": "nuevo@ejemplo.com",
        "nombre_completo": "Nuevo Nombre",
        "rol_id": 2,
        "universidad_id": 1,
        "campus_id": 1
    }

    Returns:
        JSON con datos del usuario actualizado
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Datos requeridos',
                'message': 'Se requiere body JSON con los datos a actualizar'
            }), 400

        usuario_repo = UsuarioRepository()
        user = usuario_repo.find_by_id(user_id)

        if not user:
            return jsonify({
                'error': 'Usuario no encontrado',
                'message': f'No se encontró un usuario con ID {user_id}'
            }), 404

        # Verificar permisos
        current_user = request.current_user
        if (current_user['role'] != 'administrador' and
            current_user['id'] != user_id):
            return jsonify({
                'error': 'Acceso denegado',
                'message': 'No tienes permisos para actualizar este usuario'
            }), 403

        # Solo administradores pueden cambiar roles
        if 'rol_id' in data and current_user['role'] != 'administrador':
            return jsonify({
                'error': 'Acceso denegado',
                'message': 'Solo administradores pueden cambiar roles'
            }), 403

        # Actualizar campos permitidos
        if 'email' in data:
            user.email = data['email']
        if 'nombre_completo' in data:
            user.nombre_completo = data['nombre_completo']
        if 'rol_id' in data and current_user['role'] == 'administrador':
            user.rol_id = data['rol_id']
        if 'universidad_id' in data:
            user.universidad_id = data['universidad_id']
        if 'campus_id' in data:
            user.campus_id = data['campus_id']

        # Si se cambió la contraseña
        if 'password' in data:
            jwt_service = JWTService()
            user.clave_hash = jwt_service.hash_password(data['password'])

        updated_user = usuario_repo.update(user)

        result = {
            'id': updated_user.id,
            'email': updated_user.email,
            'nombre_completo': updated_user.nombre_completo,
            'rol_id': updated_user.rol_id,
            'universidad_id': updated_user.universidad_id,
            'campus_id': updated_user.campus_id
        }

        logger.info(f"Usuario {user_id} actualizado exitosamente")
        return jsonify({
            'message': 'Usuario actualizado exitosamente',
            'user': result
        }), 200

    except ValueError as e:
        logger.warning(f"Error de validación al actualizar usuario {user_id}: {str(e)}")
        return jsonify({
            'error': 'Error de validación',
            'message': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error al actualizar usuario {user_id}: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al actualizar el usuario'
        }), 500


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@token_required
@role_required(['administrador'])
def delete_user(user_id: int):
    """
    Eliminar un usuario.

    Args:
        user_id: ID del usuario a eliminar

    Returns:
        JSON con mensaje de confirmación
    """
    try:
        usuario_repo = UsuarioRepository()
        user = usuario_repo.find_by_id(user_id)

        if not user:
            return jsonify({
                'error': 'Usuario no encontrado',
                'message': f'No se encontró un usuario con ID {user_id}'
            }), 404

        # No permitir eliminar al propio usuario
        current_user = request.current_user
        if current_user['id'] == user_id:
            return jsonify({
                'error': 'Operación no permitida',
                'message': 'No puedes eliminar tu propio usuario'
            }), 400

        success = usuario_repo.delete(user_id)

        if success:
            logger.info(f"Usuario {user_id} eliminado exitosamente")
            return jsonify({
                'message': 'Usuario eliminado exitosamente'
            }), 200
        else:
            return jsonify({
                'error': 'Usuario no encontrado',
                'message': f'No se pudo eliminar el usuario con ID {user_id}'
            }), 404

    except ValueError as e:
        logger.warning(f"Error de validación al eliminar usuario {user_id}: {str(e)}")
        return jsonify({
            'error': 'Error de validación',
            'message': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error al eliminar usuario {user_id}: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al eliminar el usuario'
        }), 500