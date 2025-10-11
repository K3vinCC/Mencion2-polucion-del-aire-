from flask import Blueprint, jsonify, request
from datetime import datetime
from src.application.casos_uso.dispositivo_service import DispositivoService
from src.application.casos_uso.lectura_service import LecturaService
from src.domain.entities.lectura_calidad_aire import LecturaCalidadAire

api = Blueprint('api', __name__)

# Las instancias de servicios se inicializarán después de la configuración
auth_service = None
dispositivo_service = None
lectura_service = None

def init_services():
    """Inicializa los servicios después de la configuración de la inyección"""
    global auth_service, dispositivo_service, lectura_service
    import inject
    from src.application.auth.auth_service import AuthService
    
    auth_service = inject.instance(AuthService)
    dispositivo_service = inject.instance(DispositivoService)
    lectura_service = inject.instance(LecturaService)

@api.route('/auth/login', methods=['POST'])
def login():
    """Endpoint de autenticación"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email y contraseña son requeridos'}), 400
    
    token = auth_service.login(data['email'], data['password'])
    if token:
        return jsonify({'token': token}), 200
    
    return jsonify({'error': 'Credenciales inválidas'}), 401

@api.route('/lecturas/aire', methods=['POST'])
def registrar_lectura():
    """Endpoint para registrar una nueva lectura de calidad del aire"""
    # Verificar autenticación del dispositivo
    token = request.headers.get('X-API-Token')
    if not token:
        return jsonify({'error': 'Token no proporcionado'}), 401
    
    dispositivo = dispositivo_service.autenticar_dispositivo(token)
    if not dispositivo:
        return jsonify({'error': 'Dispositivo no autorizado'}), 401
    
    data = request.get_json()
    lectura = LecturaCalidadAire(
        id=None,
        dispositivo_id=dispositivo.id,
        valor_pm1=data.get('pm1'),
        valor_pm2_5=data.get('pm2_5'),
        valor_pm10=data.get('pm10'),
        etiqueta=data.get('etiqueta'),
        fecha_lectura=datetime.now()
    )
    
    lectura_guardada = lectura_service.registrar_lectura(lectura)
    return jsonify({
        'id': lectura_guardada.id,
        'nivel_calidad': lectura_guardada.get_nivel_calidad()
    }), 201

@api.route('/lecturas/aire/<int:dispositivo_id>', methods=['GET'])
def obtener_lecturas(dispositivo_id):
    """Endpoint para obtener las últimas lecturas de un dispositivo"""
    # Verificar autenticación del usuario
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return jsonify({'error': 'Token no proporcionado'}), 401
    
    usuario = auth_service.validar_token(token.split(' ')[1])
    if not usuario:
        return jsonify({'error': 'Token inválido'}), 401
    
    # Verificar permisos
    if not auth_service.puede_ver_dispositivo(usuario, dispositivo_id):
        return jsonify({'error': 'No autorizado'}), 403
    
    lecturas = lectura_service.obtener_ultimas_lecturas(dispositivo_id)
    return jsonify([{
        'id': l.id,
        'pm1': l.valor_pm1,
        'pm2_5': l.valor_pm2_5,
        'pm10': l.valor_pm10,
        'nivel_calidad': l.get_nivel_calidad(),
        'fecha': l.fecha_lectura.isoformat(),
    } for l in lecturas]), 200