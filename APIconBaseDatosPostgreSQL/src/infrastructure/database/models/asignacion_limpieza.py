# src/infrastructure/database/models/asignacion_limpieza.py
"""
Modelo SQLAlchemy para AsignacionLimpieza.
"""

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class AsignacionLimpieza(Base):
    """Modelo de AsignacionLimpieza para PostgreSQL."""
    __tablename__ = 'asignaciones_limpieza'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sala_id = Column(Integer, ForeignKey('salas.id'), nullable=False)
    asignado_por_usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    asignado_a_usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    estado = Column(String(20), nullable=False, default='pendiente')
    fecha_creacion = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    fecha_completado = Column(TIMESTAMP(timezone=True))

    # Relaciones
    sala = relationship("Sala", back_populates="asignaciones_limpieza")
    usuario_asignador = relationship("Usuario",
                                   foreign_keys=[asignado_por_usuario_id],
                                   back_populates="asignaciones_creadas")
    usuario_limpiador = relationship("Usuario",
                                    foreign_keys=[asignado_a_usuario_id],
                                    back_populates="asignaciones_recibidas")

    def __repr__(self):
        return f"<AsignacionLimpieza(id={self.id}, estado='{self.estado}')>"