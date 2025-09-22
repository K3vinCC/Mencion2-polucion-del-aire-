from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os

# Crear el motor de SQLAlchemy
engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///polucion_aire_v3.db'))

# Crear la fábrica de sesiones
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Crear la base para los modelos
Base = declarative_base()

def get_session():
    """Obtiene una sesión de la base de datos"""
    session = Session()
    try:
        yield session
    finally:
        session.close()