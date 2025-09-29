# src/infrastructure/database/models/lectura_temperatura.py
"""
Modelo SQLAlchemy para LecturaTemperatura.
"""

from sqlalchemy import Column, Integer, DECIMAL, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class LecturaTemperatura(Base):
    """Modelo de LecturaTemperatura para PostgreSQL."""
    __tablename__ = 'lecturas_temperatura'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dispositivo_id = Column(Integer, ForeignKey('dispositivos.id'), nullable=False)
    grados_temperatura = Column(DECIMAL(5, 2), nullable=False)
    etiqueta = Column(String(20))
    fecha_lectura = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    # Relaciones
    dispositivo = relationship("Dispositivo", back_populates="lecturas_temperatura")

    def __repr__(self):
        return f"<LecturaTemperatura(id={self.id}, temperatura={self.grados_temperatura}°C)>"