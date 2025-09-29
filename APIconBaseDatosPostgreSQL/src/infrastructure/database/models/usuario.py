# src/infrastructure/database/models/usuario.py
"""
Modelo SQLAlchemy para Usuario.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class Usuario(Base):
    """Modelo de Usuario para PostgreSQL."""
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    clave_hash = Column(String(255), nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    rol_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    universidad_id = Column(Integer, ForeignKey('universidades.id'))
    campus_id = Column(Integer, ForeignKey('campus.id'))
    fecha_creacion = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relaciones
    rol = relationship("Rol", back_populates="usuarios")
    universidad = relationship("Universidad", back_populates="usuarios")
    campus = relationship("Campus", back_populates="usuarios")
    asignaciones_creadas = relationship("AsignacionLimpieza",
                                       foreign_keys="AsignacionLimpieza.asignado_por_usuario_id",
                                       back_populates="usuario_asignador")
    asignaciones_recibidas = relationship("AsignacionLimpieza",
                                         foreign_keys="AsignacionLimpieza.asignado_a_usuario_id",
                                         back_populates="usuario_limpiador")

    def __repr__(self):
        return f"<Usuario(id={self.id}, email='{self.email}', rol_id={self.rol_id})>"