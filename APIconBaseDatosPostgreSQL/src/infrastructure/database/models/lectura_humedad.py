# src/infrastructure/database/models/lectura_humedad.py
"""
Modelo SQLAlchemy para LecturaHumedad.
"""

from sqlalchemy import Column, Integer, DECIMAL, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class LecturaHumedad(Base):
    """Modelo de LecturaHumedad para PostgreSQL."""
    __tablename__ = 'lecturas_humedad'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dispositivo_id = Column(Integer, ForeignKey('dispositivos.id'), nullable=False)
    porcentaje_humedad = Column(DECIMAL(5, 2), nullable=False)
    etiqueta = Column(String(20))
    fecha_lectura = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    # Relaciones
    dispositivo = relationship("Dispositivo", back_populates="lecturas_humedad")

    def __repr__(self):
        return f"<LecturaHumedad(id={self.id}, humedad={self.porcentaje_humedad}%)>"