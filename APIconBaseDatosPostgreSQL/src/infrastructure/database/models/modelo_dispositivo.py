# src/infrastructure/database/models/modelo_dispositivo.py
"""
Modelo SQLAlchemy para ModeloDispositivo.
"""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class ModeloDispositivo(Base):
    """Modelo de ModeloDispositivo para PostgreSQL."""
    __tablename__ = 'modelos_dispositivos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_modelo = Column(String(100), nullable=False, unique=True)
    fabricante = Column(String(100))
    especificaciones = Column(Text)

    # Relaciones
    dispositivos = relationship("Dispositivo", back_populates="modelo")

    def __repr__(self):
        return f"<ModeloDispositivo(id={self.id}, nombre='{self.nombre_modelo}')>"