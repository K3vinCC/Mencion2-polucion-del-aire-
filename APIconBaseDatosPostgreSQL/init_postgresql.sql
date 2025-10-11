-- init_postgresql.sql
-- Script de inicialización para PostgreSQL según esquema DBML
-- Polución Aire UNI - Documento Maestro v1.2

-- Crear base de datos (ejecutar como administrador)
-- CREATE DATABASE air_quality_db;

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear esquema principal (opcional)
-- CREATE SCHEMA IF NOT EXISTS air_quality;

-- === TABLAS DE JERARQUÍA INSTITUCIONAL ===

-- Universidades
CREATE TABLE IF NOT EXISTS universidades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) UNIQUE NOT NULL,
    pais VARCHAR(100)
);

-- Campus
CREATE TABLE IF NOT EXISTS campus (
    id SERIAL PRIMARY KEY,
    universidad_id INTEGER NOT NULL REFERENCES universidades(id) ON DELETE CASCADE,
    nombre VARCHAR(150) NOT NULL,
    direccion TEXT
);

-- Edificios  
CREATE TABLE IF NOT EXISTS edificios (
    id SERIAL PRIMARY KEY,
    campus_id INTEGER NOT NULL REFERENCES campus(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    UNIQUE(campus_id, nombre)
);

-- Salas
CREATE TABLE IF NOT EXISTS salas (
    id SERIAL PRIMARY KEY,
    edificio_id INTEGER NOT NULL REFERENCES edificios(id) ON DELETE CASCADE,
    piso INTEGER,
    nombre_o_numero VARCHAR(50) NOT NULL,
    descripcion TEXT,
    UNIQUE(edificio_id, nombre_o_numero)
);

-- === TABLAS DE AUTENTICACIÓN Y USUARIOS ===

-- Roles
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

-- Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    clave_hash VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(100) NOT NULL,
    rol_id INTEGER NOT NULL REFERENCES roles(id),
    universidad_id INTEGER REFERENCES universidades(id),
    fecha_creacion TIMESTAMPTZ DEFAULT NOW()
);

-- === TABLAS DE INFRAESTRUCTURA Y DISPOSITIVOS ===

-- Modelos de dispositivos
CREATE TABLE IF NOT EXISTS modelos_dispositivos (
    id SERIAL PRIMARY KEY,
    nombre_modelo VARCHAR(100) UNIQUE NOT NULL,
    fabricante VARCHAR(100),
    especificaciones TEXT
);

-- Dispositivos
CREATE TABLE IF NOT EXISTS dispositivos (
    id SERIAL PRIMARY KEY,
    sala_id INTEGER NOT NULL REFERENCES salas(id) ON DELETE CASCADE,
    modelo_id INTEGER NOT NULL REFERENCES modelos_dispositivos(id),
    mac_address VARCHAR(17) UNIQUE NOT NULL,
    api_token_hash VARCHAR(255) NOT NULL,
    fecha_instalacion DATE,
    ultimo_mantenimiento DATE,
    estado VARCHAR(20) NOT NULL DEFAULT 'desconectado',
    ultima_vez_visto TIMESTAMPTZ
);

-- === TABLAS DE LECTURAS ===

