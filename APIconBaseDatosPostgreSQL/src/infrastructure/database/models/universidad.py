# src/infrastructure/database/models/universidad.py
"""
Modelo SQLAlchemy para Universidad.
"""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class Universidad(Base):
    """Modelo de Universidad para PostgreSQL."""
    __tablename__ = 'universidades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False, unique=True)
    pais = Column(String(100))

    # Relaciones
    campus = relationship("Campus", back_populates="universidad")
    usuarios = relationship("Usuario", back_populates="universidad")

    def __repr__(self):
        return f"<Universidad(id={self.id}, nombre='{self.nombre}')>"