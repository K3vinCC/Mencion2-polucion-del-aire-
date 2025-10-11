from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base

class SalaModel(Base):
    __tablename__ = 'salas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    edificio_id = Column(Integer, ForeignKey('edificios.id'), nullable=False)
    piso = Column(Integer)
    nombre_o_numero = Column(String, nullable=False)
    descripcion = Column(String)

    edificio = relationship("EdificioModel", back_populates="salas")
    dispositivos = relationship("DispositivoModel", back_populates="sala")