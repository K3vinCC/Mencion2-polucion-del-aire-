# scripts/init_db.py
"""
Script para inicializar la base de datos con datos de ejemplo.
"""

import os
import sys
import logging
from datetime import datetime, timedelta

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.infrastructure.database.connection import db
from src.domain.entities.usuario import Usuario
from src.domain.entities.dispositivo import Dispositivo
from src.domain.entities.sala import Sala
from src.domain.entities.universidad import Universidad
from src.infrastructure.services.jwt_service import JWTService

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """
    Inicializa la base de datos con datos de ejemplo.
    """
    # Configuración de base de datos desde variables de entorno
    database_url = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@localhost:5432/air_quality_db'
    )

    # Crear aplicación Flask para contexto
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        try:
            # Crear todas las tablas
            db.create_all()
            logger.info("Tablas creadas exitosamente")

            # Verificar si ya hay datos
            if Universidad.query.first():
                logger.info("La base de datos ya contiene datos. Omitiendo inicialización.")
                return

            # Crear universidad de ejemplo
            universidad = Universidad(
                nombre="Universidad Nacional",
                direccion="Ciudad Universitaria",
                telefono="123456789",
                email="contacto@universidad.edu"
            )
            db.session.add(universidad)
            db.session.commit()
            logger.info(f"Universidad creada: {universidad.nombre}")

            # Crear salas de ejemplo
            salas_data = [
                {"nombre": "Sala A101", "capacidad": 50, "tipo": "aula"},
                {"nombre": "Sala B202", "capacidad": 30, "tipo": "laboratorio"},
                {"nombre": "Sala C303", "capacidad": 25, "tipo": "oficina"},
                {"nombre": "Sala D404", "capacidad": 40, "tipo": "biblioteca"}
            ]

            salas = []
            for sala_data in salas_data:
                sala = Sala(
                    nombre=sala_data["nombre"],
                    capacidad=sala_data["capacidad"],
                    tipo=sala_data["tipo"],
                    universidad_id=universidad.id
                )
                db.session.add(sala)
                salas.append(sala)

            db.session.commit()
            logger.info(f"Salas creadas: {len(salas)}")

            # Crear usuarios de ejemplo
            jwt_service = JWTService()

            # Administrador
            admin_password = jwt_service.hash_password("admin123")
            admin = Usuario(
                nombre="Administrador",
                apellido="Sistema",
                email="admin@universidad.edu",
                password_hash=admin_password,
                rol="administrador",
                universidad_id=universidad.id,
                telefono="987654321",
                activo=True
            )
            db.session.add(admin)

            # Supervisor
            supervisor_password = jwt_service.hash_password("supervisor123")
            supervisor = Usuario(
                nombre="Juan",
                apellido="Pérez",
                email="supervisor@universidad.edu",
                password_hash=supervisor_password,
                rol="supervisor",
                universidad_id=universidad.id,
                telefono="987654322",
                activo=True
            )
            db.session.add(supervisor)

            # Usuario regular
            user_password = jwt_service.hash_password("user123")
            user = Usuario(
                nombre="María",
                apellido="García",
                email="user@universidad.edu",
                password_hash=user_password,
                rol="usuario",
                universidad_id=universidad.id,
                telefono="987654323",
                activo=True
            )
            db.session.add(user)

            db.session.commit()
            logger.info("Usuarios creados: administrador, supervisor, usuario")

            # Crear dispositivos de ejemplo
            dispositivos_data = [
                {"nombre": "Sensor A101", "tipo": "calidad_aire", "sala_id": salas[0].id, "token": "device_token_a101"},
                {"nombre": "Sensor B202", "tipo": "calidad_aire", "sala_id": salas[1].id, "token": "device_token_b202"},
                {"nombre": "Sensor C303", "tipo": "temperatura", "sala_id": salas[2].id, "token": "device_token_c303"},
                {"nombre": "Sensor D404", "tipo": "humedad", "sala_id": salas[3].id, "token": "device_token_d404"}
            ]

            dispositivos = []
            for dispositivo_data in dispositivos_data:
                dispositivo = Dispositivo(
                    nombre=dispositivo_data["nombre"],
                    tipo=dispositivo_data["tipo"],
                    sala_id=dispositivo_data["sala_id"],
                    token=dispositivo_data["token"],
                    activo=True
                )
                db.session.add(dispositivo)
                dispositivos.append(dispositivo)

            db.session.commit()
            logger.info(f"Dispositivos creados: {len(dispositivos)}")

            # Mostrar resumen
            print("\n" + "="*50)
            print("BASE DE DATOS INICIALIZADA EXITOSAMENTE")
            print("="*50)
            print(f"Universidad: {universidad.nombre}")
            print(f"Salas creadas: {len(salas)}")
            print(f"Usuarios creados: 3 (admin, supervisor, usuario)")
            print(f"Dispositivos creados: {len(dispositivos)}")
            print("\nCredenciales de acceso:")
            print("Administrador: admin@universidad.edu / admin123")
            print("Supervisor: supervisor@universidad.edu / supervisor123")
            print("Usuario: user@universidad.edu / user123")
            print("\nTokens de dispositivos:")
            for dispositivo in dispositivos:
                print(f"{dispositivo.nombre}: {dispositivo.token}")
            print("="*50)

        except Exception as e:
            logger.error(f"Error al inicializar la base de datos: {str(e)}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    init_database()