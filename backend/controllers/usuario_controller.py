from flask import Blueprint, request, jsonify
from services.usuario_service import UsuarioService

usuario_bp = Blueprint('usuario', __name__)

# -------------------------
# Listar todos los usuarios
# -------------------------
@usuario_bp.route('/listar', methods=['GET'])
def listar_usuarios():
    usuarios = UsuarioService.listar_usuarios()
    return jsonify({'success': True, 'usuarios': usuarios})

# -------------------------
# Obtener usuario por ID
# -------------------------
@usuario_bp.route('/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    usuario = UsuarioService.obtener_usuario(usuario_id)
    if not usuario:
        return jsonify({'success': False, 'message': 'Usuario no encontrado'}), 404
    return jsonify({'success': True, 'usuario': usuario})

# -------------------------
# Crear usuario (admin)
# -------------------------
@usuario_bp.route('/crear', methods=['POST'])
def crear_usuario():
    data = request.json
    res = UsuarioService.register(
        email=data.get('email'),
        nombre=data.get('nombre_completo'),
        password=data.get('password'),
        rol_nombre=data.get('rol', 'admin')
    )
    return jsonify(res), (201 if res['success'] else 400)

# -------------------------
# Actualizar usuario
# -------------------------
@usuario_bp.route('/<int:usuario_id>/actualizar', methods=['PUT'])
def actualizar_usuario(usuario_id):
    data = request.json
    res = UsuarioService.actualizar_usuario(
        usuario_id,
        nombre=data.get('nombre_completo'),
        email=data.get('email'),
        rol_nombre=data.get('rol')
    )
    return jsonify(res), (200 if res['success'] else 400)

# -------------------------
# Eliminar usuario
# -------------------------
@usuario_bp.route('/<int:usuario_id>/eliminar', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    res = UsuarioService.eliminar_usuario(usuario_id)
    return jsonify(res), (200 if res['success'] else 400)
