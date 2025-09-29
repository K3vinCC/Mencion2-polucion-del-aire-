# src/domain/entities/dispositivo.py
"""
Entidad de dominio Dispositivo.
Representa un sensor físico con sus atributos y reglas de negocio.
"""

from datetime import datetime
from typing import Optional
import re


class Dispositivo:
    """
    Entidad Dispositivo del dominio.

    Representa un sensor físico (ESP32) que mide calidad del aire,
    temperatura y humedad en una sala específica.
    """

    def __init__(
        self,
        id: Optional[int],
        sala_id: int,
        modelo_id: int,
        mac_address: str,
        api_token_hash: str,
        fecha_instalacion: Optional[datetime] = None,
        ultimo_mantenimiento: Optional[datetime] = None,
        estado: str = "desconectado",
        ultima_vez_visto: Optional[datetime] = None
    ):
        """
        Constructor de la entidad Dispositivo.

        Args:
            id: Identificador único del dispositivo
            sala_id: ID de la sala donde está instalado
            modelo_id: ID del modelo del dispositivo
            mac_address: Dirección MAC del dispositivo (formato XX:XX:XX:XX:XX:XX)
            api_token_hash: Hash del token API para autenticación
            fecha_instalacion: Fecha de instalación del dispositivo
            ultimo_mantenimiento: Fecha del último mantenimiento
            estado: Estado del dispositivo ('conectado' o 'desconectado')
            ultima_vez_visto: Última vez que el dispositivo envió datos
        """
        self.id = id
        self.sala_id = sala_id
        self.modelo_id = modelo_id
        self.mac_address = mac_address.upper()  # Normalizar a mayúsculas
        self.api_token_hash = api_token_hash
        self.fecha_instalacion = fecha_instalacion
        self.ultimo_mantenimiento = ultimo_mantenimiento
        self.estado = estado
        self.ultima_vez_visto = ultima_vez_visto

        # Validaciones de negocio
        self._validar_mac_address()
        self._validar_estado()

    def _validar_mac_address(self):
        """Valida que la dirección MAC tenga el formato correcto."""
        mac_pattern = re.compile(r'^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$')
        if not mac_pattern.match(self.mac_address):
            raise ValueError("Dirección MAC inválida. Debe tener formato XX:XX:XX:XX:XX:XX")

    def _validar_estado(self):
        """Valida que el estado sea uno de los permitidos."""
        estados_validos = ['conectado', 'desconectado']
        if self.estado not in estados_validos:
            raise ValueError(f"Estado inválido. Debe ser uno de: {estados_validos}")

    def esta_conectado(self) -> bool:
        """Verifica si el dispositivo está conectado."""
        return self.estado == 'conectado'

    def marcar_como_conectado(self):
        """Marca el dispositivo como conectado y actualiza la última vez visto."""
        self.estado = 'conectado'
        self.ultima_vez_visto = datetime.now()

    def marcar_como_desconectado(self):
        """Marca el dispositivo como desconectado."""
        self.estado = 'desconectado'

    def actualizar_ultima_vez_visto(self):
        """Actualiza la timestamp de última vez visto."""
        self.ultima_vez_visto = datetime.now()

    def necesita_mantenimiento(self) -> bool:
        """
        Determina si el dispositivo necesita mantenimiento.
        Regla de negocio: si han pasado más de 6 meses desde el último mantenimiento.
        """
        if not self.ultimo_mantenimiento:
            return True

        seis_meses = 6 * 30 * 24 * 60 * 60  # 6 meses en segundos
        tiempo_transcurrido = (datetime.now() - self.ultimo_mantenimiento).total_seconds()

        return tiempo_transcurrido > seis_meses

    def verificar_token(self, token_proporcionado: str) -> bool:
        """
        Verifica si el token proporcionado coincide con el hash almacenado.

        Args:
            token_proporcionado: Token en texto plano proporcionado por el dispositivo

        Returns:
            bool: True si el token es válido
        """
        import bcrypt
        try:
            return bcrypt.checkpw(
                token_proporcionado.encode('utf-8'),
                self.api_token_hash.encode('utf-8')
            )
        except Exception:
            return False

    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario (útil para respuestas JSON).

        Excluye información sensible como el hash del token API.
        """
        return {
            "id": self.id,
            "sala_id": self.sala_id,
            "modelo_id": self.modelo_id,
            "mac_address": self.mac_address,
            "fecha_instalacion": self.fecha_instalacion.isoformat() if self.fecha_instalacion else None,
            "ultimo_mantenimiento": self.ultimo_mantenimiento.isoformat() if self.ultimo_mantenimiento else None,
            "estado": self.estado,
            "ultima_vez_visto": self.ultima_vez_visto.isoformat() if self.ultima_vez_visto else None,
            "necesita_mantenimiento": self.necesita_mantenimiento()
        }

    def __eq__(self, other):
        """Compara dos dispositivos por su ID."""
        if not isinstance(other, Dispositivo):
            return False
        return self.id == other.id

    def __hash__(self):
        """Hash basado en el ID para usar en sets y diccionarios."""
        return hash(self.id)

    def __repr__(self):
        """Representación string del dispositivo."""
        return f"Dispositivo(id={self.id}, mac='{self.mac_address}', estado='{self.estado}')"