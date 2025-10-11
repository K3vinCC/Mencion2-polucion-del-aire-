# src/infrastructure/database/models/sala.py
"""
Modelo SQLAlchemy para Sala.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class Sala(Base):
    """Modelo de Sala para PostgreSQL."""
    __tablename__ = 'salas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    edificio_id = Column(Integer, ForeignKey('edificios.id'), nullable=False)
    piso = Column(Integer)
    nombre_o_numero = Column(String(50), nullable=False)
    descripcion = Column(Text)

    # Relaciones
    edificio = relationship("Edificio", back_populates="salas")
    dispositivos = relationship("Dispositivo", back_populates="sala")
    asignaciones_limpieza = relationship("AsignacionLimpieza", back_populates="sala")

    # Índice único compuesto
    __table_args__ = (
        {'schema': None}
    )

    def __repr__(self):
        return f"<Sala(id={self.id}, nombre='{self.nombre_o_numero}')>"