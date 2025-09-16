# src/adapters/web/routes.py
from flask import Blueprint, request, jsonify
from src.infrastructure.dependencies import container
from src.application.errors.exceptions import BaseError
import re # Para validación manual de correo
import jwt
import datetime
from flask import current_app

# Un Blueprint es un conjunto de rutas que luego pueden ser registradas en la aplicación principal.
# Ayuda a mantener el código organizado.
api_blueprint = Blueprint('api', __name__)


# --- Funciones de Validación Manual ---
def validar_email_manualmente(email):
    """Valida el formato de un email usando una expresión regular."""
    # Expresión regular simple para validar emails
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email)

def validar_clave_manualmente(clave):
    """Valida que la contraseña tenga al menos 8 caracteres."""
    return len(clave) >= 8


# --- Endpoints de la API ---

@api_blueprint.route('/register', methods=['POST'])
def register_user():
    """
    Endpoint para registrar un nuevo usuario.
    Este es el "Adaptador de Entrada" que conecta el mundo HTTP con nuestros casos de uso.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo de la petición inválido"}), 400

    # 1. Extracción y Validación Manual de Datos
    nombre = data.get('nombre')
    correo = data.get('correo')
    clave = data.get('clave')
    rol = data.get('rol', 'conserje') # Rol por defecto si no se especifica

    if not all([nombre, correo, clave]):
        return jsonify({"error": "Faltan campos requeridos: nombre, correo, clave"}), 400
    
    if not validar_email_manualmente(correo):
        return jsonify({"error": "Formato de correo inválido"}), 400

    if not validar_clave_manualmente(clave):
        return jsonify({"error": "La clave debe tener al menos 8 caracteres"}), 400
    
    try:
        # 2. Ejecutar el Caso de Uso a través del contenedor de dependencias
        registrar_use_case = container.registrar_usuario_use_case
        nuevo_usuario = registrar_use_case.ejecutar(
            nombre=nombre,
            correo=correo,
            clave=clave,
            rol=rol
        )

        # 3. Devolver una respuesta exitosa
        return jsonify(nuevo_usuario.to_dict()), 201

    except BaseError as e:
        # 4. Manejo de Errores de Negocio
        # Si el caso de uso lanza un error conocido (ej: email ya existe),
        # lo capturamos y devolvemos una respuesta HTTP apropiada.
        return jsonify({"error": str(e)}), 409 # 409 Conflict

@api_blueprint.route('/login', methods=['POST'])
def login_user():
    """Endpoint para iniciar sesión y obtener un token."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo de la petición inválido"}), 400
    
    correo = data.get('correo')
    clave = data.get('clave')

    if not all([correo, clave]):
        return jsonify({"error": "Faltan campos requeridos: correo, clave"}), 400

    try:
        # 1. Ejecutar el Caso de Uso de Login
        login_use_case = container.login_usuario_use_case
        usuario_autenticado = login_use_case.ejecutar(correo, clave)

        # 2. Generación "Manual" de Token (JWT)
        # Creamos el payload del token con el ID del usuario y una fecha de expiración.
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow(),
            'sub': usuario_autenticado.id
        }
        
        # Codificamos el token usando la clave secreta de la app
        token = jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        # 3. Devolver el token
        return jsonify({"token": token}), 200

    except BaseError as e:
        # 4. Manejo de Errores de Login
        return jsonify({"error": str(e)}), 401 # 401 Unauthorized