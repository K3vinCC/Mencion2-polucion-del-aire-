-- ==========================================
-- CREAR BASE DE DATOS
-- ==========================================
DROP DATABASE IF EXISTS polucion_aire;
CREATE DATABASE polucion_aire
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LOCALE_PROVIDER = 'libc'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- ==========================================
-- USAR LA BASE DE DATOS
-- ==========================================
\c polucion_aire;

-- ==========================================
-- CREAR TABLAS
-- ==========================================
CREATE TABLE universidades (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    pais TEXT
);

CREATE TABLE campus (
    id SERIAL PRIMARY KEY,
    universidad_id INTEGER NOT NULL REFERENCES universidades(id),
    nombre TEXT NOT NULL,
    direccion TEXT
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    clave_hash TEXT NOT NULL,
    nombre_completo TEXT NOT NULL,
    rol_id INTEGER NOT NULL REFERENCES roles(id),
    universidad_id INTEGER REFERENCES universidades(id),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE edificios (
    id SERIAL PRIMARY KEY,
    campus_id INTEGER NOT NULL REFERENCES campus(id),
    nombre TEXT NOT NULL,
    UNIQUE (campus_id, nombre)
);

CREATE TABLE salas (
    id SERIAL PRIMARY KEY,
    edificio_id INTEGER NOT NULL REFERENCES edificios(id),
    piso INTEGER,
    nombre_o_numero TEXT NOT NULL,
    descripcion TEXT,
    UNIQUE (edificio_id, nombre_o_numero)
);

CREATE TABLE modelos_dispositivos (
    id SERIAL PRIMARY KEY,
    nombre_modelo TEXT NOT NULL UNIQUE,
    fabricante TEXT,
    especificaciones TEXT
);

CREATE TABLE dispositivos (
    id SERIAL PRIMARY KEY,
    sala_id INTEGER NOT NULL REFERENCES salas(id),
    modelo_id INTEGER NOT NULL REFERENCES modelos_dispositivos(id),
    id_hardware TEXT NOT NULL UNIQUE,
    api_token_hash TEXT NOT NULL,
    fecha_instalacion DATE,
    ultimo_mantenimiento DATE,
    estado TEXT NOT NULL DEFAULT 'desconectado',
    ultima_vez_visto TIMESTAMP
);

CREATE TABLE lecturas_temperatura (
    id SERIAL PRIMARY KEY,
    dispositivo_id INTEGER NOT NULL REFERENCES dispositivos(id),
    grados_temperatura REAL NOT NULL,
    etiqueta TEXT,
    fecha_lectura TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lecturas_humedad (
    id SERIAL PRIMARY KEY,
    dispositivo_id INTEGER NOT NULL REFERENCES dispositivos(id),
    porcentaje_humedad REAL NOT NULL,
    etiqueta TEXT,
    fecha_lectura TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lecturas_calidad_aire (
    id SERIAL PRIMARY KEY,
    dispositivo_id INTEGER NOT NULL REFERENCES dispositivos(id),
    valor_pm1 REAL,
    valor_pm2_5 REAL,
    valor_pm10 REAL,
    etiqueta TEXT,
    fecha_lectura TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE asignaciones_limpieza (
    id SERIAL PRIMARY KEY,
    sala_id INTEGER NOT NULL REFERENCES salas(id),
    asignado_por_usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    asignado_a_usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    estado TEXT NOT NULL DEFAULT 'pendiente',
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_completado TIMESTAMP
);
