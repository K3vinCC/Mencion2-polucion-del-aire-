# src/infrastructure/database/models/__init__.py
"""
Modelos de base de datos para el sistema de monitoreo de calidad del aire.
Esquema PostgreSQL según documento maestro DBML.
"""

# Importar Base primero
from .institucional import Base

# Importar todos los modelos
from .institucional import Universidad, Campus, Edificio, Sala
from .usuarios import Rol, Usuario
from .dispositivos import ModeloDispositivo, Dispositivo
from .lecturas import LecturaTemperatura, LecturaHumedad, LecturaCalidadAire
from .operaciones import AsignacionLimpieza

# Exportar todos los modelos
__all__ = [
    'Base',
    'Universidad',
    'Campus', 
    'Edificio',
    'Sala',
    'Rol',
    'Usuario',
    'ModeloDispositivo',
    'Dispositivo',
    'LecturaTemperatura',
    'LecturaHumedad', 
    'LecturaCalidadAire',
    'AsignacionLimpieza'
]
"""
Módulo de modelos de base de datos SQLAlchemy.
"""

from .universidad import Universidad
from .campus import Campus
from .rol import Rol
from .usuario import Usuario
from .edificio import Edificio
from .sala import Sala
from .modelo_dispositivo import ModeloDispositivo
from .dispositivo import Dispositivo
from .lectura_temperatura import LecturaTemperatura
from .lectura_humedad import LecturaHumedad
from .lectura_calidad_aire import LecturaCalidadAire
from .asignacion_limpieza import AsignacionLimpieza

__all__ = [
    'Universidad',
    'Campus',
    'Rol',
    'Usuario',
    'Edificio',
    'Sala',
    'ModeloDispositivo',
    'Dispositivo',
    'LecturaTemperatura',
    'LecturaHumedad',
    'LecturaCalidadAire',
    'AsignacionLimpieza'
]