from flask import Blueprint, request, jsonify
from services.usuario_service import UsuarioService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    return jsonify(UsuarioService.register(
        email=data.get('email'),
        nombre=data.get('nombre_completo'),
        password=data.get('password'),
        rol_nombre=data.get('rol', 'admin')
    ))

@auth_bp.route('/register/conserje', methods=['POST'])
def register_conserje():
    data = request.json
    return jsonify(UsuarioService.register(
        email=data.get('email'),
        nombre=data.get('nombre_completo'),
        password=data.get('password'),
        rol_nombre='conserje'
    ))

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    return jsonify(UsuarioService.login(
        email=data.get('email'),
        password=data.get('password')
    ))
