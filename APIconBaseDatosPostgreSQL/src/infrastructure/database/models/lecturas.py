# src/infrastructure/database/models/lecturas.py
"""
Modelos de lecturas de sensores según esquema DBML PostgreSQL.
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .institucional import Base


class LecturaTemperatura(Base):
    """Modelo para lecturas de temperatura."""
    __tablename__ = 'lecturas_temperatura'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dispositivo_id = Column(Integer, ForeignKey('dispositivos.id'), nullable=False)
    grados_temperatura = Column(Numeric(5, 2), nullable=False)  # Decimal(5,2) en PostgreSQL
    etiqueta = Column(String(20))  # Ej: "Normal", "Alto", "Crítico"
    fecha_lectura = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relaciones
    dispositivo = relationship("Dispositivo", back_populates="lecturas_temperatura")

    def __repr__(self):
        return f"<LecturaTemperatura(id={self.id}, temp={self.grados_temperatura}°C, etiqueta='{self.etiqueta}')>"


class LecturaHumedad(Base):
    """Modelo para lecturas de humedad."""
    __tablename__ = 'lecturas_humedad'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dispositivo_id = Column(Integer, ForeignKey('dispositivos.id'), nullable=False)
    porcentaje_humedad = Column(Numeric(5, 2), nullable=False)  # Decimal(5,2) en PostgreSQL
    etiqueta = Column(String(20))  # Ej: "Normal", "Alto", "Bajo"
    fecha_lectura = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relaciones
    dispositivo = relationship("Dispositivo", back_populates="lecturas_humedad")

    def __repr__(self):
        return f"<LecturaHumedad(id={self.id}, humedad={self.porcentaje_humedad}%, etiqueta='{self.etiqueta}')>"


class LecturaCalidadAire(Base):
    """Modelo para lecturas de calidad del aire (material particulado)."""
    __tablename__ = 'lecturas_calidad_aire'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dispositivo_id = Column(Integer, ForeignKey('dispositivos.id'), nullable=False)
    valor_pm1 = Column(Numeric(8, 2))  # Partículas PM1.0
    valor_pm2_5 = Column(Numeric(8, 2))  # Partículas PM2.5
    valor_pm10 = Column(Numeric(8, 2))  # Partículas PM10
    etiqueta = Column(String(20))  # Ej: "Bueno", "Moderado", "Nocivo", "Insalubre", "Muy Insalubre", "Peligroso"
    fecha_lectura = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relaciones
    dispositivo = relationship("Dispositivo", back_populates="lecturas_calidad_aire")

    def __repr__(self):
        return f"<LecturaCalidadAire(id={self.id}, PM2.5={self.valor_pm2_5}, etiqueta='{self.etiqueta}')>"