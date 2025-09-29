# src/infrastructure/database/models/usuarios.py
"""
Modelos de autenticación y usuarios según esquema DBML PostgreSQL.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .institucional import Base


class Rol(Base):
    """Modelo para roles de usuario."""
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False)
    # Ej: "SuperAdmin", "Admin_Universidad", "Conserje", "Limpiador"

    # Relaciones
    usuarios = relationship("Usuario", back_populates="rol")

    def __repr__(self):
        return f"<Rol(id={self.id}, nombre='{self.nombre}')>"


class Usuario(Base):
    """Modelo para usuarios del sistema."""
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    clave_hash = Column(String(255), nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    rol_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    universidad_id = Column(Integer, ForeignKey('universidades.id'))
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    rol = relationship("Rol", back_populates="usuarios")
    universidad = relationship("Universidad", back_populates="usuarios")
    asignaciones_creadas = relationship(
        "AsignacionLimpieza", 
        foreign_keys="AsignacionLimpieza.asignado_por_usuario_id",
        back_populates="asignado_por"
    )
    asignaciones_recibidas = relationship(
        "AsignacionLimpieza",
        foreign_keys="AsignacionLimpieza.asignado_a_usuario_id", 
        back_populates="asignado_a"
    )

    def __repr__(self):
        return f"<Usuario(id={self.id}, email='{self.email}', rol='{self.rol.nombre if self.rol else None}')>"