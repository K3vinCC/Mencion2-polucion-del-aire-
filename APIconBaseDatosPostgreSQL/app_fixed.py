#!/usr/bin/env python3
"""
Aplicación Flask corregida para la API de Monitoreo de Calidad del Aire.
Sistema de Universidad Nacional de Ingeniería
"""

import os
from pathlib import Path
from flask import Flask, jsonify, send_from_directory, request, make_response
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import jwt
import datetime

def create_app():
    """Crear aplicación Flask con configuración completa."""
    
    app = Flask(__name__)
    
    # Configuración CORS más permisiva para desarrollo
    CORS(app, 
         origins=["*"],  # Permitir todos los orígenes en desarrollo
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-API-Token"],
         supports_credentials=True)
    
    # Configuración básica
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    
    # Determinar directorio del proyecto
    project_root = Path(__file__).parent
    print(f"📁 Directorio del proyecto: {project_root}")
    
    # Configuración de Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.yaml'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Sistema de Monitoreo de Calidad del Aire - UNI",
            'supportedSubmitMethods': ['get', 'post', 'put', 'delete', 'patch'],
            'tryItOutEnabled': True,
            'displayOperationId': False,
            'displayRequestDuration': True,
            'docExpansion': 'list',
            'defaultModelsExpandDepth': 2,
            'deepLinking': True
        }
    )
    
    app.register_blueprint(swaggerui_blueprint)
    
    # === ENDPOINTS PRINCIPALES ===
    
    @app.route('/')
    def index():
        """Página de inicio de la API."""
        return jsonify({
            "message": "🎓 API de Monitoreo de Calidad del Aire - Universidad Nacional de Ingeniería",
            "version": "1.2.0",
            "description": "Sistema IoT para monitoreo de calidad del aire en campus universitarios",
            "endpoints": {
                "documentation": f"{request.url_root}api/docs",
                "health": f"{request.url_root}health",
                "swagger_spec": f"{request.url_root}static/swagger.yaml"
            },
            "status": "✅ API funcionando correctamente"
        })
    
    @app.route('/health')
    def health_check():
        """Verificar estado del sistema."""
        return jsonify({
            "status": "healthy",
            "message": "🚀 Sistema de Monitoreo UNI funcionando correctamente",
            "version": "1.2.0",
            "database": os.getenv('DATABASE_URL', 'PostgreSQL configurado'),
            "endpoints": {
                "swagger_ui": f"{request.url_root}api/docs",
                "swagger_spec": f"{request.url_root}static/swagger.yaml"
            }
        })
    
    @app.route('/static/swagger.yaml')
    def swagger_spec():
        """Servir especificación OpenAPI/Swagger."""
        try:
            swagger_path = project_root / 'swagger.yaml'
            print(f"🔍 Buscando swagger.yaml en: {swagger_path}")
            print(f"📄 Archivo existe: {swagger_path.exists()}")
            
            if swagger_path.exists():
                return send_from_directory(
                    str(project_root),
                    'swagger.yaml',
                    mimetype='text/yaml; charset=utf-8'
                )
            else:
                # Listar archivos en el directorio para debug
                files = [f.name for f in project_root.iterdir() if f.is_file()]
                return jsonify({
                    "error": "❌ swagger.yaml no encontrado",
                    "searched_path": str(swagger_path),
                    "project_root": str(project_root),
                    "files_in_directory": files
                }), 404
                
        except Exception as e:
            return jsonify({
                "error": f"❌ Error al cargar swagger.yaml: {str(e)}",
                "project_root": str(project_root)
            }), 500
    
    @app.route('/debug/info')
    def debug_info():
        """Información de debug del sistema."""
        try:
            swagger_path = project_root / 'swagger.yaml'
            files = [f.name for f in project_root.iterdir() if f.is_file()]
            
            return jsonify({
                "project_root": str(project_root),
                "swagger_path": str(swagger_path),
                "swagger_exists": swagger_path.exists(),
                "files_in_project": files,
                "environment": {
                    "FLASK_ENV": os.getenv('FLASK_ENV'),
                    "FLASK_DEBUG": os.getenv('FLASK_DEBUG'),
                    "DATABASE_URL": os.getenv('DATABASE_URL', 'No configurada')
                }
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # === ENDPOINTS DE PRUEBA BÁSICOS ===
    
    @app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
    def login():
        """Endpoint de login funcional."""
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add("Access-Control-Allow-Headers", "*")
            response.headers.add("Access-Control-Allow-Methods", "*")
            return response
            
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No se enviaron datos"}), 400
                
            email = data.get('email')
            password = data.get('password')
            
            # Verificar credenciales de prueba
            if email == "admin@uni.edu.pe" and password == "admin123":
                # Generar token JWT simple (para pruebas)
                import datetime
                
                token_payload = {
                    "user_id": 1,
                    "email": email,
                    "role": "Admin_Universidad",
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
                }
                
                token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
                
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
                return jsonify({"error": "Credenciales inválidas"}), 401
                
        except Exception as e:
            return jsonify({"error": f"Error en login: {str(e)}"}), 500
    
    @app.route('/api/users', methods=['GET'])
    def get_users():
        """Endpoint de usuarios de prueba."""
        return jsonify({
            "message": "👥 Endpoint de usuarios",
            "status": "OK",
            "users": [
                {"email": "admin@uni.edu.pe", "role": "Admin_Universidad"},
                {"email": "conserje@uni.edu.pe", "role": "Conserje"},
                {"email": "limpieza@uni.edu.pe", "role": "Limpiador"}
            ]
        })
    
    @app.route('/api/devices', methods=['GET'])
    def get_devices():
        """Endpoint de dispositivos de prueba."""
        return jsonify({
            "message": "📱 Endpoint de dispositivos IoT",
            "status": "OK",
            "devices": []
        })
    
    # === MANEJO DE ERRORES ===
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "❌ Endpoint no encontrado",
            "message": "Consulta la documentación en /api/docs",
            "available_endpoints": [
                "/",
                "/health",
                "/api/docs",
                "/static/swagger.yaml",
                "/debug/info"
            ]
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "❌ Error interno del servidor",
            "message": "Revisa los logs para más detalles"
        }), 500
    
    return app


def main():
    """Función principal para ejecutar la aplicación."""
    print("🚀 Iniciando Sistema de Monitoreo de Calidad del Aire - UNI")
    print("=" * 60)
    
    app = create_app()
    
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', '5000'))
    debug = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    
    print(f"🌐 Servidor: http://localhost:{port}")
    print(f"📚 Documentación: http://localhost:{port}/api/docs")
    print(f"💚 Health Check: http://localhost:{port}/health")
    print(f"🔧 Debug Info: http://localhost:{port}/debug/info")
    print("=" * 60)
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=False  # Desactivar auto-reload para evitar problemas
    )


if __name__ == '__main__':
    main()