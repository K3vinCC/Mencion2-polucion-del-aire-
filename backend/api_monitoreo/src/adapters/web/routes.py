# src/adapters/web/routes.py
from flask import Blueprint, request, jsonify, g
from src.infrastructure.dependencies import container
from src.application.errors.exceptions import BaseError
from src.infrastructure.middleware.auth_middleware import token_required, device_token_required, admin_required, conserje_required
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


# --- Endpoints de Usuarios ---

@api_blueprint.route('/users', methods=['GET'])
@token_required
@admin_required
def get_users():
    """Obtener todos los usuarios (solo administradores)."""
    try:
        obtener_todos_use_case = container.obtener_todos_usuarios_use_case
        usuarios = obtener_todos_use_case.ejecutar()
        return jsonify([usuario.to_dict() for usuario in usuarios]), 200
    except BaseError as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    """Obtener un usuario específico."""
    try:
        obtener_use_case = container.obtener_usuario_use_case
        usuario = obtener_use_case.ejecutar(user_id)
        return jsonify(usuario.to_dict()), 200
    except BaseError as e:
        return jsonify({"error": str(e)}), 404

@api_blueprint.route('/users/<int:user_id>', methods=['PUT'])
@token_required
@admin_required
def update_user(user_id):
    """Actualizar un usuario (solo administradores)."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo de la petición inválido"}), 400

    try:
        actualizar_use_case = container.actualizar_usuario_use_case
        usuario = actualizar_use_case.ejecutar(
            usuario_id=user_id,
            nombre=data.get('nombre'),
            correo=data.get('correo'),
            clave=data.get('clave'),
            rol=data.get('rol'),
            numero_contacto=data.get('numero_contacto'),
            url_imagen_perfil=data.get('url_imagen_perfil'),
            id_edificio_asignado=data.get('id_edificio_asignado')
        )
        return jsonify(usuario.to_dict()), 200
    except BaseError as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(user_id):
    """Eliminar un usuario (solo administradores)."""
    try:
        eliminar_use_case = container.eliminar_usuario_use_case
        eliminar_use_case.ejecutar(user_id)
        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
    except BaseError as e:
        return jsonify({"error": str(e)}), 400


# --- Endpoints de Dispositivos ---

@api_blueprint.route('/devices', methods=['POST'])
@token_required
@admin_required
def create_device():
    """Crear un nuevo dispositivo (solo administradores)."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo de la petición inválido"}), 400

    nombre = data.get('nombre')
    ubicacion = data.get('ubicacion')
    id_edificio = data.get('id_edificio')

    if not all([nombre, ubicacion, id_edificio]):
        return jsonify({"error": "Faltan campos requeridos: nombre, ubicacion, id_edificio"}), 400

    try:
        registrar_use_case = container.registrar_dispositivo_use_case
        dispositivo = registrar_use_case.ejecutar(
            nombre=nombre,
            ubicacion=ubicacion,
            id_edificio=id_edificio
        )
        return jsonify(dispositivo.to_dict()), 201
    except BaseError as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route('/devices', methods=['GET'])
@token_required
def get_devices():
    """Obtener todos los dispositivos."""
    try:
        dispositivo_repository = container.dispositivo_repository
        dispositivos = dispositivo_repository.get_all()
        return jsonify([dispositivo.to_dict() for dispositivo in dispositivos]), 200
    except BaseError as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route('/devices/<int:device_id>', methods=['GET'])
@token_required
def get_device(device_id):
    """Obtener un dispositivo específico."""
    try:
        dispositivo_repository = container.dispositivo_repository
        dispositivo = dispositivo_repository.find_by_id(device_id)
        if not dispositivo:
            return jsonify({"error": "Dispositivo no encontrado"}), 404
        return jsonify(dispositivo.to_dict()), 200
    except BaseError as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route('/devices/<int:device_id>', methods=['PUT'])
