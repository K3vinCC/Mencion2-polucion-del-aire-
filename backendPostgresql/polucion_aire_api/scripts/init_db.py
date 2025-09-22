import os
import sys
import bcrypt
from datetime import datetime

# Añadir el directorio raíz al PATH para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.infrastructure.database.database import Base, engine, Session
from src.infrastructure.database.models.usuario import UsuarioModel
from src.infrastructure.database.models.dispositivo import DispositivoModel
from src.infrastructure.database.models.rol import RolModel
from src.infrastructure.database.models.universidad import UniversidadModel
from src.infrastructure.database.models.campus import CampusModel
from src.infrastructure.database.models.edificio import EdificioModel
from src.infrastructure.database.models.sala import SalaModel
from src.infrastructure.database.models.modelo_dispositivo import ModeloDispositivoModel

from sqlalchemy import text

def inicializar_base_datos():
    """Inicializa la base de datos con datos básicos necesarios"""
    
    # Crear todas las tablas
    print("Creando tablas...")
    Base.metadata.create_all(engine)
    
    session = Session()
    
    try:
        # 1. Crear roles básicos
        print("Creando roles básicos...")
        session.execute(text("""
            INSERT OR IGNORE INTO roles (id, nombre) VALUES 
            (1, 'SuperAdmin'),
            (2, 'Admin_Universidad'),
            (3, 'Conserje'),
            (4, 'Limpiador')
        """))
        
        # 2. Crear universidad de prueba
        print("Creando universidad de prueba...")
        session.execute(text("""
            INSERT OR IGNORE INTO universidades (id, nombre, pais)
            VALUES (1, 'Universidad de Prueba', 'España')
        """))
        
        # 3. Crear campus de prueba
        print("Creando campus de prueba...")
        session.execute(text("""
            INSERT OR IGNORE INTO campus (id, universidad_id, nombre, direccion)
            VALUES (1, 1, 'Campus Principal', 'Calle Principal 123')
        """))
        
        # 4. Crear edificio de prueba
        print("Creando edificio de prueba...")
        session.execute(text("""
            INSERT OR IGNORE INTO edificios (id, campus_id, nombre)
            VALUES (1, 1, 'Edificio A')
        """))
        
        # 5. Crear sala de prueba
        print("Creando sala de prueba...")
        session.execute(text("""
            INSERT OR IGNORE INTO salas (id, edificio_id, piso, nombre_o_numero)
            VALUES (1, 1, 1, 'Sala 101')
        """))
        
        # 6. Crear modelo de dispositivo de prueba
        print("Creando modelo de dispositivo de prueba...")
        session.execute(text("""
            INSERT OR IGNORE INTO modelos_dispositivos (id, nombre_modelo, fabricante)
            VALUES (1, 'Sensor Calidad Aire v1', 'FabricanteX')
        """))
        
        # 7. Crear usuario administrador si no existe
        if not session.query(UsuarioModel).filter_by(email='admin@example.com').first():
            print("Creando usuario administrador...")
            password = "admin123"
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            
            admin = UsuarioModel(
                email='admin@example.com',
                clave_hash=password_hash,
                nombre_completo='Administrador',
                rol_id=1,  # SuperAdmin
                universidad_id=1,
                fecha_creacion=datetime.now()
            )
            session.add(admin)
        
        # 8. Crear dispositivo de prueba si no existe
        if not session.query(DispositivoModel).filter_by(id_hardware='DEVICE001').first():
            print("Creando dispositivo de prueba...")
            api_token = "test-device-token-2025"  # Token de prueba
            token_hash = bcrypt.hashpw(api_token.encode(), bcrypt.gensalt()).decode()
            
            dispositivo = DispositivoModel(
                sala_id=1,
                modelo_id=1,
                id_hardware='DEVICE001',
                api_token_hash=token_hash,
                fecha_instalacion=datetime.now(),
                estado='conectado',
                ultima_vez_visto=datetime.now()
            )
            session.add(dispositivo)
        
        # Guardar todos los cambios
        session.commit()
        print("\nBase de datos inicializada exitosamente!")
        print("\nCredenciales de acceso:")
        print("------------------------")
        print("Usuario admin:")
        print("Email: admin@example.com")
        print("Contraseña: admin123")
        print("\nDispositivo de prueba:")
        print("Token: test-device-token-2025")
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == '__main__':
    inicializar_base_datos()