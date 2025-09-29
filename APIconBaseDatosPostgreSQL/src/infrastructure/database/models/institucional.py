# src/infrastructure/database/models/institucional.py
"""
Modelos de la jerarquía institucional según esquema DBML PostgreSQL.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Universidad(Base):
    """Modelo para universidades."""
    __tablename__ = 'universidades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), unique=True, nullable=False)
    pais = Column(String(100))

    # Relaciones
    campus = relationship("Campus", back_populates="universidad", cascade="all, delete-orphan")
    usuarios = relationship("Usuario", back_populates="universidad")

    def __repr__(self):
        return f"<Universidad(id={self.id}, nombre='{self.nombre}')>"


class Campus(Base):
    """Modelo para campus universitarios."""
    __tablename__ = 'campus'

    id = Column(Integer, primary_key=True, autoincrement=True)
    universidad_id = Column(Integer, ForeignKey('universidades.id'), nullable=False)
    nombre = Column(String(150), nullable=False)
    direccion = Column(Text)

    # Relaciones
    universidad = relationship("Universidad", back_populates="campus")
    edificios = relationship("Edificio", back_populates="campus", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Campus(id={self.id}, nombre='{self.nombre}')>"


class Edificio(Base):
    """Modelo para edificios."""
    __tablename__ = 'edificios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    campus_id = Column(Integer, ForeignKey('campus.id'), nullable=False)
    nombre = Column(String(100), nullable=False)

    # Relaciones
    campus = relationship("Campus", back_populates="edificios")
    salas = relationship("Sala", back_populates="edificio", cascade="all, delete-orphan")

    # Índice único compuesto
    __table_args__ = (
        {'schema': None},  # PostgreSQL schema si se necesita
    )

    def __repr__(self):
        return f"<Edificio(id={self.id}, nombre='{self.nombre}')>"


class Sala(Base):
    """Modelo para salas."""
    __tablename__ = 'salas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    edificio_id = Column(Integer, ForeignKey('edificios.id'), nullable=False)
    piso = Column(Integer)
    nombre_o_numero = Column(String(50), nullable=False)
    descripcion = Column(Text)

    # Relaciones
    edificio = relationship("Edificio", back_populates="salas")
    dispositivos = relationship("Dispositivo", back_populates="sala", cascade="all, delete-orphan")
    asignaciones_limpieza = relationship("AsignacionLimpieza", back_populates="sala")

    def __repr__(self):
        return f"<Sala(id={self.id}, nombre='{self.nombre_o_numero}')>"