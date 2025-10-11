-- Script de inicialización PostgreSQL exclusivo
-- Sistema de Monitoreo de Calidad del Aire UNI
-- Según esquema DBML del documento maestro

-- Crear extensiones necesarias para PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- === TABLAS PRINCIPALES ===

-- Tabla universidades
CREATE TABLE IF NOT EXISTS universidades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) UNIQUE NOT NULL,
    pais VARCHAR(100)
);

-- Tabla campus
CREATE TABLE IF NOT EXISTS campus (
    id SERIAL PRIMARY KEY,
    universidad_id INTEGER NOT NULL REFERENCES universidades(id) ON DELETE CASCADE,
    nombre VARCHAR(150) NOT NULL,
    direccion TEXT
);

-- Tabla roles del sistema
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    clave_hash VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(100) NOT NULL,
    rol_id INTEGER NOT NULL REFERENCES roles(id),
    universidad_id INTEGER REFERENCES universidades(id),
    fecha_creacion TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla edificios
CREATE TABLE IF NOT EXISTS edificios (
    id SERIAL PRIMARY KEY,
    campus_id INTEGER NOT NULL REFERENCES campus(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    UNIQUE(campus_id, nombre)
);

-- Tabla salas
CREATE TABLE IF NOT EXISTS salas (
    id SERIAL PRIMARY KEY,
    edificio_id INTEGER NOT NULL REFERENCES edificios(id) ON DELETE CASCADE,
    piso INTEGER,
    nombre_o_numero VARCHAR(50) NOT NULL,
    descripcion TEXT,
    UNIQUE(edificio_id, nombre_o_numero)
);

-- Tabla modelos de dispositivos
CREATE TABLE IF NOT EXISTS modelos_dispositivos (
    id SERIAL PRIMARY KEY,
    nombre_modelo VARCHAR(100) UNIQUE NOT NULL,
    fabricante VARCHAR(100),
    especificaciones TEXT
);

-- Tabla dispositivos IoT
CREATE TABLE IF NOT EXISTS dispositivos (
    id SERIAL PRIMARY KEY,
    sala_id INTEGER NOT NULL REFERENCES salas(id) ON DELETE CASCADE,
    modelo_id INTEGER NOT NULL REFERENCES modelos_dispositivos(id),
    mac_address VARCHAR(17) UNIQUE NOT NULL, -- Formato MAC: XX:XX:XX:XX:XX:XX
    api_token_hash VARCHAR(255) NOT NULL,
    fecha_instalacion DATE,
    ultimo_mantenimiento DATE,
    estado VARCHAR(20) NOT NULL DEFAULT 'desconectado',
    ultima_vez_visto TIMESTAMPTZ
);

-- Tabla lecturas de temperatura
CREATE TABLE IF NOT EXISTS lecturas_temperatura (
    id SERIAL PRIMARY KEY,
    dispositivo_id INTEGER NOT NULL REFERENCES dispositivos(id) ON DELETE CASCADE,
    grados_temperatura DECIMAL(5, 2) NOT NULL,
    etiqueta VARCHAR(20),
    fecha_lectura TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla lecturas de humedad
CREATE TABLE IF NOT EXISTS lecturas_humedad (
    id SERIAL PRIMARY KEY,
    dispositivo_id INTEGER NOT NULL REFERENCES dispositivos(id) ON DELETE CASCADE,
    porcentaje_humedad DECIMAL(5, 2) NOT NULL,
    etiqueta VARCHAR(20),
    fecha_lectura TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla lecturas de calidad del aire
CREATE TABLE IF NOT EXISTS lecturas_calidad_aire (
    id SERIAL PRIMARY KEY,
    dispositivo_id INTEGER NOT NULL REFERENCES dispositivos(id) ON DELETE CASCADE,
    valor_pm1 DECIMAL(8, 2),
    valor_pm2_5 DECIMAL(8, 2),
    valor_pm10 DECIMAL(8, 2),
    etiqueta VARCHAR(20),
    fecha_lectura TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabla asignaciones de limpieza
CREATE TABLE IF NOT EXISTS asignaciones_limpieza (
    id SERIAL PRIMARY KEY,
    sala_id INTEGER NOT NULL REFERENCES salas(id),
    asignado_por_usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    asignado_a_usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fecha_completado TIMESTAMPTZ
);

-- === DATOS INICIALES SEGÚN DOCUMENTO MAESTRO ===

-- Roles del sistema (según documento maestro)
INSERT INTO roles (nombre) VALUES 
    ('SuperAdmin'),
    ('Admin_Universidad'),
    ('Conserje'),
    ('Limpiador')
ON CONFLICT (nombre) DO NOTHING;

-- Universidad Nacional de Ingeniería (ejemplo del documento)
INSERT INTO universidades (nombre, pais) VALUES 
    ('Universidad Nacional de Ingeniería', 'Perú')
ON CONFLICT (nombre) DO NOTHING;

-- Campus Central UNI
INSERT INTO campus (universidad_id, nombre, direccion) VALUES 
    (1, 'Campus Central', 'Av. Túpac Amaru 210, Rímac, Lima 25, Perú')
ON CONFLICT DO NOTHING;

-- Usuario Admin_Universidad de prueba
-- Contraseña: admin123 (hash bcrypt)
INSERT INTO usuarios (email, clave_hash, nombre_completo, rol_id, universidad_id) VALUES 
    ('admin@uni.edu.pe', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewKKy1UiFNlwwHG6', 'Administrador UNI', 2, 1),
    ('conserje@uni.edu.pe', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewKKy1UiFNlwwHG6', 'Juan Pérez Conserje', 3, 1),
    ('limpieza@uni.edu.pe', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewKKy1UiFNlwwHG6', 'María García Limpiadora', 4, 1)
ON CONFLICT (email) DO NOTHING;

-- Edificios del Campus Central
INSERT INTO edificios (campus_id, nombre) VALUES 
    (1, 'Edificio de Sistemas'),
    (1, 'Edificio de Civil'),
    (1, 'Edificio de Mecánica')
ON CONFLICT (campus_id, nombre) DO NOTHING;

-- Salas de ejemplo
INSERT INTO salas (edificio_id, piso, nombre_o_numero, descripcion) VALUES 
    (1, 1, 'Aula 101', 'Aula de programación'),
    (1, 1, 'Aula 102', 'Laboratorio de redes'),
    (1, 2, 'Aula 201', 'Sala de conferencias'),
    (2, 1, 'Aula C-101', 'Aula de estructuras'),
    (3, 1, 'Lab M-101', 'Laboratorio de máquinas')
ON CONFLICT (edificio_id, nombre_o_numero) DO NOTHING;

-- Modelos de dispositivos IoT
INSERT INTO modelos_dispositivos (nombre_modelo, fabricante, especificaciones) VALUES 
    ('ESP32-DHT22-PMS5003', 'Custom Build', 'ESP32 + DHT22 (temp/humedad) + PMS5003 (PM2.5/PM10)'),
    ('Arduino-SHT30-PMS7003', 'Custom Build', 'Arduino Uno + SHT30 + PMS7003 (calidad aire)')
ON CONFLICT (nombre_modelo) DO NOTHING;

-- === ÍNDICES PARA PERFORMANCE ===

-- Índices para usuarios y autenticación
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_rol ON usuarios(rol_id);
CREATE INDEX IF NOT EXISTS idx_usuarios_universidad ON usuarios(universidad_id);

-- Índices para dispositivos IoT
CREATE INDEX IF NOT EXISTS idx_dispositivos_mac ON dispositivos(mac_address);
CREATE INDEX IF NOT EXISTS idx_dispositivos_sala ON dispositivos(sala_id);
CREATE INDEX IF NOT EXISTS idx_dispositivos_estado ON dispositivos(estado);

-- Índices para lecturas de sensores (consultas frecuentes)
CREATE INDEX IF NOT EXISTS idx_lecturas_temp_dispositivo_fecha ON lecturas_temperatura(dispositivo_id, fecha_lectura DESC);
CREATE INDEX IF NOT EXISTS idx_lecturas_humedad_dispositivo_fecha ON lecturas_humedad(dispositivo_id, fecha_lectura DESC);
CREATE INDEX IF NOT EXISTS idx_lecturas_aire_dispositivo_fecha ON lecturas_calidad_aire(dispositivo_id, fecha_lectura DESC);

-- Índices para asignaciones de limpieza
CREATE INDEX IF NOT EXISTS idx_asignaciones_sala_estado ON asignaciones_limpieza(sala_id, estado);
CREATE INDEX IF NOT EXISTS idx_asignaciones_fecha ON asignaciones_limpieza(fecha_creacion DESC);

-- === RESTRICCIONES Y VALIDACIONES ===

-- Verificar formato MAC address
ALTER TABLE dispositivos ADD CONSTRAINT chk_mac_format 
CHECK (mac_address ~ '^[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}$');

-- Estados válidos para dispositivos
ALTER TABLE dispositivos ADD CONSTRAINT chk_dispositivo_estado 
CHECK (estado IN ('conectado', 'desconectado', 'mantenimiento'));

-- Estados válidos para asignaciones
ALTER TABLE asignaciones_limpieza ADD CONSTRAINT chk_asignacion_estado 
CHECK (estado IN ('pendiente', 'en_progreso', 'completado', 'cancelado'));

-- Validar rangos de valores de sensores
ALTER TABLE lecturas_temperatura ADD CONSTRAINT chk_temp_range 
CHECK (grados_temperatura BETWEEN -50 AND 80);

ALTER TABLE lecturas_humedad ADD CONSTRAINT chk_humedad_range 
CHECK (porcentaje_humedad BETWEEN 0 AND 100);

-- Mensajes de confirmación
DO $$
BEGIN
    RAISE NOTICE 'PostgreSQL inicializado correctamente para Sistema de Monitoreo UNI';
    RAISE NOTICE 'Roles creados: SuperAdmin, Admin_Universidad, Conserje, Limpiador';
    RAISE NOTICE 'Universidad: Universidad Nacional de Ingeniería';
    RAISE NOTICE 'Usuario admin: admin@uni.edu.pe / admin123';
END $$;