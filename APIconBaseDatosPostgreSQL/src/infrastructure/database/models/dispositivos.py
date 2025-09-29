# src/infrastructure/database/models/dispositivos.py
"""
Modelos de dispositivos y sensores según esquema DBML PostgreSQL.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from .institucional import Base


class ModeloDispositivo(Base):
    """Modelo para tipos/modelos de dispositivos."""
    __tablename__ = 'modelos_dispositivos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_modelo = Column(String(100), unique=True, nullable=False)
    fabricante = Column(String(100))
    especificaciones = Column(Text)

    # Relaciones
    dispositivos = relationship("Dispositivo", back_populates="modelo")

    def __repr__(self):
        return f"<ModeloDispositivo(id={self.id}, nombre='{self.nombre_modelo}')>"


class Dispositivo(Base):
    """Modelo para dispositivos sensores."""
    __tablename__ = 'dispositivos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sala_id = Column(Integer, ForeignKey('salas.id'), nullable=False)
    modelo_id = Column(Integer, ForeignKey('modelos_dispositivos.id'), nullable=False)
    mac_address = Column(String(17), unique=True, nullable=False)  # Formato MAC: XX:XX:XX:XX:XX:XX
    api_token_hash = Column(String(255), nullable=False)
    fecha_instalacion = Column(Date)
    ultimo_mantenimiento = Column(Date)
    estado = Column(String(20), nullable=False, default='desconectado')  # conectado/desconectado
    ultima_vez_visto = Column(DateTime(timezone=True))

    # Relaciones
    sala = relationship("Sala", back_populates="dispositivos")
    modelo = relationship("ModeloDispositivo", back_populates="dispositivos")
    lecturas_temperatura = relationship("LecturaTemperatura", back_populates="dispositivo", cascade="all, delete-orphan")
    lecturas_humedad = relationship("LecturaHumedad", back_populates="dispositivo", cascade="all, delete-orphan")
    lecturas_calidad_aire = relationship("LecturaCalidadAire", back_populates="dispositivo", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Dispositivo(id={self.id}, mac='{self.mac_address}', estado='{self.estado}')>"