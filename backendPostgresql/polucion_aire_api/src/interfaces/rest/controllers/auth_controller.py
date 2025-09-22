from flask import Blueprint, jsonify, request
from src.application.auth.auth_service import AuthService
from src.interfaces.rest.middleware.auth_middleware import require_auth, require_roles
from src.domain.entities.usuario import Usuario
import inject
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@require_auth  # Solo usuarios autenticados pueden crear otros usuarios
@require_roles(1, 2)  # Solo SuperAdmin(1) y Admin_Universidad(2) pueden crear usuarios
def register():
    """Endpoint para registrar un nuevo usuario"""
    data = request.get_json()
    
    if not data or not all(key in data for key in ['email', 'password', 'nombre_completo', 'rol_id']):
        return jsonify({'error': 'Faltan datos requeridos'}), 400
    
    # Hash de la contraseña
    password_hash = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
    
    # Crear usuario
    nuevo_usuario = Usuario(
        id=None,
        email=data['email'],
        clave_hash=password_hash,
        nombre_completo=data['nombre_completo'],
        rol_id=data['rol_id'],
        universidad_id=data.get('universidad_id'),  # Opcional
        fecha_creacion=None  # Se establecerá automáticamente
    )
    
    # Obtener el servicio de autenticación
    auth_service = inject.instance(AuthService)
    
    try:
        usuario_creado = auth_service.crear_usuario(nuevo_usuario)
        return jsonify({
            'message': 'Usuario creado exitosamente',
            'usuario': {
                'id': usuario_creado.id,
                'email': usuario_creado.email,
                'nombre_completo': usuario_creado.nombre_completo,
                'rol_id': usuario_creado.rol_id
            }
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint para autenticar un usuario"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email y contraseña son requeridos'}), 400
    
    auth_service = inject.instance(AuthService)
    token = auth_service.login(data['email'], data['password'])
    
    if token:
        return jsonify({'token': token}), 200
    
    return jsonify({'error': 'Credenciales inválidas'}), 401

@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user():
    """Endpoint para obtener la información del usuario actual"""
    return jsonify({
        'id': g.usuario_actual.id,
        'email': g.usuario_actual.email,
        'nombre_completo': g.usuario_actual.nombre_completo,
        'rol_id': g.usuario_actual.rol_id,
        'universidad_id': g.usuario_actual.universidad_id
    })