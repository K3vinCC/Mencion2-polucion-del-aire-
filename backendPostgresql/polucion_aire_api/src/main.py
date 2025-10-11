from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import inject
from src.domain.ports.usuario_repository import IUsuarioRepository
from src.domain.ports.notificacion_service import INotificacionService
from src.infrastructure.repositories.sqlite_usuario_repository import SQLiteUsuarioRepository
from src.infrastructure.services.telegram_notificacion_service import TelegramNotificacionService
from src.interfaces.rest.routes import configure_routes

def configure_inject():
    """Configura las inyecciones de dependencia"""
    def config(binder):
        from src.domain.ports.dispositivo_repository import IDispositivoRepository
        from src.infrastructure.repositories.sqlite_dispositivo_repository import SQLiteDispositivoRepository
        from src.domain.ports.lectura_calidad_aire_repository import ILecturaCalidadAireRepository
        from src.infrastructure.repositories.sqlite_lectura_calidad_aire_repository import SQLiteLecturaCalidadAireRepository
        
        # Repositorios
        binder.bind(IUsuarioRepository, SQLiteUsuarioRepository())
        binder.bind(IDispositivoRepository, SQLiteDispositivoRepository())
        binder.bind(ILecturaCalidadAireRepository, SQLiteLecturaCalidadAireRepository())
        
        # Servicios
        binder.bind(INotificacionService, TelegramNotificacionService())
    
    inject.configure(config)

def create_app():
    """
    Crea y configura la aplicación Flask
    """
    # Cargar variables de entorno
    load_dotenv()
    
    # Configurar inyección de dependencias
    configure_inject()
    
    # Crear aplicación Flask
    app = Flask(__name__)
    
    # Configurar CORS
    CORS(app)
    
    # Configurar rutas
    configure_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )