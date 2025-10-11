# src/main.py
"""
Punto de entrada principal de la API de Monitoreo de Calidad del Aire.
"""

import os
import logging
from flask import Flask
from flask_cors import CORS

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Solo console logging para evitar problemas con archivos
    ]
)

logger = logging.getLogger(__name__)

def create_app() -> Flask:
    """
    Factory function para crear la aplicación Flask.

    Returns:
        Flask: Instancia configurada de la aplicación Flask
    """
    app = Flask(__name__)

    # Configuración CORS
    CORS(app)

    # Configuración de la aplicación
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')

    # Configuración de base de datos
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        # Usar SQLite para desarrollo si no hay DATABASE_URL
        database_url = 'sqlite:///air_quality_dev.db'
        logger.warning("DATABASE_URL no configurada, usando SQLite para desarrollo")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuración de servicios externos
    app.config['TELEGRAM_BOT_TOKEN'] = os.getenv('TELEGRAM_BOT_TOKEN')
    app.config['TELEGRAM_CHAT_ID'] = os.getenv('TELEGRAM_CHAT_ID')

    # Inicializar base de datos
    from src.infrastructure.database.database import init_db
    with app.app_context():
        try:
            init_db()
        except Exception as e:
            logger.error(f"Error al inicializar la base de datos: {str(e)}")
            raise

    # Registrar blueprints
    from src.infrastructure.controllers.auth_controller import auth_bp
    from src.infrastructure.controllers.users_controller import users_bp
    from src.infrastructure.controllers.devices_controller import devices_bp
    from src.infrastructure.controllers.readings_controller import readings_bp
    from src.infrastructure.controllers.assignments_controller import assignments_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(devices_bp)
    app.register_blueprint(readings_bp)
    app.register_blueprint(assignments_bp)

    # Ruta de health check
    @app.route('/health', methods=['GET'])
    def health_check():
        """Endpoint de health check."""
        return {
            'status': 'healthy',
            'service': 'Air Quality Monitoring API',
            'version': '1.0.0'
        }, 200

    # Configuración de Swagger UI
    from flask_swagger_ui import get_swaggerui_blueprint

    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.yaml'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "API de Monitoreo de Calidad del Aire"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Ruta raíz
    @app.route('/', methods=['GET'])
    def root():
        """Endpoint raíz con información básica de la API."""
        return {
            'message': 'API de Monitoreo de Calidad del Aire',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'users': '/api/users',
                'devices': '/api/devices',
                'readings': '/api/readings',
                'assignments': '/api/assignments',
                'health': '/health',
                'documentation': '/api/docs'
            },
            'documentation': 'Ver /api/docs para documentación Swagger UI'
        }, 200

    # Ruta para servir el archivo swagger.yaml
    @app.route('/static/swagger.yaml', methods=['GET'])
    def swagger_spec():
        """Servir la especificación OpenAPI/Swagger."""
        try:
            import os
            # Buscar el archivo swagger.yaml en el directorio raíz del proyecto
            current_dir = os.path.dirname(os.path.dirname(__file__))
            swagger_path = os.path.join(current_dir, 'swagger.yaml')
            with open(swagger_path, 'r', encoding='utf-8') as f:
                return f.read(), 200, {'Content-Type': 'application/yaml'}
        except FileNotFoundError:
            return {'error': 'Archivo de documentación no encontrado'}, 404
        except Exception as e:
            return {'error': f'Error al cargar documentación: {str(e)}'}, 500
    @app.errorhandler(404)
    def not_found(error):
        return {
            'error': 'Recurso no encontrado',
            'message': 'La ruta solicitada no existe'
        }, 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return {
            'error': 'Método no permitido',
            'message': 'El método HTTP utilizado no está permitido para esta ruta'
        }, 405

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"Error interno del servidor: {str(error)}")
        return {
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error inesperado'
        }, 500

    logger.info("Aplicación Flask creada exitosamente")
    return app

def main():
    """
    Función principal para ejecutar la aplicación.
    """
    app = create_app()

    # Configuración del servidor
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    logger.info(f"Iniciando servidor en {host}:{port} (debug={debug})")

    app.run(
        host=host,
        port=port,
        debug=debug
    )

if __name__ == '__main__':
    main()