#!/usr/bin/env python3
"""
Script para visualizar datos de la base de datos PostgreSQL
Sistema de Monitoreo de Calidad del Aire - UNI
"""

import os
import sys
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import json
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

def connect_to_database():
    """Conectar a PostgreSQL usando las variables de entorno."""
    database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/air_quality_db')
    
    try:
        print("🔌 Conectando a PostgreSQL...")
        conn = psycopg2.connect(database_url)
        print("✅ Conexión exitosa!")
        return conn
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def show_tables(conn):
    """Mostrar todas las tablas en la base de datos."""
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            
            tables = cursor.fetchall()
            print("\n📊 TABLAS EN LA BASE DE DATOS:")
            print("-" * 40)
            for i, (table,) in enumerate(tables, 1):
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{i:2}. {table:<25} ({count} registros)")
            
            return [table[0] for table in tables]
    except Exception as e:
        print(f"❌ Error consultando tablas: {e}")
        return []

def show_users(conn):
    """Mostrar usuarios del sistema."""
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    u.id,
                    u.email,
                    u.nombre_completo,
                    r.nombre as rol,
                    uni.nombre as universidad,
                    u.fecha_creacion
                FROM usuarios u
                JOIN roles r ON u.rol_id = r.id
                LEFT JOIN universidades uni ON u.universidad_id = uni.id
                ORDER BY u.id;
            """)
            
            users = cursor.fetchall()
            print("\n👥 USUARIOS DEL SISTEMA:")
            print("-" * 80)
            print(f"{'ID':<3} {'Email':<25} {'Nombre':<20} {'Rol':<15} {'Universidad':<15}")
            print("-" * 80)
            
            for user in users:
                uni = user['universidad'][:12] + "..." if user['universidad'] and len(user['universidad']) > 15 else user['universidad'] or "N/A"
                print(f"{user['id']:<3} {user['email']:<25} {user['nombre_completo'][:18]:<20} {user['rol']:<15} {uni:<15}")
                
    except Exception as e:
        print(f"❌ Error consultando usuarios: {e}")

def show_institutional_structure(conn):
    """Mostrar estructura institucional."""
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    u.nombre as universidad,
                    c.nombre as campus,
                    e.nombre as edificio,
                    s.nombre_o_numero as sala,
                    COUNT(d.id) as dispositivos
                FROM universidades u
                JOIN campus c ON u.id = c.universidad_id
                JOIN edificios e ON c.id = e.campus_id
                JOIN salas s ON e.id = s.edificio_id
                LEFT JOIN dispositivos d ON s.id = d.sala_id
                GROUP BY u.id, u.nombre, c.id, c.nombre, e.id, e.nombre, s.id, s.nombre_o_numero
                ORDER BY u.nombre, c.nombre, e.nombre, s.nombre_o_numero;
            """)
            
            structure = cursor.fetchall()
            print("\n🏛️ ESTRUCTURA INSTITUCIONAL:")
            print("-" * 70)
            
            current_uni = None
            current_campus = None
            current_edificio = None
            
            for item in structure:
                if item['universidad'] != current_uni:
                    current_uni = item['universidad']
                    print(f"\n🎓 {current_uni}")
                
                if item['campus'] != current_campus:
                    current_campus = item['campus']
                    print(f"  📍 {current_campus}")
                
                if item['edificio'] != current_edificio:
                    current_edificio = item['edificio']
                    print(f"    🏢 {current_edificio}")
                
                dispositivos = f"({item['dispositivos']} dispositivos)" if item['dispositivos'] > 0 else "(sin dispositivos)"
                print(f"      🚪 {item['sala']} {dispositivos}")
                
    except Exception as e:
        print(f"❌ Error consultando estructura: {e}")

