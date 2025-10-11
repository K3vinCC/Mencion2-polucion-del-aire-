from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base

class UniversidadModel(Base):
    __tablename__ = 'universidades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, unique=True, nullable=False)
    pais = Column(String)
    
    usuarios = relationship("UsuarioModel", back_populates="universidad")
    campus = relationship("CampusModel", back_populates="universidad")