@token_required
@admin_required
def update_device(device_id):
    """Actualizar un dispositivo (solo administradores)."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo de la petición inválido"}), 400

    try:
        dispositivo_repository = container.dispositivo_repository
        dispositivo = dispositivo_repository.find_by_id(device_id)
        if not dispositivo:
            return jsonify({"error": "Dispositivo no encontrado"}), 404

        # Actualizar campos (esto sería mejor con un método update en el repositorio)
        # Por ahora, solo verificamos que existe
        return jsonify({"message": "Funcionalidad de actualización pendiente"}), 200
    except BaseError as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route('/devices/<int:device_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_device(device_id):
    """Eliminar un dispositivo (solo administradores)."""
    try:
        dispositivo_repository = container.dispositivo_repository
        dispositivo = dispositivo_repository.find_by_id(device_id)
        if not dispositivo:
            return jsonify({"error": "Dispositivo no encontrado"}), 404

        # Aquí normalmente eliminaríamos el dispositivo
        return jsonify({"message": "Funcionalidad de eliminación pendiente"}), 200
    except BaseError as e:
        return jsonify({"error": str(e)}), 400


# --- Endpoints de Lecturas ---

@api_blueprint.route('/readings', methods=['POST'])
@device_token_required
def create_reading():
    """Crear una nueva lectura de calidad del aire (desde dispositivo)."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo de la petición inválido"}), 400

    pm25 = data.get('pm25')
    pm10 = data.get('pm10')
    co2 = data.get('co2')
    temperatura = data.get('temperatura')
    humedad = data.get('humedad')

    if not all([pm25, pm10, co2, temperatura, humedad]):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    try:
        registrar_use_case = container.registrar_lectura_use_case
        lectura = registrar_use_case.ejecutar(
            token_dispositivo=request.headers['X-Device-Token'],
            pm25=float(pm25),
            pm10=float(pm10),
            co2=float(co2),
            temperatura=float(temperatura),
            humedad=float(humedad)
        )
        return jsonify(lectura.to_dict()), 201
    except BaseError as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route('/readings', methods=['GET'])
@token_required
def get_readings():
    """Obtener lecturas de calidad del aire."""
    id_dispositivo = request.args.get('device_id', type=int)
    id_edificio = request.args.get('building_id', type=int)
    limit = request.args.get('limit', 100, type=int)

    try:
        lectura_repository = container.lectura_repository

        if id_dispositivo:
            lecturas = lectura_repository.get_by_dispositivo(id_dispositivo, limit)
        elif id_edificio:
            lecturas = lectura_repository.get_by_edificio(id_edificio, limit)
        else:
            lecturas = lectura_repository.get_lecturas_recientes()

        return jsonify([lectura.to_dict() for lectura in lecturas]), 200
    except BaseError as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route('/readings/<int:reading_id>', methods=['GET'])
@token_required
def get_reading(reading_id):
    """Obtener una lectura específica."""
    try:
        lectura_repository = container.lectura_repository
        lectura = lectura_repository.find_by_id(reading_id)
        if not lectura:
            return jsonify({"error": "Lectura no encontrada"}), 404
        return jsonify(lectura.to_dict()), 200
    except BaseError as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route('/readings/stats', methods=['GET'])
@token_required
def get_reading_stats():
    """Obtener estadísticas de calidad del aire por edificio."""
    id_edificio = request.args.get('building_id', type=int)
    horas = request.args.get('hours', 24, type=int)

    if not id_edificio:
        return jsonify({"error": "Se requiere el parámetro building_id"}), 400

    try:
        lectura_repository = container.lectura_repository
        promedio = lectura_repository.get_promedio_calidad(id_edificio, horas)

        if promedio:
            return jsonify({
                "edificio_id": id_edificio,
                "periodo_horas": horas,
                "promedio": promedio
            }), 200
        else:
            return jsonify({"error": "No hay datos suficientes para calcular estadísticas"}), 404
    except BaseError as e:
        return jsonify({"error": str(e)}), 400


