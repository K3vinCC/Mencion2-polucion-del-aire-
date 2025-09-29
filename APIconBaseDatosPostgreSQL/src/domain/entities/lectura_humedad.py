# src/domain/entities/lectura_humedad.py
"""
Entidad de dominio LecturaHumedad.
Representa una lectura de humedad relativa tomada por un sensor.
"""

from datetime import datetime
from typing import Optional
from decimal import Decimal


class LecturaHumedad:
    """
    Entidad LecturaHumedad del dominio.

    Representa una medición de humedad relativa en porcentaje
    tomada por un dispositivo sensor.
    """

    def __init__(
        self,
        id: Optional[int],
        dispositivo_id: int,
        porcentaje_humedad: Decimal,
        etiqueta: Optional[str] = None,
        fecha_lectura: Optional[datetime] = None
    ):
        """
        Constructor de la entidad LecturaHumedad.

        Args:
            id: Identificador único de la lectura
            dispositivo_id: ID del dispositivo que tomó la lectura
            porcentaje_humedad: Humedad relativa en porcentaje (0-100)
            etiqueta: Etiqueta opcional para categorizar la lectura
            fecha_lectura: Fecha y hora de la lectura
        """
        self.id = id
        self.dispositivo_id = dispositivo_id
        self.porcentaje_humedad = porcentaje_humedad
        self.etiqueta = etiqueta
        self.fecha_lectura = fecha_lectura or datetime.now()

        # Validaciones de negocio
        self._validar_humedad()

    def _validar_humedad(self):
        """Valida que la humedad esté en el rango válido (0-100%)."""
        humedad = float(self.porcentaje_humedad)
        if humedad < 0 or humedad > 100:
            raise ValueError("Humedad fuera de rango válido (0-100%)")

    def get_nivel_confort(self) -> str:
        """
        Determina el nivel de confort basado en la humedad relativa.

        Returns:
            str: Nivel de confort ('MUY_SECO', 'OPTIMO', 'HUMEDO', 'MUY_HUMEDO')
        """
        humedad = float(self.porcentaje_humedad)

        if humedad < 30:
            return 'MUY_SECO'
        elif 30 <= humedad <= 60:
            return 'OPTIMO'
        elif 61 <= humedad <= 80:
            return 'HUMEDO'
        else:
            return 'MUY_HUMEDO'

    def es_humedad_confortable(self) -> bool:
        """
        Determina si la humedad está en el rango de confort (30-60%).

        Returns:
            bool: True si está en rango de confort
        """
        humedad = float(self.porcentaje_humedad)
        return 30 <= humedad <= 60

    def puede_favorecer_moho(self) -> bool:
        """
        Determina si la humedad puede favorecer el crecimiento de moho.

        Returns:
            bool: True si la humedad es alta (>70%)
        """
        humedad = float(self.porcentaje_humedad)
        return humedad > 70

    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario (útil para respuestas JSON).
        """
        return {
            "id": self.id,
            "dispositivo_id": self.dispositivo_id,
            "porcentaje_humedad": float(self.porcentaje_humedad),
            "etiqueta": self.etiqueta,
            "fecha_lectura": self.fecha_lectura.isoformat() if self.fecha_lectura else None,
            "nivel_confort": self.get_nivel_confort(),
            "confortable": self.es_humedad_confortable(),
            "riesgo_moho": self.puede_favorecer_moho()
        }

    def __eq__(self, other):
        """Compara dos lecturas por su ID."""
        if not isinstance(other, LecturaHumedad):
            return False
        return self.id == other.id

    def __hash__(self):
        """Hash basado en el ID para usar en sets y diccionarios."""
        return hash(self.id)

    def __repr__(self):
        """Representación string de la lectura."""
        return f"LecturaHumedad(id={self.id}, dispositivo_id={self.dispositivo_id}, humedad={self.porcentaje_humedad}%)"