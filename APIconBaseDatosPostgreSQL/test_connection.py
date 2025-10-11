#!/usr/bin/env python3
"""
Script de prueba de conexión PostgreSQL
Sistema de Monitoreo de Calidad del Aire UNI
"""

import os
import sys
import traceback
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_postgresql_connection():
    """
    Prueba la conexión a PostgreSQL usando SQLAlchemy
    """
    print("🔍 Probando conexión a PostgreSQL...")
    print("-" * 50)
    
    try:
        # Importar dependencias
        try:
            import sqlalchemy
            from sqlalchemy import create_engine, text
            print(f"✅ SQLAlchemy versión: {sqlalchemy.__version__}")
        except ImportError as e:
            print(f"❌ Error: SQLAlchemy no instalado: {e}")
            return False
        
        try:
            import psycopg2
            print(f"✅ psycopg2 versión: {psycopg2.__version__}")
        except ImportError as e:
            print(f"❌ Error: psycopg2 no instalado: {e}")
            print("💡 Instalar con: pip install psycopg2-binary")
            return False
        
        # Obtener URL de base de datos
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ Error: DATABASE_URL no encontrada en .env")
            return False
        
        print(f"🔗 URL de conexión: {database_url}")
        
        # Crear engine
        print("\n📡 Creando conexión...")
        engine = create_engine(database_url, echo=True)
        
        # Probar conexión
        print("\n🔌 Probando conexión a la base de datos...")
        with engine.connect() as connection:
            # Probar query simple
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Conexión exitosa!")
            print(f"🐘 PostgreSQL versión: {version}")
            
            # Probar si las tablas existen
            print("\n📊 Verificando tablas...")
            tables_query = text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            
            result = connection.execute(tables_query)
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print(f"✅ Tablas encontradas ({len(tables)}):")
                for table in tables:
                    print(f"   • {table}")
            else:
                print("⚠️  No se encontraron tablas (base de datos vacía)")
            
            # Probar datos de ejemplo
            print("\n👥 Verificando usuarios de prueba...")
            try:
                users_query = text("SELECT email, nombre_completo FROM usuarios LIMIT 5")
                result = connection.execute(users_query)
                users = result.fetchall()
                
                if users:
                    print(f"✅ Usuarios encontrados ({len(users)}):")
                    for user in users:
                        print(f"   • {user[0]} - {user[1]}")
                else:
                    print("⚠️  No se encontraron usuarios")
            except Exception as e:
                print(f"⚠️  Error consultando usuarios: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("\n🔧 Detalles del error:")
        traceback.print_exc()
        return False

def test_config():
    """
    Verifica la configuración del proyecto
    """
    print("\n⚙️  Verificando configuración...")
    print("-" * 50)
    
    # Verificar .env
    if os.path.exists('.env'):
        print("✅ Archivo .env encontrado")
    else:
        print("❌ Archivo .env no encontrado")
        return False
    
    # Verificar variables importantes
    required_vars = [
        'DATABASE_URL',
        'FLASK_SECRET_KEY', 
        'JWT_SECRET_KEY',
        'FLASK_ENV'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Ocultar valores sensibles
            if 'SECRET' in var or 'PASSWORD' in var:
                display_value = '*' * len(value)
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NO DEFINIDA")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Variables faltantes: {', '.join(missing_vars)}")
        return False
    
    return True

def suggest_solutions():
    """
    Sugiere soluciones para problemas comunes
    """
    print("\n💡 Soluciones sugeridas:")
    print("-" * 50)
    print("1. Para instalar PostgreSQL localmente:")
    print("   • Windows: Descargar desde https://www.postgresql.org/download/windows/")
    print("   • Configurar usuario: postgres, contraseña: password")
    print("   • Puerto: 5432")
    print()
    print("2. Para usar Docker (recomendado):")
    print("   • Instalar Docker Desktop desde https://www.docker.com/products/docker-desktop")
    print("   • Ejecutar: docker compose up -d")
    print()
    print("3. Para instalar dependencias Python:")
    print("   • pip install psycopg2-binary")
    print("   • pip install python-dotenv")
    print()
    print("4. Para crear la base de datos manualmente:")
    print("   • Conectar como superusuario a PostgreSQL")
    print("   • CREATE DATABASE air_quality_db;")
    print("   • Ejecutar el script init-db.sql")

if __name__ == "__main__":
    print("🚀 Script de Prueba PostgreSQL - Sistema UNI")
    print("=" * 50)
    
    # Verificar configuración
    config_ok = test_config()
    
    if config_ok:
        # Probar conexión
        connection_ok = test_postgresql_connection()
        
        if connection_ok:
            print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        else:
            print("\n❌ Falló la conexión a PostgreSQL")
            suggest_solutions()
    else:
        print("\n❌ Error en la configuración")
        suggest_solutions()
    
    print("\n" + "=" * 50)
    print("Prueba finalizada")