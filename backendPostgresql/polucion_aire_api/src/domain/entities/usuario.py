from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Usuario:
    """Entidad Usuario del dominio"""
    id: Optional[int]
    email: str
    nombre_completo: str
    rol_id: int
    universidad_id: Optional[int]
    fecha_creacion: datetime
    clave_hash: str = None  # Solo se usa para crear/actualizar

    @property
    def es_super_admin(self) -> bool:
        return self.rol_id == 1  # ID del rol SuperAdmin

    @property
    def es_admin_universidad(self) -> bool:
        return self.rol_id == 2  # ID del rol Admin_Universidad