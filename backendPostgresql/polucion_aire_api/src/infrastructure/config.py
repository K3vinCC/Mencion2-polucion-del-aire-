import inject
from src.domain.ports.usuario_repository import IUsuarioRepository
from src.domain.ports.notificacion_service import INotificacionService
from src.infrastructure.repositories.sqlite_usuario_repository import SQLiteUsuarioRepository
from src.infrastructure.services.telegram_notificacion_service import TelegramNotificacionService

def configure_app(app):
    """Configura la aplicación Flask con inyección de dependencias"""
    
    def configure_inject():
        """Configura las inyecciones de dependencia"""
        def config(binder):
            # Repositorios
            binder.bind(IUsuarioRepository, SQLiteUsuarioRepository())
            
            # Servicios
            binder.bind(INotificacionService, TelegramNotificacionService())
        
        inject.configure(config)
    
    # Configurar inyección de dependencias
    configure_inject()
    
    return app