# --- Endpoints de Asignaciones ---

@api_blueprint.route('/assignments', methods=['POST'])
@token_required
@conserje_required
def create_assignment():
    """Crear una nueva asignación de limpieza."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo de la petición inválido"}), 400

    id_lectura = data.get('id_lectura')
    id_usuario_asignado = data.get('id_usuario_asignado')
    descripcion = data.get('descripcion')
    prioridad = data.get('prioridad', 'media')

    if not all([id_lectura, id_usuario_asignado, descripcion]):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    try:
        crear_use_case = container.crear_asignacion_limpieza_use_case
        asignacion = crear_use_case.ejecutar(
            id_lectura=id_lectura,
            id_usuario_asignado=id_usuario_asignado,
            descripcion=descripcion,
            prioridad=prioridad
        )
        return jsonify(asignacion.to_dict()), 201
    except BaseError as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route('/assignments', methods=['GET'])
@token_required
def get_assignments():
    """Obtener asignaciones de limpieza."""
    estado = request.args.get('estado')
    id_usuario = request.args.get('user_id', type=int)

    try:
        asignacion_repository = container.asignacion_repository

        if estado:
            asignaciones = asignacion_repository.get_by_estado(estado)
        elif id_usuario:
            asignaciones = asignacion_repository.get_by_usuario(id_usuario)
        else:
            asignaciones = asignacion_repository.get_pendientes()

        return jsonify([asignacion.to_dict() for asignacion in asignaciones]), 200
    except BaseError as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route('/assignments/<int:assignment_id>', methods=['GET'])
@token_required
def get_assignment(assignment_id):
    """Obtener una asignación específica."""
    try:
        asignacion_repository = container.asignacion_repository
        asignacion = asignacion_repository.find_by_id(assignment_id)
        if not asignacion:
            return jsonify({"error": "Asignación no encontrada"}), 404
        return jsonify(asignacion.to_dict()), 200
    except BaseError as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route('/assignments/<int:assignment_id>/complete', methods=['PUT'])
@token_required
@conserje_required
def complete_assignment(assignment_id):
    """Marcar una asignación como completada."""
    try:
        asignacion_repository = container.asignacion_repository
        asignacion = asignacion_repository.find_by_id(assignment_id)
        if not asignacion:
            return jsonify({"error": "Asignación no encontrada"}), 404

        # Verificar que el usuario asignado es el que está completando
        if asignacion.id_usuario_asignado != g.usuario.id:
            return jsonify({"error": "Solo el usuario asignado puede completar esta tarea"}), 403

        from datetime import datetime
        asignacion_repository.update_estado(assignment_id, 'completada', datetime.utcnow().isoformat())
        return jsonify({"message": "Asignación completada exitosamente"}), 200
    except BaseError as e:
        return jsonify({"error": str(e)}), 400

@api_blueprint.route('/assignments/<int:assignment_id>', methods=['PUT'])
@token_required
@conserje_required
def update_assignment(assignment_id):
    """Actualizar el estado de una asignación."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Cuerpo de la petición inválido"}), 400

    estado = data.get('estado')
    if not estado:
        return jsonify({"error": "Se requiere el campo 'estado'"}), 400

    try:
        asignacion_repository = container.asignacion_repository
        asignacion = asignacion_repository.find_by_id(assignment_id)
        if not asignacion:
            return jsonify({"error": "Asignación no encontrada"}), 404

        fecha_completado = None
        if estado == 'completada':
            from datetime import datetime
            fecha_completado = datetime.utcnow().isoformat()

        asignacion_repository.update_estado(assignment_id, estado, fecha_completado)
        return jsonify({"message": f"Asignación actualizada a estado: {estado}"}), 200
    except BaseError as e:
        return jsonify({"error": str(e)}), 400