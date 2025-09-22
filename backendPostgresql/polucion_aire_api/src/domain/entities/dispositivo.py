from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Dispositivo:
    """Entidad Dispositivo del dominio"""
    id: Optional[int]
    sala_id: int
    modelo_id: int
    id_hardware: str
    api_token_hash: str
    fecha_instalacion: Optional[datetime]
    ultimo_mantenimiento: Optional[datetime]
    estado: str
    ultima_vez_visto: Optional[datetime]

    @property
    def esta_conectado(self) -> bool:
        return self.estado == 'conectado'

    @property
    def necesita_mantenimiento(self) -> bool:
        if not self.ultimo_mantenimiento:
            return True
        dias_desde_mantenimiento = (datetime.now() - self.ultimo_mantenimiento).days
        return dias_desde_mantenimiento > 90  # 3 meses