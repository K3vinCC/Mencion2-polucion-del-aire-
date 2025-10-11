# src/infrastructure/database/models/operaciones.py
"""
Modelos de operaciones del sistema según esquema DBML PostgreSQL.
"""

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .institucional import Base


class AsignacionLimpieza(Base):
    """Modelo para asignaciones de limpieza."""
    __tablename__ = 'asignaciones_limpieza'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sala_id = Column(Integer, ForeignKey('salas.id'), nullable=False)
    asignado_por_usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    asignado_a_usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    estado = Column(String(20), nullable=False, default='pendiente')  # pendiente/en_progreso/completado/cancelado
    fecha_creacion = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    fecha_completado = Column(DateTime(timezone=True))

    # Relaciones
    sala = relationship("Sala", back_populates="asignaciones_limpieza")
    asignado_por = relationship(
        "Usuario", 
        foreign_keys=[asignado_por_usuario_id],
        back_populates="asignaciones_creadas"
    )
    asignado_a = relationship(
        "Usuario",
        foreign_keys=[asignado_a_usuario_id], 
        back_populates="asignaciones_recibidas"
    )

    def __repr__(self):
        return f"<AsignacionLimpieza(id={self.id}, sala_id={self.sala_id}, estado='{self.estado}')>"