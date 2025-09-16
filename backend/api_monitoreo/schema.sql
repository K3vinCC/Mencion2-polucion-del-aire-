-- schema.sql

-- Tabla para almacenar la información de cada campus
CREATE TABLE campus (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT UNIQUE NOT NULL,
  direccion TEXT
);

-- Tabla para almacenar la información de cada modelo de dispositivo
CREATE TABLE modelos_dispositivo (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre_modelo TEXT UNIQUE NOT NULL,
  fabricante TEXT,
  especificaciones TEXT
);

-- Tabla para cada edificio, vinculado a un campus
CREATE TABLE edificios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_campus INTEGER NOT NULL,
  nombre TEXT NOT NULL,
  FOREIGN KEY (id_campus) REFERENCES campus (id)
);

-- Tabla para registrar cada aparato físico
CREATE TABLE dispositivos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_sala INTEGER NOT NULL,
  id_modelo INTEGER NOT NULL,
  fecha_instalacion TEXT,
  ultimo_mantenimiento TEXT,
  FOREIGN KEY (id_sala) REFERENCES salas (id),
  FOREIGN KEY (id_modelo) REFERENCES modelos_dispositivo (id)
);

-- Y así sucesivamente para el resto de las tablas...
-- Por ahora, nos enfocaremos en los usuarios para el login/registro.

CREATE TABLE usuarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  correo TEXT UNIQUE NOT NULL,
  clave_hash TEXT NOT NULL,
  numero_contacto TEXT,
  url_imagen_perfil TEXT,
  rol TEXT NOT NULL,
  id_edificio_asignado INTEGER,
  fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_edificio_asignado) REFERENCES edificios (id)
);

CREATE TABLE personal_aseo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    numero_contacto TEXT NOT NULL,
    url_imagen_perfil TEXT,
    id_edificio_asignado INTEGER NOT NULL,
    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_edificio_asignado) REFERENCES edificios (id)
);