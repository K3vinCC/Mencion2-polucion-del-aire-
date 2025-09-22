import inject
from src.domain.ports.dispositivo_repository import IDispositivoRepository
from src.domain.entities.dispositivo import Dispositivo

class DispositivoService:
    """Servicio para la gestión de dispositivos"""
    
    @inject.autoparams()
    def __init__(self, dispositivo_repository: IDispositivoRepository):
        self.dispositivo_repository = dispositivo_repository
    
    def autenticar_dispositivo(self, token: str) -> Dispositivo:
        """Autentica un dispositivo por su token"""
        # TODO: Implementar autenticación real
        return None  # Por ahora retornamos None

    def registrar_dispositivo(self, dispositivo: Dispositivo) -> Dispositivo:
        """Registra un nuevo dispositivo"""
        return self.dispositivo_repository.crear(dispositivo)