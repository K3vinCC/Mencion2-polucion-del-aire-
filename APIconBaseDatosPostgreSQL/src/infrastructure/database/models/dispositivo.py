# src/infrastructure/database/models/dispositivo.py
"""
Modelo SQLAlchemy para Dispositivo.
"""

from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class Dispositivo(Base):
    """Modelo de Dispositivo para PostgreSQL."""
    __tablename__ = 'dispositivos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sala_id = Column(Integer, ForeignKey('salas.id'), nullable=False)
    modelo_id = Column(Integer, ForeignKey('modelos_dispositivos.id'), nullable=False)
    mac_address = Column(String(17), nullable=False, unique=True)
    api_token_hash = Column(String(255), nullable=False)
    fecha_instalacion = Column(Date)
    ultimo_mantenimiento = Column(Date)
    estado = Column(String(20), nullable=False, default='desconectado')
    ultima_vez_visto = Column(TIMESTAMP(timezone=True))

    # Relaciones
    sala = relationship("Sala", back_populates="dispositivos")
    modelo = relationship("ModeloDispositivo", back_populates="dispositivos")
    lecturas_temperatura = relationship("LecturaTemperatura", back_populates="dispositivo")
    lecturas_humedad = relationship("LecturaHumedad", back_populates="dispositivo")
    lecturas_calidad_aire = relationship("LecturaCalidadAire", back_populates="dispositivo")

    def __repr__(self):
        return f"<Dispositivo(id={self.id}, mac='{self.mac_address}', estado='{self.estado}')>"