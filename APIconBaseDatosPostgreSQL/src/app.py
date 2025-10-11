# src/app.py
"""
Aplicación principal Flask para la API de Monitoreo de Calidad del Aire.
"""

import os
from pathlib import Path
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint


def create_app(config_name: str = None) -> Flask:
    """
    Factory function para crear la aplicación Flask.

    Args:
        config_name: Nombre de la configuración a usar

    Returns:
        Aplicación Flask configurada
    """
    # Crear aplicación Flask
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    
    # Configurar CORS
    CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','))

    # Obtener el directorio del proyecto
    project_root = Path(__file__).parent.parent
    
    # Configuración de Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.yaml'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Sistema de Monitoreo de Calidad del Aire UNI",
            'supportedSubmitMethods': ['get', 'post', 'put', 'delete', 'patch'],
            'tryItOutEnabled': True,
            'displayOperationId': False,
            'displayRequestDuration': True,
            'docExpansion': 'list',
            'defaultModelsExpandDepth': 2,
            'defaultModelExpandDepth': 2
        }
    )
    
    app.register_blueprint(swaggerui_blueprint)
    
    # Ruta para servir swagger.yaml
    @app.route('/static/swagger.yaml')
    def swagger_yaml():
        try:
            swagger_path = project_root / 'swagger.yaml'
            if swagger_path.exists():
                return send_from_directory(
                    str(project_root),
                    'swagger.yaml',
                    mimetype='text/yaml'
                )
            else:
                return jsonify({"error": "swagger.yaml not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Debug endpoint para verificar rutas
    @app.route('/debug/paths')
    def debug_paths():
        try:
            current_file = Path(__file__)
            project_root = current_file.parent.parent
            swagger_path = project_root / 'swagger.yaml'
            
            return jsonify({
                "current_file": str(current_file),
                "project_root": str(project_root),
                "swagger_path": str(swagger_path),
                "swagger_exists": swagger_path.exists(),
                "files_in_project_root": [f.name for f in project_root.iterdir() if f.is_file()][:10]
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        try:
            return jsonify({
                "status": "healthy",
                "message": "API de Monitoreo de Calidad del Aire funcionando",
                "endpoints": {
                    "swagger_ui": f"{request.url_root}api/docs",
                    "swagger_spec": f"{request.url_root}static/swagger.yaml",
                    "health": f"{request.url_root}health"
                },
                "database": os.getenv('DATABASE_URL', 'No configurada'),
                "version": "1.2.0"
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    
    # Endpoints de prueba básicos
    @app.route('/login', methods=['POST'])
    def login():
        return jsonify({
            "message": "Endpoint de login funcionando",
            "status": "OK",
            "note": "Implementación completa disponible en /api/docs"
        })
    
    @app.route('/usuarios', methods=['GET'])
    def get_users():
        return jsonify({
            "users": [],
            "message": "Endpoint de usuarios funcionando",
            "status": "OK"
        })
    
    @app.route('/dispositivos', methods=['GET'])
    def get_devices():
        return jsonify({
            "devices": [],
            "message": "Endpoint de dispositivos funcionando",
            "status": "OK"
        })
    
    @app.route('/lecturas', methods=['POST'])
    def receive_readings():
        return jsonify({
            "status": "datos recibidos",
            "message": "Endpoint de lecturas funcionando",
            "timestamp": "2025-01-01T00:00:00Z"
        }), 202
    
    # Ruta raíz
    @app.route('/')
    def index():
        return jsonify({
            "message": "API de Monitoreo de Calidad del Aire - Universidad Nacional de Ingeniería",
            "version": "1.2.0",
            "documentation": f"{request.url_root}api/docs",
            "health": f"{request.url_root}health",
            "swagger_spec": f"{request.url_root}static/swagger.yaml"
        })
    
    return app


# Instancia de la aplicación para desarrollo
app = create_app()


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )