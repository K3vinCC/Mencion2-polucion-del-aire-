# src/domain/entities/lectura_calidad_aire.py
"""
Entidad de dominio LecturaCalidadAire.
Representa una lectura de calidad del aire tomada por un sensor.
"""

from datetime import datetime
from typing import Optional
from decimal import Decimal


class LecturaCalidadAire:
    """
    Entidad LecturaCalidadAire del dominio.

    Representa una medición de calidad del aire (PM1, PM2.5, PM10)
    tomada por un dispositivo sensor en un momento específico.
    """

    # Definición de rangos de calidad del aire según estándares
    RANGOS_CALIDAD = {
        'BUENO': {'min': 0, 'max': 12, 'color': '#27B500'},
        'MODERADO': {'min': 13, 'max': 35, 'color': '#DFD922'},
        'NOCIVO': {'min': 36, 'max': 55, 'color': '#DF7A22'},
        'INSALUBRE': {'min': 56, 'max': 150, 'color': '#DB3737'},
        'MUY_INSALUBRE': {'min': 151, 'max': 250, 'color': '#9C4AD3'},
        'PELIGROSO': {'min': 251, 'max': float('inf'), 'color': '#6D0815'}
    }

    def __init__(
        self,
        id: Optional[int],
        dispositivo_id: int,
        valor_pm1: Optional[Decimal] = None,
        valor_pm2_5: Optional[Decimal] = None,
        valor_pm10: Optional[Decimal] = None,
        etiqueta: Optional[str] = None,
        fecha_lectura: Optional[datetime] = None
    ):
        """
        Constructor de la entidad LecturaCalidadAire.

        Args:
            id: Identificador único de la lectura
            dispositivo_id: ID del dispositivo que tomó la lectura
            valor_pm1: Valor de PM1 (partículas de 1 micrómetro)
            valor_pm2_5: Valor de PM2.5 (partículas de 2.5 micrómetros)
            valor_pm10: Valor de PM10 (partículas de 10 micrómetros)
            etiqueta: Etiqueta opcional para categorizar la lectura
            fecha_lectura: Fecha y hora de la lectura
        """
        self.id = id
        self.dispositivo_id = dispositivo_id
        self.valor_pm1 = valor_pm1
        self.valor_pm2_5 = valor_pm2_5
        self.valor_pm10 = valor_pm10
        self.etiqueta = etiqueta
        self.fecha_lectura = fecha_lectura or datetime.now()

        # Validaciones de negocio
        self._validar_valores()

    def _validar_valores(self):
        """Valida que los valores de PM sean positivos cuando están presentes."""
        valores_pm = [self.valor_pm1, self.valor_pm2_5, self.valor_pm10]

        for valor in valores_pm:
            if valor is not None and valor < 0:
                raise ValueError("Los valores de PM no pueden ser negativos")

    def get_nivel_calidad(self) -> str:
        """
        Determina el nivel de calidad del aire basado en el valor PM2.5.

        Returns:
            str: Nivel de calidad ('BUENO', 'MODERADO', 'NOCIVO', etc.)
        """
        if self.valor_pm2_5 is None:
            return 'DESCONOCIDO'

        valor = float(self.valor_pm2_5)

        for nivel, rango in self.RANGOS_CALIDAD.items():
            if rango['min'] <= valor <= rango['max']:
                return nivel

        return 'PELIGROSO'  # Por si acaso está por encima del último rango

    def get_color_calidad(self) -> str:
        """
        Obtiene el color correspondiente al nivel de calidad del aire.

        Returns:
            str: Código de color hexadecimal
        """
        nivel = self.get_nivel_calidad()
        return self.RANGOS_CALIDAD.get(nivel, {}).get('color', '#000000')

    def es_calidad_aceptable(self) -> bool:
        """
        Determina si la calidad del aire es aceptable (BUENO o MODERADO).

        Returns:
            bool: True si la calidad es aceptable
        """
        nivel = self.get_nivel_calidad()
        return nivel in ['BUENO', 'MODERADO']

    def requiere_accion_inmediata(self) -> bool:
        """
        Determina si la calidad del aire requiere acción inmediata.

        Returns:
            bool: True si requiere acción (NOCIVO o peor)
        """
        nivel = self.get_nivel_calidad()
        return nivel in ['NOCIVO', 'INSALUBRE', 'MUY_INSALUBRE', 'PELIGROSO']

    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario (útil para respuestas JSON).
        """
        return {
            "id": self.id,
            "dispositivo_id": self.dispositivo_id,
            "valor_pm1": float(self.valor_pm1) if self.valor_pm1 else None,
            "valor_pm2_5": float(self.valor_pm2_5) if self.valor_pm2_5 else None,
            "valor_pm10": float(self.valor_pm10) if self.valor_pm10 else None,
            "etiqueta": self.etiqueta,
            "fecha_lectura": self.fecha_lectura.isoformat() if self.fecha_lectura else None,
            "nivel_calidad": self.get_nivel_calidad(),
            "color_calidad": self.get_color_calidad(),
            "calidad_aceptable": self.es_calidad_aceptable(),
            "requiere_accion": self.requiere_accion_inmediata()
        }

    def __eq__(self, other):
        """Compara dos lecturas por su ID."""
        if not isinstance(other, LecturaCalidadAire):
            return False
        return self.id == other.id

    def __hash__(self):
        """Hash basado en el ID para usar en sets y diccionarios."""
        return hash(self.id)

    def __repr__(self):
        """Representación string de la lectura."""
        return f"LecturaCalidadAire(id={self.id}, dispositivo_id={self.dispositivo_id}, pm2_5={self.valor_pm2_5}, nivel='{self.get_nivel_calidad()}')"