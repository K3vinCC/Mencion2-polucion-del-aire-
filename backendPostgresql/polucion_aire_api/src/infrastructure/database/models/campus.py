from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base

class CampusModel(Base):
    __tablename__ = 'campus'

    id = Column(Integer, primary_key=True, autoincrement=True)
    universidad_id = Column(Integer, ForeignKey('universidades.id'), nullable=False)
    nombre = Column(String, nullable=False)
    direccion = Column(String)

    universidad = relationship("UniversidadModel", back_populates="campus")
    edificios = relationship("EdificioModel", back_populates="campus")