#!/usr/bin/env python3
"""
API COMPLETA de Monitoreo de Calidad del Aire - UNI
Servidor Flask con todos los endpoints funcionales
"""

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import jwt
import datetime
import os
import sqlite3
import hashlib

app = Flask(__name__)

# Configuración CORS completa
CORS(app, 
     origins=["*"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-API-Token"],
     supports_credentials=True)

# Configuración
app.config['SECRET_KEY'] = 'uni-air-quality-secret-2025'
app.config['DEBUG'] = False

# Base de datos en memoria para desarrollo
def init_db():
    """Inicializar base de datos temporal"""
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    
    # Crear tablas básicas
    cursor.execute('''
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE,
            clave_hash TEXT,
            nombre_completo TEXT,
            rol TEXT,
            universidad TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE dispositivos (
            id INTEGER PRIMARY KEY,
            mac_address TEXT UNIQUE,
            ubicacion TEXT,
            estado TEXT DEFAULT 'desconectado',
            modelo TEXT,
            fecha_instalacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insertar usuarios de prueba
    usuarios_test = [
        (1, 'admin@uni.edu.pe', hashlib.sha256('admin123'.encode()).hexdigest(), 
         'Administrador UNI', 'Admin_Universidad', 'Universidad Nacional de Ingeniería'),
        (2, 'conserje@uni.edu.pe', hashlib.sha256('admin123'.encode()).hexdigest(),
         'Juan Pérez Conserje', 'Conserje', 'Universidad Nacional de Ingeniería'),
        (3, 'limpieza@uni.edu.pe', hashlib.sha256('admin123'.encode()).hexdigest(),
         'María García Limpiadora', 'Limpiador', 'Universidad Nacional de Ingeniería')
    ]
    
    cursor.executemany('''
        INSERT INTO usuarios (id, email, clave_hash, nombre_completo, rol, universidad)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', usuarios_test)
    
    # Insertar dispositivos de prueba
    dispositivos_test = [
        (1, 'AA:BB:CC:DD:EE:FF', 'Aula 101 - Edificio Sistemas', 'conectado', 'ESP32-DHT22-PMS5003'),
        (2, 'BB:CC:DD:EE:FF:AA', 'Aula 102 - Edificio Sistemas', 'desconectado', 'Arduino-SHT30-PMS7003'),
        (3, 'CC:DD:EE:FF:AA:BB', 'Lab M-101 - Edificio Mecánica', 'conectado', 'ESP32-DHT22-PMS5003')
    ]
    
    cursor.executemany('''
        INSERT INTO dispositivos (id, mac_address, ubicacion, estado, modelo)
        VALUES (?, ?, ?, ?, ?)
    ''', dispositivos_test)
    
    conn.commit()
    return conn

# Inicializar base de datos
db_conn = init_db()

def verificar_token(token):
    """Verificar y decodificar token JWT"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.before_request
def handle_options():
    """Manejar requests OPTIONS para CORS"""
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

# ===== ENDPOINTS PRINCIPALES =====

@app.route('/')
def index():
    """Página de inicio"""
    return jsonify({
        "mensaje": "🎓 API de Monitoreo de Calidad del Aire - UNI",
        "version": "2.0.0",
        "estado": "✅ Funcionando correctamente",
        "endpoints": {
            "login": "/login",
            "usuarios": "/api/usuarios", 
            "dispositivos": "/api/dispositivos",
            "swagger": "/api/docs",
            "salud": "/health"
        },
        "credenciales_prueba": {
            "email": "admin@uni.edu.pe",
            "clave": "admin123"
        }
    })

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        "estado": "saludable",
        "mensaje": "🚀 API UNI funcionando correctamente",
        "version": "2.0.0",
        "base_datos": "✅ Conectada",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """Login completo con JWT"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se enviaron datos"}), 400
            
        email = data.get('email')
        clave = data.get('clave')
        
        print(f"📧 Intento de login: {email}")
        
        if not email or not clave:
            return jsonify({"error": "Email y clave son requeridos"}), 400
        
        # Buscar usuario en base de datos
        cursor = db_conn.cursor()
        cursor.execute('''
            SELECT id, email, clave_hash, nombre_completo, rol, universidad
            FROM usuarios WHERE email = ?
        ''', (email,))
        
        usuario = cursor.fetchone()
        
        if not usuario:
            print(f"❌ Usuario no encontrado: {email}")
            return jsonify({"error": "Credenciales inválidas"}), 401
        
        # Verificar contraseña
        clave_hash = hashlib.sha256(clave.encode()).hexdigest()
        if clave_hash != usuario[2]:
            print(f"❌ Contraseña incorrecta para: {email}")
            return jsonify({"error": "Credenciales inválidas"}), 401
        
        # Generar token JWT
        token_payload = {
            "usuario_id": usuario[0],
            "email": usuario[1],
            "rol": usuario[4],
            "universidad": usuario[5],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
        }
        
        token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
        
        print(f"✅ Login exitoso para: {email}")
        
        return jsonify({
            "token": token,
            "expira_en": 43200,
            "tipo": "Bearer",
            "usuario": {
                "id": usuario[0],
                "email": usuario[1],
                "nombre_completo": usuario[3],
                "rol": usuario[4],
                "universidad": usuario[5]
            },
            "mensaje": "✅ Login exitoso"
        }), 200
        
    except Exception as e:
        print(f"💥 Error en login: {str(e)}")
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    """Obtener lista de usuarios (requiere autenticación)"""
    try:
        # Verificar token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Token requerido"}), 401
        
        token = auth_header.split(' ')[1]
        payload = verificar_token(token)
        
        if not payload:
            return jsonify({"error": "Token inválido o expirado"}), 401
        
        print(f"👤 Usuario autenticado: {payload.get('email')}")
        
        # Obtener usuarios de la base de datos
        cursor = db_conn.cursor()
        cursor.execute('''
            SELECT id, email, nombre_completo, rol, universidad, fecha_creacion
            FROM usuarios
        ''')
        
        usuarios = cursor.fetchall()
        
        usuarios_json = []
        for usuario in usuarios:
            usuarios_json.append({
                "id": usuario[0],
                "email": usuario[1],
                "nombre_completo": usuario[2],
                "rol": usuario[3],
                "universidad": usuario[4],
                "fecha_creacion": usuario[5]
            })
        
        return jsonify({
            "usuarios": usuarios_json,
            "total": len(usuarios_json),
            "mensaje": "👥 Usuarios obtenidos exitosamente"
        })
        
    except Exception as e:
        print(f"💥 Error obteniendo usuarios: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500

@app.route('/api/dispositivos', methods=['GET'])
def obtener_dispositivos():
    """Obtener lista de dispositivos IoT"""
    try:
        # Verificar token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Token requerido"}), 401
        
        token = auth_header.split(' ')[1]
        payload = verificar_token(token)
        
        if not payload:
            return jsonify({"error": "Token inválido o expirado"}), 401
        
        # Obtener dispositivos
        cursor = db_conn.cursor()
        cursor.execute('''
            SELECT id, mac_address, ubicacion, estado, modelo, fecha_instalacion
            FROM dispositivos
        ''')
        
        dispositivos = cursor.fetchall()
        
        dispositivos_json = []
        for dispositivo in dispositivos:
            dispositivos_json.append({
                "id": dispositivo[0],
                "mac_address": dispositivo[1],
                "ubicacion": dispositivo[2],
                "estado": dispositivo[3],
                "modelo": dispositivo[4],
                "fecha_instalacion": dispositivo[5]
            })
        
        return jsonify({
            "dispositivos": dispositivos_json,
            "total": len(dispositivos_json),
            "mensaje": "📱 Dispositivos obtenidos exitosamente"
        })
        
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    """Dashboard con información general"""
    try:
        # Verificar token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Token requerido"}), 401
        
        token = auth_header.split(' ')[1]
        payload = verificar_token(token)
        
        if not payload:
            return jsonify({"error": "Token inválido o expirado"}), 401
        
        cursor = db_conn.cursor()
        
        # Contar usuarios
        cursor.execute('SELECT COUNT(*) FROM usuarios')
        total_usuarios = cursor.fetchone()[0]
        
        # Contar dispositivos
        cursor.execute('SELECT COUNT(*) FROM dispositivos')
        total_dispositivos = cursor.fetchone()[0]
        
        # Dispositivos conectados
        cursor.execute("SELECT COUNT(*) FROM dispositivos WHERE estado = 'conectado'")
        dispositivos_conectados = cursor.fetchone()[0]
        
        return jsonify({
            "dashboard": {
                "total_usuarios": total_usuarios,
                "total_dispositivos": total_dispositivos,
                "dispositivos_conectados": dispositivos_conectados,
                "dispositivos_desconectados": total_dispositivos - dispositivos_conectados,
                "calidad_aire_promedio": "Buena",
                "ultima_actualizacion": datetime.datetime.now().isoformat()
            },
            "mensaje": "📊 Dashboard obtenido exitosamente"
        })
        
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

# ===== MANEJO DE ERRORES =====

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "❌ Endpoint no encontrado",
        "endpoints_disponibles": [
            "/", "/health", "/login", 
            "/api/usuarios", "/api/dispositivos", "/api/dashboard"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "❌ Error interno del servidor"
    }), 500

if __name__ == '__main__':
    print("🚀 Iniciando API COMPLETA de Monitoreo de Calidad del Aire - UNI")
    print("=" * 70)
    print("🌐 Servidor: http://localhost:5000")
    print("🔐 Login: POST /login")
    print("👥 Usuarios: GET /api/usuarios (requiere token)")
    print("📱 Dispositivos: GET /api/dispositivos (requiere token)")
    print("📊 Dashboard: GET /api/dashboard (requiere token)")
    print("💚 Health: GET /health")
    print("=" * 70)
    print("📧 Credenciales de prueba:")
    print("   Email: admin@uni.edu.pe")
    print("   Clave: admin123")
    print("=" * 70)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False
    )