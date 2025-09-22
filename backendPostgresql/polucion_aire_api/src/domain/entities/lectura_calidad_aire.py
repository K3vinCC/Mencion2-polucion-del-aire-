from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class LecturaCalidadAire:
    """Entidad Lectura de Calidad del Aire del dominio"""
    id: Optional[int]
    dispositivo_id: int
    valor_pm1: Optional[float]
    valor_pm2_5: Optional[float]
    valor_pm10: Optional[float]
    etiqueta: Optional[str]
    fecha_lectura: datetime

    def get_nivel_calidad(self) -> str:
        """Determina el nivel de calidad del aire basado en PM2.5"""
        if not self.valor_pm2_5:
            return "No disponible"
        
        if self.valor_pm2_5 <= 12:
            return "Bueno"
        elif self.valor_pm2_5 <= 35.4:
            return "Moderado"
        elif self.valor_pm2_5 <= 55.4:
            return "Nocivo"
        elif self.valor_pm2_5 <= 150.4:
            return "Insalubre"
        elif self.valor_pm2_5 <= 250.4:
            return "Muy Insalubre"
        else:
            return "Peligroso"

    def requiere_accion(self) -> bool:
        """Determina si la lectura requiere una acción de limpieza"""
        return self.get_nivel_calidad() in ["Nocivo", "Insalubre", "Muy Insalubre", "Peligroso"]