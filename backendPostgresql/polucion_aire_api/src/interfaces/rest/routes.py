from src.interfaces.rest.controllers.api_controller import api, init_services
from src.interfaces.rest.controllers.auth_controller import auth_bp

def configure_routes(app):
    """Configura las rutas de la aplicación"""
    # Inicializar servicios después de la configuración de la inyección
    init_services()
    # Registrar blueprints
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')