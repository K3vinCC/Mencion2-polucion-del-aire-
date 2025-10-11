# src/infrastructure/database/models/edificio.py
"""
Modelo SQLAlchemy para Edificio.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class Edificio(Base):
    """Modelo de Edificio para PostgreSQL."""
    __tablename__ = 'edificios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    campus_id = Column(Integer, ForeignKey('campus.id'), nullable=False)
    nombre = Column(String(100), nullable=False)

    # Relaciones
    campus = relationship("Campus", back_populates="edificios")
    salas = relationship("Sala", back_populates="edificio")

    # Índice único compuesto
    __table_args__ = (
        {'schema': None}
    )

    def __repr__(self):
        return f"<Edificio(id={self.id}, nombre='{self.nombre}')>"