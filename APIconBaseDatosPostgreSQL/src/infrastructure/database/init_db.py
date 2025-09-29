# src/infrastructure/database/init_db.py
"""
Script de inicialización de la base de datos PostgreSQL.
Crea todas las tablas y inserta datos de prueba.
"""

import sys
import os
from datetime import datetime, date

# Agregar el directorio raíz del proyecto al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.infrastructure.database.database import get_engine, get_session
from src.infrastructure.database.models import (
    Universidad, Campus, Rol, Usuario, Edificio, Sala,
    ModeloDispositivo, Dispositivo, LecturaTemperatura,
    LecturaHumedad, LecturaCalidadAire, AsignacionLimpieza
)


def create_tables():
    """Crear todas las tablas en la base de datos."""
    engine = get_engine()
    print("Creando tablas en la base de datos...")

    # Importar Base desde database.py
    from src.infrastructure.database.database import Base
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")


def insert_test_data():
    """Insertar datos de prueba en la base de datos."""
    try:
        with get_session() as session:
            print("Insertando datos de prueba...")

        # Crear universidad
        universidad = Universidad(
            nombre="Universidad Nacional",
            pais="Colombia"
        )
        session.add(universidad)
        session.flush()

        # Crear campus
        campus = Campus(
            nombre="Campus Principal",
            direccion="Centro de la ciudad",
            universidad_id=universidad.id
        )
        session.add(campus)
        session.flush()

        # Crear roles
        roles_data = [
            {"nombre": "administrador"},
            {"nombre": "operador"},
            {"nombre": "limpiador"}
        ]

        roles = []
        for rol_data in roles_data:
            rol = Rol(**rol_data)
            session.add(rol)
            roles.append(rol)
        session.flush()

        # Crear usuarios
        from src.domain.entities.usuario import Usuario as DomainUsuario
        import bcrypt

        usuarios_data = [
            {
                "email": "admin@uninacional.edu.co",
                "clave_hash": bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                "nombre_completo": "Administrador General",
                "rol_id": roles[0].id,  # administrador
                "universidad_id": universidad.id,
                "campus_id": campus.id
            },
            {
                "email": "operador@uninacional.edu.co",
                "clave_hash": bcrypt.hashpw("operador123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                "nombre_completo": "Operador de Sistemas",
                "rol_id": roles[1].id,  # operador
                "universidad_id": universidad.id,
                "campus_id": campus.id
            },
            {
                "email": "limpiador@uninacional.edu.co",
                "clave_hash": bcrypt.hashpw("limpiador123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                "nombre_completo": "Personal de Limpieza",
                "rol_id": roles[2].id,  # limpiador
                "universidad_id": universidad.id,
                "campus_id": campus.id
            }
        ]

        usuarios = []
        for usuario_data in usuarios_data:
            usuario = Usuario(**usuario_data)
            session.add(usuario)
            usuarios.append(usuario)
        session.flush()

        # Crear edificio
        edificio = Edificio(
            campus_id=campus.id,
            nombre="Edificio de Ingeniería"
        )
        session.add(edificio)
        session.flush()

        # Crear salas
        salas_data = [
            {"edificio_id": edificio.id, "piso": 1, "nombre_o_numero": "101", "descripcion": "Sala de conferencias"},
            {"edificio_id": edificio.id, "piso": 2, "nombre_o_numero": "201", "descripcion": "Laboratorio de química"},
            {"edificio_id": edificio.id, "piso": 3, "nombre_o_numero": "301", "descripcion": "Aula de clases"}
        ]

        salas = []
        for sala_data in salas_data:
            sala = Sala(**sala_data)
            session.add(sala)
            salas.append(sala)
        session.flush()

        # Crear modelos de dispositivo
        modelos_data = [
            {"nombre_modelo": "AirQuality Sensor Pro", "fabricante": "SensorTech", "especificaciones": "Sensor PM2.5, temperatura, humedad"},
            {"nombre_modelo": "TempHumidity Monitor", "fabricante": "ClimateControl", "especificaciones": "Sensor de temperatura y humedad"}
        ]

        modelos = []
        for modelo_data in modelos_data:
            modelo = ModeloDispositivo(**modelo_data)
            session.add(modelo)
            modelos.append(modelo)
        session.flush()

        # Crear dispositivos
        import secrets
        from cryptography.fernet import Fernet

        cipher = Fernet(Fernet.generate_key())

        dispositivos_data = [
            {
                "sala_id": salas[0].id,
                "modelo_id": modelos[0].id,
                "mac_address": "AA:BB:CC:DD:EE:01",
                "api_token_hash": bcrypt.hashpw(secrets.token_hex(32).encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                "fecha_instalacion": date.today(),
                "estado": "conectado"
            },
            {
                "sala_id": salas[1].id,
                "modelo_id": modelos[0].id,
                "mac_address": "AA:BB:CC:DD:EE:02",
                "api_token_hash": bcrypt.hashpw(secrets.token_hex(32).encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                "fecha_instalacion": date.today(),
                "estado": "conectado"
            }
        ]

        dispositivos = []
        for dispositivo_data in dispositivos_data:
            dispositivo = Dispositivo(**dispositivo_data)
            session.add(dispositivo)
            dispositivos.append(dispositivo)
        session.flush()

        # Crear lecturas de prueba
        # Lecturas de temperatura
        for dispositivo in dispositivos:
            lectura_temp = LecturaTemperatura(
                dispositivo_id=dispositivo.id,
                grados_temperatura=25.5,
                etiqueta="ambiente",
                fecha_lectura=datetime.now()
            )
            session.add(lectura_temp)

        # Lecturas de humedad
        for dispositivo in dispositivos:
            lectura_hum = LecturaHumedad(
                dispositivo_id=dispositivo.id,
                porcentaje_humedad=65.0,
                etiqueta="ambiente",
                fecha_lectura=datetime.now()
            )
            session.add(lectura_hum)

        # Lecturas de calidad del aire
        for dispositivo in dispositivos:
            lectura_aire = LecturaCalidadAire(
                dispositivo_id=dispositivo.id,
                valor_pm1=15.2,
                valor_pm2_5=25.8,
                valor_pm10=35.4,
                etiqueta="ambiente",
                fecha_lectura=datetime.now()
            )
            session.add(lectura_aire)

        # Crear asignación de limpieza
        asignacion = AsignacionLimpieza(
            sala_id=salas[0].id,
            asignado_por_usuario_id=usuarios[0].id,  # administrador
            asignado_a_usuario_id=usuarios[2].id,    # limpiador
            estado="pendiente"
        )
        session.add(asignacion)

        print("Datos de prueba insertados exitosamente.")

    except Exception as e:
        print(f"Error al insertar datos de prueba: {e}")
        raise


def main():
    """Función principal para inicializar la base de datos."""
    try:
        create_tables()
        insert_test_data()
        print("Base de datos inicializada correctamente.")
    except Exception as e:
        print(f"Error durante la inicialización: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()