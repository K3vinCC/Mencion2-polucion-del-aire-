# src/infrastructure/database/models/rol.py
"""
Modelo SQLAlchemy para Rol.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class Rol(Base):
    """Modelo de Rol para PostgreSQL."""
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)

    # Relaciones
    usuarios = relationship("Usuario", back_populates="rol")

    def __repr__(self):
        return f"<Rol(id={self.id}, nombre='{self.nombre}')>"