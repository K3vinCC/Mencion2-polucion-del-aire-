from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base

class DispositivoModel(Base):
    """Modelo SQLAlchemy para la tabla dispositivos"""
    __tablename__ = 'dispositivos'
    
    id = Column(Integer, primary_key=True)
    sala_id = Column(Integer, ForeignKey('salas.id'), nullable=False)
    modelo_id = Column(Integer, ForeignKey('modelos_dispositivos.id'), nullable=False)
    id_hardware = Column(String(100), unique=True, nullable=False)
    api_token_hash = Column(String(255), nullable=False)
    fecha_instalacion = Column(DateTime)
    ultimo_mantenimiento = Column(DateTime)
    estado = Column(String(20), nullable=False, default='desconectado')
    ultima_vez_visto = Column(DateTime)

    sala = relationship("SalaModel", back_populates="dispositivos")
    modelo = relationship("ModeloDispositivoModel", back_populates="dispositivos")