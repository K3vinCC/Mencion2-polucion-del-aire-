# src/config/__init__.py
"""
Configuración principal de la aplicación.
"""

import os
from datetime import timedelta
from typing import Optional

class Config:
    """Configuración base de la aplicación."""

    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = False

    # Base de datos - PostgreSQL exclusivo
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError('DATABASE_URL es requerida. Configurar PostgreSQL: postgresql://user:pass@host:port/db')
    
    if 'postgresql' not in DATABASE_URL.lower():
        raise ValueError('Solo se soporta PostgreSQL. URL debe comenzar con postgresql://')
        
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False').lower() == 'true'
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20
    }

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', '12'))

    # Encriptación
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')

    @property
    def jwt_expiration_delta(self) -> timedelta:
        """Retorna el tiempo de expiración del JWT."""
        return timedelta(hours=self.JWT_EXPIRATION_HOURS)


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """Configuración para testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///:memory:')
    JWT_EXPIRATION_HOURS = 1  # Tokens cortos para testing


class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    TESTING = False

    # En producción, todas las variables de entorno deben estar configuradas
    @property
    def required_env_vars(self):
        """Variables de entorno requeridas en producción."""
        return [
            'DATABASE_URL',
            'JWT_SECRET_KEY',
            'ENCRYPTION_KEY',
            'TELEGRAM_BOT_TOKEN',
            'TELEGRAM_CHAT_ID',
            'FLASK_SECRET_KEY'
        ]

    def __init__(self):
        super().__init__()
        self._validate_production_config()

    def _validate_production_config(self):
        """Valida que todas las variables requeridas estén configuradas."""
        missing_vars = []
        for var in self.required_env_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(
                f"Variables de entorno requeridas faltantes en producción: {', '.join(missing_vars)}"
            )


# Mapeo de configuraciones por entorno
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env: Optional[str] = None) -> Config:
    """
    Obtiene la configuración apropiada según el entorno.

    Args:
        env: Entorno deseado ('development', 'testing', 'production')

    Returns:
        Instancia de configuración apropiada
    """
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')

    config_class = config.get(env.lower(), config['default'])
    return config_class()