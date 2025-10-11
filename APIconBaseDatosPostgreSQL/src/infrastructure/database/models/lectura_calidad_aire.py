# src/infrastructure/database/models/lectura_calidad_aire.py
"""
Modelo SQLAlchemy para LecturaCalidadAire.
"""

from sqlalchemy import Column, Integer, DECIMAL, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class LecturaCalidadAire(Base):
    """Modelo de LecturaCalidadAire para PostgreSQL."""
    __tablename__ = 'lecturas_calidad_aire'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dispositivo_id = Column(Integer, ForeignKey('dispositivos.id'), nullable=False)
    valor_pm1 = Column(DECIMAL(8, 2))
    valor_pm2_5 = Column(DECIMAL(8, 2))
    valor_pm10 = Column(DECIMAL(8, 2))
    etiqueta = Column(String(20))
    fecha_lectura = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    # Relaciones
    dispositivo = relationship("Dispositivo", back_populates="lecturas_calidad_aire")

    def __repr__(self):
        return f"<LecturaCalidadAire(id={self.id}, pm2_5={self.valor_pm2_5})>"