# src/config/logging.py
"""
Configuración de logging para la aplicación.
"""

import logging
import logging.handlers
import os
from pathlib import Path

from src.config import get_config


def setup_logging():
    """
    Configura el sistema de logging de la aplicación.
    """
    config = get_config()

    # Crear directorio de logs si no existe
    log_dir = Path(config.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Configurar el logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.LOG_LEVEL.upper()))

    # Formateador
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler para archivo
    file_handler = logging.handlers.RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, config.LOG_LEVEL.upper()))

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Limpiar handlers existentes
    root_logger.handlers.clear()

    # Agregar handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Configurar loggers específicos de librerías
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.INFO)

    # Logger de la aplicación
    app_logger = logging.getLogger('air_quality_api')
    app_logger.info("Sistema de logging configurado correctamente")


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado para un módulo específico.

    Args:
        name: Nombre del módulo/logger

    Returns:
        Logger configurado
    """
    return logging.getLogger(f'air_quality_api.{name}')