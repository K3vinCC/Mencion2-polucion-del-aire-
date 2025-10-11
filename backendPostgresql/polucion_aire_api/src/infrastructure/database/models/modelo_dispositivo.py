from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base

class ModeloDispositivoModel(Base):
    __tablename__ = 'modelos_dispositivos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_modelo = Column(String, unique=True, nullable=False)
    fabricante = Column(String)
    especificaciones = Column(String)

    dispositivos = relationship("DispositivoModel", back_populates="modelo")