# src/infrastructure/database/database.py
"""
Configuración de la base de datos PostgreSQL usando SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy.pool import QueuePool
import os
from contextlib import contextmanager

# Crear la base declarativa para los modelos
Base = declarative_base()

class DatabaseConfig:
    """Configuración centralizada de la base de datos."""

    def __init__(self):
        self.database_url = self._get_database_url()
        self.engine = None
        self.SessionLocal = None

    def _get_database_url(self) -> str:
        """
        Obtiene la URL de conexión a la base de datos desde variables de entorno.

        Returns:
            str: URL de conexión a la base de datos

        Raises:
            ValueError: Si la URL de la base de datos no está configurada
        """
        database_url = os.getenv('DATABASE_URL')

        if not database_url:
            raise ValueError('DATABASE_URL es requerida. Configurar PostgreSQL: postgresql://user:pass@host:port/db')
        
        if 'postgresql' not in database_url:
            raise ValueError('Solo se soporta PostgreSQL como base de datos')

        return database_url

    def create_engine(self):
        """
        Crea el engine de SQLAlchemy con configuración optimizada para PostgreSQL.
        """
        self.engine = create_engine(
            self.database_url,
            poolclass=QueuePool,
            pool_size=10,          # Número de conexiones en el pool
            max_overflow=20,       # Conexiones adicionales permitidas
            pool_timeout=30,       # Timeout para obtener conexión del pool
            pool_recycle=3600,     # Reciclar conexiones cada hora
            echo=False,            # No mostrar SQL en logs (cambiar a True para debug)
            future=True            # Usar SQLAlchemy 2.0
        )

        return self.engine

    def create_session_factory(self):
        """
        Crea la fábrica de sesiones con configuración de scoped session.
        """
        if not self.engine:
            self.create_engine()

        self.SessionLocal = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
        )

        return self.SessionLocal

    @contextmanager
    def get_session(self):
        """
        Context manager para obtener una sesión de base de datos.

        Yields:
            Session: Sesión de SQLAlchemy

        Raises:
            Exception: Cualquier error durante el uso de la sesión
        """
        if not self.SessionLocal:
            self.create_session_factory()

        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def init_database(self):
        """
        Inicializa la base de datos creando todas las tablas definidas en los modelos.
        """
        if not self.engine:
            self.create_engine()

        # Importar todos los modelos para que Base los conozca
        from .models import (
            Universidad, Campus, Rol, Usuario, Edificio, Sala,
            ModeloDispositivo, Dispositivo, LecturaTemperatura,
            LecturaHumedad, LecturaCalidadAire, AsignacionLimpieza
        )

        Base.metadata.create_all(bind=self.engine)
        print("Base de datos inicializada correctamente.")

    def drop_database(self):
        """
        Elimina todas las tablas de la base de datos (útil para desarrollo).
        """
        if not self.engine:
            self.create_engine()

        Base.metadata.drop_all(bind=self.engine)
        print("Todas las tablas han sido eliminadas.")

    def reset_database(self):
        """
        Reinicia la base de datos eliminando y recreando todas las tablas.
        """
        self.drop_database()
        self.init_database()

# Instancia global de configuración de base de datos
db_config = DatabaseConfig()

# Funciones de conveniencia para uso en la aplicación
def get_engine():
    """Obtiene el engine de SQLAlchemy."""
    if not db_config.engine:
        db_config.create_engine()
    return db_config.engine

def get_session():
    """Obtiene una sesión de base de datos."""
    return db_config.get_session()

def init_db():
    """Inicializa la base de datos."""
    db_config.init_database()

def reset_db():
    """Reinicia la base de datos."""
    db_config.reset_database()