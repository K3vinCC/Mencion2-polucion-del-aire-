from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base

class UsuarioModel(Base):
    """Modelo SQLAlchemy para la tabla usuarios"""
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    clave_hash = Column(String(255), nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    rol_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    universidad_id = Column(Integer, ForeignKey('universidades.id'))
    fecha_creacion = Column(DateTime, server_default=func.now())
    
    rol = relationship("RolModel", back_populates="usuarios")
    universidad = relationship("UniversidadModel", back_populates="usuarios")