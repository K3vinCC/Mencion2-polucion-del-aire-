# src/domain/entities/lectura_temperatura.py
"""
Entidad de dominio LecturaTemperatura.
Representa una lectura de temperatura tomada por un sensor.
"""

from datetime import datetime
from typing import Optional
from decimal import Decimal


class LecturaTemperatura:
    """
    Entidad LecturaTemperatura del dominio.

    Representa una medición de temperatura en grados Celsius
    tomada por un dispositivo sensor.
    """

    def __init__(
        self,
        id: Optional[int],
        dispositivo_id: int,
        grados_temperatura: Decimal,
        etiqueta: Optional[str] = None,
        fecha_lectura: Optional[datetime] = None
    ):
        """
        Constructor de la entidad LecturaTemperatura.

        Args:
            id: Identificador único de la lectura
            dispositivo_id: ID del dispositivo que tomó la lectura
            grados_temperatura: Temperatura en grados Celsius
            etiqueta: Etiqueta opcional para categorizar la lectura
            fecha_lectura: Fecha y hora de la lectura
        """
        self.id = id
        self.dispositivo_id = dispositivo_id
        self.grados_temperatura = grados_temperatura
        self.etiqueta = etiqueta
        self.fecha_lectura = fecha_lectura or datetime.now()

        # Validaciones de negocio
        self._validar_temperatura()

    def _validar_temperatura(self):
        """Valida que la temperatura esté en un rango razonable."""
        temp = float(self.grados_temperatura)
        if temp < -50 or temp > 60:  # Rangos extremos para ambientes controlados
            raise ValueError("Temperatura fuera de rango válido (-50°C a 60°C)")

    def get_nivel_confort(self) -> str:
        """
        Determina el nivel de confort térmico basado en la temperatura.

        Returns:
            str: Nivel de confort ('FRIO', 'OPTIMO', 'CALUROSO')
        """
        temp = float(self.grados_temperatura)

        if temp < 18:
            return 'FRIO'
        elif 18 <= temp <= 24:
            return 'OPTIMO'
        else:
            return 'CALUROSO'

    def es_temperatura_confortable(self) -> bool:
        """
        Determina si la temperatura está en el rango de confort (18-24°C).

        Returns:
            bool: True si está en rango de confort
        """
        temp = float(self.grados_temperatura)
        return 18 <= temp <= 24

    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario (útil para respuestas JSON).
        """
        return {
            "id": self.id,
            "dispositivo_id": self.dispositivo_id,
            "grados_temperatura": float(self.grados_temperatura),
            "etiqueta": self.etiqueta,
            "fecha_lectura": self.fecha_lectura.isoformat() if self.fecha_lectura else None,
            "nivel_confort": self.get_nivel_confort(),
            "confortable": self.es_temperatura_confortable()
        }

    def __eq__(self, other):
        """Compara dos lecturas por su ID."""
        if not isinstance(other, LecturaTemperatura):
            return False
        return self.id == other.id

    def __hash__(self):
        """Hash basado en el ID para usar en sets y diccionarios."""
        return hash(self.id)

    def __repr__(self):
        """Representación string de la lectura."""
        return f"LecturaTemperatura(id={self.id}, dispositivo_id={self.dispositivo_id}, temperatura={self.grados_temperatura}°C)"