# src/infrastructure/database/models/campus.py
"""
Modelo SQLAlchemy para Campus.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class Campus(Base):
    """Modelo de Campus para PostgreSQL."""
    __tablename__ = 'campus'

    id = Column(Integer, primary_key=True, autoincrement=True)
    universidad_id = Column(Integer, ForeignKey('universidades.id'), nullable=False)
    nombre = Column(String(150), nullable=False)
    direccion = Column(Text)

    # Relaciones
    universidad = relationship("Universidad", back_populates="campus")
    edificios = relationship("Edificio", back_populates="campus")
    usuarios = relationship("Usuario", back_populates="campus")

    def __repr__(self):
        return f"<Campus(id={self.id}, nombre='{self.nombre}')>"