def show_devices(conn):
    """Mostrar dispositivos IoT."""
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT 
                    d.id,
                    d.mac_address,
                    d.estado,
                    md.nombre_modelo,
                    s.nombre_o_numero as sala,
                    e.nombre as edificio,
                    d.fecha_instalacion,
                    d.ultima_vez_visto
                FROM dispositivos d
                JOIN modelos_dispositivos md ON d.modelo_id = md.id
                JOIN salas s ON d.sala_id = s.id
                JOIN edificios e ON s.edificio_id = e.id
                ORDER BY d.id;
            """)
            
            devices = cursor.fetchall()
            print("\n📱 DISPOSITIVOS IoT:")
            print("-" * 100)
            print(f"{'ID':<3} {'MAC Address':<18} {'Estado':<12} {'Modelo':<20} {'Ubicación':<25} {'Instalación':<12}")
            print("-" * 100)
            
            for device in devices:
                ubicacion = f"{device['edificio'][:10]}/{device['sala']}"
                instalacion = device['fecha_instalacion'].strftime('%Y-%m-%d') if device['fecha_instalacion'] else "N/A"
                
                # Color por estado
                estado_icon = {
                    'conectado': '🟢',
                    'desconectado': '🔴', 
                    'mantenimiento': '🟡'
                }.get(device['estado'], '⚪')
                
                print(f"{device['id']:<3} {device['mac_address']:<18} {estado_icon} {device['estado']:<11} {device['nombre_modelo'][:18]:<20} {ubicacion[:23]:<25} {instalacion:<12}")
                
    except Exception as e:
        print(f"❌ Error consultando dispositivos: {e}")

def show_recent_readings(conn):
    """Mostrar lecturas recientes."""
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Lecturas de temperatura recientes
            cursor.execute("""
                SELECT 
                    d.mac_address,
                    lt.grados_temperatura,
                    lt.fecha_lectura
                FROM lecturas_temperatura lt
                JOIN dispositivos d ON lt.dispositivo_id = d.id
                ORDER BY lt.fecha_lectura DESC
                LIMIT 5;
            """)
            
            temp_readings = cursor.fetchall()
            
            # Lecturas de humedad recientes
            cursor.execute("""
                SELECT 
                    d.mac_address,
                    lh.porcentaje_humedad,
                    lh.fecha_lectura
                FROM lecturas_humedad lh
                JOIN dispositivos d ON lh.dispositivo_id = d.id
                ORDER BY lh.fecha_lectura DESC
                LIMIT 5;
            """)
            
            humidity_readings = cursor.fetchall()
            
            # Lecturas de calidad del aire recientes
            cursor.execute("""
                SELECT 
                    d.mac_address,
                    lca.valor_pm2_5,
                    lca.valor_pm10,
                    lca.fecha_lectura
                FROM lecturas_calidad_aire lca
                JOIN dispositivos d ON lca.dispositivo_id = d.id
                ORDER BY lca.fecha_lectura DESC
                LIMIT 5;
            """)
            
            air_readings = cursor.fetchall()
            
            print("\n📊 LECTURAS RECIENTES:")
            print("-" * 60)
            
            if temp_readings:
                print("🌡️  Temperatura:")
                for reading in temp_readings:
                    fecha = reading['fecha_lectura'].strftime('%Y-%m-%d %H:%M')
                    print(f"   {reading['mac_address']} - {reading['grados_temperatura']}°C ({fecha})")
            else:
                print("🌡️  Temperatura: Sin datos")
            
            if humidity_readings:
                print("\n💧 Humedad:")
                for reading in humidity_readings:
                    fecha = reading['fecha_lectura'].strftime('%Y-%m-%d %H:%M')
                    print(f"   {reading['mac_address']} - {reading['porcentaje_humedad']}% ({fecha})")
            else:
                print("\n💧 Humedad: Sin datos")
            
            if air_readings:
                print("\n🌬️  Calidad del Aire:")
                for reading in air_readings:
                    fecha = reading['fecha_lectura'].strftime('%Y-%m-%d %H:%M')
                    print(f"   {reading['mac_address']} - PM2.5: {reading['valor_pm2_5']}, PM10: {reading['valor_pm10']} ({fecha})")
            else:
                print("\n🌬️  Calidad del Aire: Sin datos")
                
    except Exception as e:
        print(f"❌ Error consultando lecturas: {e}")

def interactive_query(conn):
    """Permitir consultas SQL interactivas."""
    print("\n💻 CONSULTA INTERACTIVA SQL")
    print("Escribe una consulta SQL o 'exit' para salir:")
    print("Ejemplo: SELECT * FROM usuarios LIMIT 3;")
    print("-" * 50)
    
    while True:
        try:
            query = input("SQL> ").strip()
            
            if query.lower() in ['exit', 'quit', 'salir']:
                break
            
            if not query:
                continue
            
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                
                if cursor.description:
                    results = cursor.fetchall()
                    
                    if results:
                        # Mostrar resultados
                        columns = [desc[0] for desc in cursor.description]
                        print(f"\n📊 Resultados ({len(results)} filas):")
                        print(" | ".join(columns))
                        print("-" * (len(" | ".join(columns))))
                        
                        for row in results[:10]:  # Limitar a 10 resultados
                            values = [str(row[col])[:20] for col in columns]
                            print(" | ".join(values))
                        
                        if len(results) > 10:
                            print(f"... y {len(results) - 10} filas más")
                    else:
                        print("✅ Consulta ejecutada, sin resultados.")
                else:
                    print("✅ Consulta ejecutada exitosamente.")
                    
        except Exception as e:
            print(f"❌ Error en consulta: {e}")

def main():
    """Función principal."""
    print("🐘 EXPLORADOR DE BASE DE DATOS POSTGRESQL")
    print("Sistema de Monitoreo de Calidad del Aire - UNI")
    print("=" * 60)
    
    conn = connect_to_database()
    if not conn:
        print("\n❌ No se pudo conectar a la base de datos.")
        print("💡 Verifica que PostgreSQL esté ejecutándose en localhost:5432")
        return
    
    try:
        # Mostrar información general
        tables = show_tables(conn)
        
        if tables:
            show_users(conn)
            show_institutional_structure(conn)
            show_devices(conn)
            show_recent_readings(conn)
            
            print("\n" + "=" * 60)
            print("¿Qué quieres hacer?")
            print("1. Consulta SQL interactiva")
            print("2. Salir")
            
            choice = input("\nSelecciona una opción (1-2): ").strip()
            
            if choice == "1":
                interactive_query(conn)
        
        print("\n👋 ¡Hasta luego!")
        
    finally:
        conn.close()
        print("🔌 Conexión cerrada.")

if __name__ == "__main__":
    main()