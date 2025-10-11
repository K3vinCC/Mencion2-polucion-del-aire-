# src/application/use_cases/registrar_dispositivo.py
import secrets
from src.domain.entities.dispositivo import Dispositivo
from src.domain.ports.dispositivo_repository import IDispositivoRepository

class RegistrarDispositivo:
    """
    Caso de Uso: Registrar un nuevo dispositivo.
    """

    def __init__(self, dispositivo_repository: IDispositivoRepository):
        self.dispositivo_repository = dispositivo_repository

    def ejecutar(self, nombre, ubicacion, id_edificio, estado='activo'):
        """
        Registra un nuevo dispositivo con un token de acceso único.

        Args:
            nombre (str): Nombre del dispositivo.
            ubicacion (str): Ubicación del dispositivo.
            id_edificio (int): ID del edificio.
            estado (str): Estado inicial del dispositivo.

        Returns:
            Dispositivo: La entidad del dispositivo recién creado.
        """
        # Generar token único para el dispositivo
        token_acceso = secrets.token_urlsafe(32)

        nuevo_dispositivo = Dispositivo(
            id=None,
            nombre=nombre,
            ubicacion=ubicacion,
            token_acceso=token_acceso,
            id_edificio=id_edificio,
            estado=estado
        )

        dispositivo_creado = self.dispositivo_repository.save(nuevo_dispositivo)
        return dispositivo_creado