# src/infrastructure/web/app.py
from flask import Flask, jsonify
import os
from src.adapters.web.routes import api_blueprint
from src.infrastructure.dependencies import container
from src.application.errors.exceptions import BaseError

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Ruta absoluta a la base de datos para evitar problemas de rutas relativas
    # __file__ es la ruta de este archivo, '..' sube un nivel
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, '..', '..', '..', 'database.db')
    app.config['DATABASE_PATH'] = db_path
    
    # El contenedor necesita el contexto de la aplicación para acceder a la config
    with app.app_context():
        # Inyectamos la app en el contenedor si es necesario o simplemente usamos el contexto
        # Aquí es donde se conectan todas nuestras dependencias
        app.container = container

    @app.route('/ping')
    def ping():
        return jsonify({"message": "pong"})

    # Registrar nuestro Blueprint de la API
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # --- Manejador de Errores Global ---
    # Captura cualquier excepción no controlada y devuelve una respuesta JSON estandarizada
    @app.errorhandler(Exception)
    def handle_generic_error(e):
        # En un entorno de producción, podrías loggear el error aquí
        # import traceback
        # traceback.print_exc()
        return jsonify({"error": "Ocurrió un error interno en el servidor"}), 500

    @app.errorhandler(BaseError)
    def handle_base_error(e):
        """Maneja errores de negocio personalizados."""
        return jsonify({"error": str(e)}), 400

    return app