-- Lecturas de temperatura
CREATE TABLE IF NOT EXISTS lecturas_temperatura (
    id SERIAL PRIMARY KEY,
    dispositivo_id INTEGER NOT NULL REFERENCES dispositivos(id) ON DELETE CASCADE,
    grados_temperatura DECIMAL(5,2) NOT NULL,
    etiqueta VARCHAR(20),
    fecha_lectura TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Lecturas de humedad
CREATE TABLE IF NOT EXISTS lecturas_humedad (
    id SERIAL PRIMARY KEY,
    dispositivo_id INTEGER NOT NULL REFERENCES dispositivos(id) ON DELETE CASCADE,
    porcentaje_humedad DECIMAL(5,2) NOT NULL,
    etiqueta VARCHAR(20),
    fecha_lectura TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Lecturas de calidad del aire
CREATE TABLE IF NOT EXISTS lecturas_calidad_aire (
    id SERIAL PRIMARY KEY,
    dispositivo_id INTEGER NOT NULL REFERENCES dispositivos(id) ON DELETE CASCADE,
    valor_pm1 DECIMAL(8,2),
    valor_pm2_5 DECIMAL(8,2),
    valor_pm10 DECIMAL(8,2),
    etiqueta VARCHAR(20),
    fecha_lectura TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- === TABLAS DE OPERACIONES ===

-- Asignaciones de limpieza
CREATE TABLE IF NOT EXISTS asignaciones_limpieza (
    id SERIAL PRIMARY KEY,
    sala_id INTEGER NOT NULL REFERENCES salas(id) ON DELETE CASCADE,
    asignado_por_usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    asignado_a_usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_completado TIMESTAMPTZ
);

-- === ÍNDICES PARA RENDIMIENTO ===

CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_rol ON usuarios(rol_id);
CREATE INDEX IF NOT EXISTS idx_dispositivos_mac ON dispositivos(mac_address);
CREATE INDEX IF NOT EXISTS idx_dispositivos_sala ON dispositivos(sala_id);
CREATE INDEX IF NOT EXISTS idx_lecturas_temp_dispositivo ON lecturas_temperatura(dispositivo_id);
CREATE INDEX IF NOT EXISTS idx_lecturas_temp_fecha ON lecturas_temperatura(fecha_lectura);
CREATE INDEX IF NOT EXISTS idx_lecturas_humedad_dispositivo ON lecturas_humedad(dispositivo_id);
CREATE INDEX IF NOT EXISTS idx_lecturas_humedad_fecha ON lecturas_humedad(fecha_lectura);
CREATE INDEX IF NOT EXISTS idx_lecturas_aire_dispositivo ON lecturas_calidad_aire(dispositivo_id);
CREATE INDEX IF NOT EXISTS idx_lecturas_aire_fecha ON lecturas_calidad_aire(fecha_lectura);
CREATE INDEX IF NOT EXISTS idx_asignaciones_sala ON asignaciones_limpieza(sala_id);
CREATE INDEX IF NOT EXISTS idx_asignaciones_estado ON asignaciones_limpieza(estado);

-- === DATOS INICIALES ===

-- Insertar roles del sistema
INSERT INTO roles (nombre) VALUES 
    ('SuperAdmin'),
    ('Admin_Universidad'),
    ('Conserje'),
    ('Limpiador')
ON CONFLICT (nombre) DO NOTHING;

-- Insertar universidad de ejemplo
INSERT INTO universidades (nombre, pais) VALUES 
    ('Universidad Nacional de Ingeniería', 'Perú'),
    ('Universidad de Lima', 'Perú')
ON CONFLICT (nombre) DO NOTHING;

-- Insertar campus de ejemplo
INSERT INTO campus (universidad_id, nombre, direccion) VALUES 
    (1, 'Campus Central', 'Av. Túpac Amaru 210, Rímac, Lima'),
    (1, 'Campus Norte', 'Av. Universitaria 1801, San Miguel, Lima')
ON CONFLICT DO NOTHING;

-- Insertar edificios de ejemplo
INSERT INTO edificios (campus_id, nombre) VALUES 
    (1, 'Edificio de Ingeniería Civil'),
    (1, 'Edificio de Sistemas'),
    (2, 'Edificio Principal')
ON CONFLICT (campus_id, nombre) DO NOTHING;

-- Insertar salas de ejemplo
INSERT INTO salas (edificio_id, piso, nombre_o_numero, descripcion) VALUES 
    (1, 1, 'Aula 101', 'Aula de clases teóricas - Capacidad 40 estudiantes'),
    (1, 1, 'Aula 102', 'Aula de clases teóricas - Capacidad 35 estudiantes'),
    (1, 2, 'Lab 201', 'Laboratorio de computación - 20 PCs'),
    (2, 1, 'Aula A-101', 'Aula magna - Capacidad 80 estudiantes'),
    (2, 2, 'Sala B-205', 'Sala de reuniones y seminarios')
ON CONFLICT (edificio_id, nombre_o_numero) DO NOTHING;

-- Insertar modelos de dispositivos
INSERT INTO modelos_dispositivos (nombre_modelo, fabricante, especificaciones) VALUES 
    ('ESP32-DHT22-PMS5003', 'Custom Build', 'Sensor DHT22 para temperatura/humedad + Sensor PMS5003 para material particulado'),
    ('Arduino-ENV-Shield', 'Arduino', 'Shield ambiental completo con múltiples sensores')
ON CONFLICT (nombre_modelo) DO NOTHING;

-- Insertar usuarios de ejemplo (contraseñas hasheadas con bcrypt para 'password123')
INSERT INTO usuarios (email, clave_hash, nombre_completo, rol_id, universidad_id) VALUES 
    ('admin@uni.edu.pe', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewVyhtYqF/PYrPGa', 'Administrador General UNI', 2, 1),
    ('conserje1@uni.edu.pe', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewVyhtYqF/PYrPGa', 'Carlos Mendoza', 3, 1),
    ('limpieza1@uni.edu.pe', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewVyhtYqF/PYrPGa', 'María García', 4, 1),
    ('limpieza2@uni.edu.pe', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewVyhtYqF/PYrPGa', 'Juan Rodríguez', 4, 1)
ON CONFLICT (email) DO NOTHING;

-- Insertar dispositivos de ejemplo
INSERT INTO dispositivos (sala_id, modelo_id, mac_address, api_token_hash, fecha_instalacion, estado) VALUES 
    (1, 1, '3C:71:BF:4F:9D:E4', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewVyhtYqF/PYrPGa', '2025-01-15', 'conectado'),
    (2, 1, '3C:71:BF:4F:9D:E5', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewVyhtYqF/PYrPGa', '2025-01-16', 'desconectado'),
    (3, 1, '3C:71:BF:4F:9D:E6', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewVyhtYqF/PYrPGa', '2025-01-17', 'conectado')
ON CONFLICT (mac_address) DO NOTHING;

-- Insertar lecturas de ejemplo (datos recientes)
INSERT INTO lecturas_temperatura (dispositivo_id, grados_temperatura, etiqueta, fecha_lectura) VALUES 
    (1, 22.5, 'Normal', NOW() - INTERVAL '5 minutes'),
    (1, 23.1, 'Normal', NOW() - INTERVAL '2 minutes'),
    (3, 24.8, 'Alto', NOW() - INTERVAL '3 minutes');

INSERT INTO lecturas_humedad (dispositivo_id, porcentaje_humedad, etiqueta, fecha_lectura) VALUES 
    (1, 45.2, 'Normal', NOW() - INTERVAL '5 minutes'),
    (1, 46.8, 'Normal', NOW() - INTERVAL '2 minutes'),
    (3, 52.1, 'Alto', NOW() - INTERVAL '3 minutes');

INSERT INTO lecturas_calidad_aire (dispositivo_id, valor_pm1, valor_pm2_5, valor_pm10, etiqueta, fecha_lectura) VALUES 
    (1, 8.2, 15.7, 23.4, 'Bueno', NOW() - INTERVAL '5 minutes'),
    (1, 9.1, 16.2, 24.1, 'Bueno', NOW() - INTERVAL '2 minutes'),
    (3, 25.4, 45.8, 67.2, 'Moderado', NOW() - INTERVAL '3 minutes');

-- Insertar asignación de limpieza de ejemplo
INSERT INTO asignaciones_limpieza (sala_id, asignado_por_usuario_id, asignado_a_usuario_id, estado) VALUES 
    (3, 2, 3, 'pendiente');

COMMIT;