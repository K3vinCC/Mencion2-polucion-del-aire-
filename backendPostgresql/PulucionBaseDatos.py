import sqlite3
import os

DB_FILENAME = 'polucion_aire_v3.db'

def crear_base_de_datos():
    """
    Crea el archivo de la base de datos SQLite y define el esquema completo
    si el archivo no existe previamente.
    """
    # Borra la base de datos anterior si existe para empezar de cero.
    if os.path.exists(DB_FILENAME):
        os.remove(DB_FILENAME)
        print(f"Base de datos '{DB_FILENAME}' existente eliminada.")

    try:
        # Se conecta a la base de datos (la crea si no existe)
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        print(f"Base de datos '{DB_FILENAME}' creada exitosamente.")

        # Usamos executescript para ejecutar múltiples sentencias SQL
        cursor.executescript("""
            -- Tablas de Jerarquía Institucional
            CREATE TABLE universidades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                pais TEXT
            );

            CREATE TABLE campus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                universidad_id INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                direccion TEXT,
                FOREIGN KEY (universidad_id) REFERENCES universidades (id)
            );

            -- Tablas de Autenticación y Usuarios
            CREATE TABLE roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
            );

            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                clave_hash TEXT NOT NULL,
                nombre_completo TEXT NOT NULL,
                rol_id INTEGER NOT NULL,
                universidad_id INTEGER,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (rol_id) REFERENCES roles (id),
                FOREIGN KEY (universidad_id) REFERENCES universidades (id)
            );

            -- Tablas de Infraestructura y Dispositivos
            CREATE TABLE edificios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campus_id INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                FOREIGN KEY (campus_id) REFERENCES campus (id),
                UNIQUE (campus_id, nombre)
            );

            CREATE TABLE salas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                edificio_id INTEGER NOT NULL,
                piso INTEGER,
                nombre_o_numero TEXT NOT NULL,
                descripcion TEXT,
                FOREIGN KEY (edificio_id) REFERENCES edificios (id),
                UNIQUE (edificio_id, nombre_o_numero)
            );

            CREATE TABLE modelos_dispositivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_modelo TEXT NOT NULL UNIQUE,
                fabricante TEXT,
                especificaciones TEXT
            );

            CREATE TABLE dispositivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sala_id INTEGER NOT NULL,
                modelo_id INTEGER NOT NULL,
                id_hardware TEXT NOT NULL UNIQUE,
                api_token_hash TEXT NOT NULL,
                fecha_instalacion DATE,
                ultimo_mantenimiento DATE,
                estado TEXT NOT NULL DEFAULT 'desconectado',
                ultima_vez_visto TIMESTAMP,
                FOREIGN KEY (sala_id) REFERENCES salas (id),
                FOREIGN KEY (modelo_id) REFERENCES modelos_dispositivos (id)
            );

            -- Tablas de Lecturas
            CREATE TABLE lecturas_temperatura (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dispositivo_id INTEGER NOT NULL,
                grados_temperatura REAL NOT NULL,
                etiqueta TEXT,
                fecha_lectura TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (dispositivo_id) REFERENCES dispositivos (id)
            );

            CREATE TABLE lecturas_humedad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dispositivo_id INTEGER NOT NULL,
                porcentaje_humedad REAL NOT NULL,
                etiqueta TEXT,
                fecha_lectura TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (dispositivo_id) REFERENCES dispositivos (id)
            );

            CREATE TABLE lecturas_calidad_aire (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dispositivo_id INTEGER NOT NULL,
                valor_pm1 REAL,
                valor_pm2_5 REAL,
                valor_pm10 REAL,
                etiqueta TEXT,
                fecha_lectura TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (dispositivo_id) REFERENCES dispositivos (id)
            );

            -- Tablas de Operaciones
            CREATE TABLE asignaciones_limpieza (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sala_id INTEGER NOT NULL,
                asignado_por_usuario_id INTEGER NOT NULL,
                asignado_a_usuario_id INTEGER NOT NULL,
                estado TEXT NOT NULL DEFAULT 'pendiente',
                fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                fecha_completado TIMESTAMP,
                FOREIGN KEY (sala_id) REFERENCES salas (id),
                FOREIGN KEY (asignado_por_usuario_id) REFERENCES usuarios (id),
                FOREIGN KEY (asignado_a_usuario_id) REFERENCES usuarios (id)
            );
        """)
        print("Esquema de tablas creado exitosamente.")

        # --- Insertar Datos Iniciales Esenciales ---
        # Insertar los roles definidos en el sistema
        roles_iniciales = [('SuperAdmin',), ('Admin_Universidad',), ('Conserje',), ('Limpiador',)]
        cursor.executemany("INSERT INTO roles (nombre) VALUES (?)", roles_iniciales)
        print(f"{cursor.rowcount} roles iniciales han sido insertados.")

        # Confirmar los cambios
        conn.commit()
        print("Cambios guardados en la base de datos.")

    except sqlite3.Error as e:
        print(f"Error al crear la base de datos: {e}")
    finally:
        # Cerrar la conexión
        if conn:
            conn.close()
            print("Conexión con la base de datos cerrada.")

if __name__ == '__main__':
    crear_base_de_datos()