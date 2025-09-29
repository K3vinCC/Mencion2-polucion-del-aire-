#!/usr/bin/env python3
"""
Servidor Flask simplificado y estable para API de Monitoreo de Calidad del Aire
"""

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import jwt
import datetime
import os

app = Flask(__name__)

# Configuración CORS completa
CORS(app, 
     origins=["*"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-API-Token"],
     supports_credentials=True)

# Configuración básica
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['DEBUG'] = True

@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

@app.route('/')
def index():
    """Página de inicio"""
    return jsonify({
        "message": "🎓 API de Monitoreo de Calidad del Aire - UNI",
        "version": "1.3.0",
        "status": "✅ Funcionando correctamente",
        "endpoints": {
            "login": "/api/auth/login",
            "docs": "/api/docs",
            "health": "/health"
        }
    })

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "message": "🚀 API funcionando correctamente",
        "version": "1.3.0"
    })

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    """Endpoint de login con JWT"""
    try:
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add("Access-Control-Allow-Headers", "*")
            response.headers.add("Access-Control-Allow-Methods", "*")
            return response
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se enviaron datos"}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        print(f"📧 Intento de login: {email}")
        
        # Verificar credenciales
        if email == "admin@uni.edu.pe" and password == "admin123":
            # Generar token JWT
            token_payload = {
                "user_id": 1,
                "email": email,
                "role": "Admin_Universidad",
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
            }
            
            token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
            
            print(f"✅ Login exitoso para: {email}")
            
            return jsonify({
                "token": token,
                "expires_in": 43200,
                "user": {
                    "id": 1,
                    "email": email,
                    "name": "Administrador UNI",
                    "role": "Admin_Universidad"
                }
            }), 200
        else:
            print(f"❌ Credenciales inválidas para: {email}")
            return jsonify({"error": "Credenciales inválidas"}), 401
            
    except Exception as e:
        print(f"💥 Error en login: {str(e)}")
        return jsonify({"error": f"Error en login: {str(e)}"}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """Obtener usuarios (requiere autenticación)"""
    try:
        # Verificar token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Token requerido"}), 401
        
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print(f"👤 Usuario autenticado: {payload.get('email')}")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401
        
        # Datos de usuarios de la base de datos
        users = [
            {"id": 1, "email": "admin@uni.edu.pe", "name": "Administrador UNI", "role": "Admin_Universidad"},
            {"id": 2, "email": "conserje@uni.edu.pe", "name": "Juan Pérez Conserje", "role": "Conserje"},
            {"id": 3, "email": "limpieza@uni.edu.pe", "name": "María García Limpiadora", "role": "Limpiador"}
        ]
        
        return jsonify({
            "users": users,
            "total": len(users),
            "message": "👥 Usuarios obtenidos exitosamente"
        })
        
    except Exception as e:
        print(f"💥 Error obteniendo usuarios: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500

@app.route('/api/devices', methods=['GET'])
def get_devices():
    """Obtener dispositivos IoT"""
    try:
        # Verificar token (similar a users)
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Token requerido"}), 401
        
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({"error": "Token inválido"}), 401
        
        devices = [
            {"id": 1, "mac_address": "AA:BB:CC:DD:EE:FF", "location": "Aula 101", "status": "conectado"},
            {"id": 2, "mac_address": "BB:CC:DD:EE:FF:AA", "location": "Aula 102", "status": "desconectado"}
        ]
        
        return jsonify({
            "devices": devices,
            "total": len(devices),
            "message": "📱 Dispositivos obtenidos exitosamente"
        })
        
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "❌ Endpoint no encontrado",
        "message": "Endpoints disponibles: /, /health, /api/auth/login, /api/users, /api/devices"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "❌ Error interno del servidor"
    }), 500

if __name__ == '__main__':
    print("🚀 Iniciando API de Monitoreo de Calidad del Aire - UNI")
    print("=" * 60)
    print("🌐 Servidor: http://localhost:5000")
    print("🔐 Login: POST /api/auth/login")
    print("👥 Usuarios: GET /api/users (requiere token)")
    print("📱 Dispositivos: GET /api/devices (requiere token)")
    print("💚 Health: GET /health")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,  # Sin debug para evitar problemas
        use_reloader=False  # Sin auto-reload
    )