# src/application/use_cases/registrar_dispositivo.py
"""
Caso de uso: Registrar Dispositivo
Permite registrar nuevos dispositivos sensores en el sistema.
"""

import secrets
import bcrypt
from src.domain.ports.dispositivo_repository import IDispositivoRepository
from src.domain.entities.dispositivo import Dispositivo


class RegistrarDispositivo:
    """
    Caso de uso para registrar nuevos dispositivos sensores.

    Maneja la creación de dispositivos con validación de MAC address,
    generación de tokens API y asignación a salas.
    """

    def __init__(self, dispositivo_repository: IDispositivoRepository):
        """
        Constructor del caso de uso.

        Args:
            dispositivo_repository: Repositorio de dispositivos inyectado
        """
        self.dispositivo_repository = dispositivo_repository

    def ejecutar(
        self,
        mac_address: str,
        modelo_id: int,
        sala_id: int,
        fecha_instalacion=None
    ) -> tuple[Dispositivo, str]:
        """
        Ejecuta el registro de un nuevo dispositivo.

        Args:
            mac_address: Dirección MAC del dispositivo (formato XX:XX:XX:XX:XX:XX)
            modelo_id: ID del modelo del dispositivo
            sala_id: ID de la sala donde se instalará
            fecha_instalacion: Fecha de instalación (opcional, por defecto hoy)

        Returns:
            tuple: (Dispositivo creado, token_API generado)

        Raises:
            ValueError: Si los datos son inválidos o ya existe un dispositivo con esa MAC
        """
        # Validar datos de entrada
        self._validar_datos(mac_address, modelo_id, sala_id)

        # Verificar que no exista un dispositivo con la misma MAC
        dispositivo_existente = self.dispositivo_repository.find_by_mac(mac_address)
        if dispositivo_existente:
            raise ValueError("Ya existe un dispositivo registrado con esta dirección MAC")

        # Generar token API único y seguro
        api_token = self._generar_api_token()
        api_token_hash = self._generar_api_token_hash(api_token)

        # Crear entidad de dispositivo
        nuevo_dispositivo = Dispositivo(
            id=None,
            sala_id=sala_id,
            modelo_id=modelo_id,
            mac_address=mac_address,
            api_token_hash=api_token_hash,
            fecha_instalacion=fecha_instalacion,
            ultimo_mantenimiento=None,
            estado='desconectado',
            ultima_vez_visto=None
        )

        # Guardar en el repositorio
        dispositivo_creado = self.dispositivo_repository.save(nuevo_dispositivo)

        return dispositivo_creado, api_token

    def _validar_datos(self, mac_address: str, modelo_id: int, sala_id: int):
        """
        Valida los datos de entrada según reglas de negocio.

        Args:
            mac_address: Dirección MAC a validar
            modelo_id: ID del modelo a validar
            sala_id: ID de la sala a validar

        Raises:
            ValueError: Si algún dato es inválido
        """
        # Validar MAC address (ya se valida en la entidad, pero verificamos aquí también)
        if not mac_address:
            raise ValueError("La dirección MAC es requerida")

        # Normalizar MAC address
        mac_normalizada = mac_address.upper().replace('-', ':')
        if not self._es_mac_valida(mac_normalizada):
            raise ValueError("Formato de dirección MAC inválido. Use formato XX:XX:XX:XX:XX:XX")

        # Validar modelo_id
        if not modelo_id or modelo_id <= 0:
            raise ValueError("El ID del modelo debe ser un número positivo")

        # Validar sala_id
        if not sala_id or sala_id <= 0:
            raise ValueError("El ID de la sala debe ser un número positivo")

    def _es_mac_valida(self, mac: str) -> bool:
        """
        Verifica si una dirección MAC tiene el formato correcto.

        Args:
            mac: Dirección MAC a validar

        Returns:
            bool: True si el formato es válido
        """
        import re
        mac_pattern = re.compile(r'^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$')
        return mac_pattern.match(mac) is not None

    def _generar_api_token(self) -> str:
        """
        Genera un token API único y seguro.

        Returns:
            str: Token API de 64 caracteres hexadecimales
        """
        return secrets.token_hex(32)  # 64 caracteres hexadecimales

    def _generar_api_token_hash(self, token: str) -> str:
        """
        Genera un hash seguro del token API para almacenamiento.

        Args:
            token: Token API en texto plano

        Returns:
            str: Hash del token
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(token.encode('utf-8'), salt)
        return hashed.decode('utf-8')