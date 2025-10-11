#!/usr/bin/env python3
"""
Script principal para ejecutar la aplicación.
"""

import os
import sys
from pathlib import Path

# Agregar el directorio src al path
project_root = Path(__file__).parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

# Cargar variables de entorno desde .env si existe
from dotenv import load_dotenv
env_file = project_root / '.env'
if env_file.exists():
    load_dotenv(env_file)

# Importar y ejecutar la aplicación
from src.app import app

if __name__ == '__main__':
    # Obtener configuración del entorno
    env = os.getenv('FLASK_ENV', 'development')

    print(f"Iniciando aplicación en modo: {env}")
    print(f"Base de datos: {app.config.get('SQLALCHEMY_DATABASE_URI', 'No configurada')}")

    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', '5000')),
        debug=app.config['DEBUG']
    )