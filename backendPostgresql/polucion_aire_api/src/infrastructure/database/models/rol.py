from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base

class RolModel(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, unique=True, nullable=False)
    
    usuarios = relationship("UsuarioModel", back_populates="rol")