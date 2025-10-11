from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base

class EdificioModel(Base):
    __tablename__ = 'edificios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    campus_id = Column(Integer, ForeignKey('campus.id'), nullable=False)
    nombre = Column(String, nullable=False)

    campus = relationship("CampusModel", back_populates="edificios")
    salas = relationship("SalaModel", back_populates="edificio")