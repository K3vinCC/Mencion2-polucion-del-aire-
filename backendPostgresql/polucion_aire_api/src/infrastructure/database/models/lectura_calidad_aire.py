from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.infrastructure.database.database import Base

class LecturaCalidadAireModel(Base):
    """Modelo SQLAlchemy para la tabla lecturas_calidad_aire"""
    __tablename__ = 'lecturas_calidad_aire'
    
    id = Column(Integer, primary_key=True)
    dispositivo_id = Column(Integer, ForeignKey('dispositivos.id'), nullable=False)
    valor_pm1 = Column(Float)
    valor_pm2_5 = Column(Float)
    valor_pm10 = Column(Float)
    etiqueta = Column(String(20))
    fecha_lectura = Column(DateTime, nullable=False, default=func.now())