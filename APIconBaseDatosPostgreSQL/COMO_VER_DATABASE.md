# 🐘 Guía para Conectarse a PostgreSQL

## 📊 **Opción 1: pgAdmin (Interfaz Gráfica)**

### Descargar e Instalar:
1. Ir a: https://www.pgadmin.org/download/
2. Descargar pgAdmin 4 para Windows
3. Instalar con configuración por defecto

### Configurar Conexión:
1. Abrir pgAdmin
2. Click derecho en "Servers" → "Create" → "Server"
3. **General Tab:**
   - Name: `UNI Air Quality DB`
4. **Connection Tab:**
   - Host: `localhost`
   - Port: `5432`
   - Database: `air_quality_db`
   - Username: `postgres`
   - Password: `password`
5. Click "Save"

### Ver Datos:
```
Servers → UNI Air Quality DB → Databases → air_quality_db → Schemas → public → Tables
```

---

## 💻 **Opción 2: psql (Línea de Comandos)**

### Si tienes PostgreSQL instalado localmente:
```bash
# Conectarse a la base de datos
psql -h localhost -p 5432 -U postgres -d air_quality_db

# Comandos útiles:
\dt                    # Listar todas las tablas
\d usuarios           # Describir tabla usuarios
SELECT * FROM roles;  # Ver todos los roles
SELECT * FROM usuarios LIMIT 5;  # Ver primeros 5 usuarios
\q                    # Salir
```

---

## 🐳 **Opción 3: Docker con psql**

### Si usas Docker:
```bash
# Conectarse al contenedor PostgreSQL
docker exec -it air_quality_postgres psql -U postgres -d air_quality_db

# O desde fuera del contenedor:
docker run --rm -it --network host postgres:15 psql -h localhost -U postgres -d air_quality_db
```

---

## 🌐 **Opción 4: Herramientas Web**

### DBeaver (Gratis):
1. Descargar: https://dbeaver.io/download/
2. Nueva Conexión → PostgreSQL
3. Configurar:
   - Server: `localhost`
   - Port: `5432`
   - Database: `air_quality_db`
   - Username: `postgres`
   - Password: `password`

### Adminer (Web):
```bash
# Ejecutar Adminer en Docker
docker run --rm -p 8080:8080 adminer

# Ir a: http://localhost:8080
# Sistema: PostgreSQL
# Servidor: host.docker.internal (o tu IP local)
# Usuario: postgres
# Contraseña: password
# Base de datos: air_quality_db
```

---

## 📊 **Consultas Útiles de Ejemplo**

```sql
-- Ver estructura de la base de datos
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Ver todos los roles
SELECT * FROM roles;

-- Ver usuarios con sus roles
SELECT u.email, u.nombre_completo, r.nombre as rol
FROM usuarios u
JOIN roles r ON u.rol_id = r.id;

-- Ver universidades y campus
SELECT u.nombre as universidad, c.nombre as campus
FROM universidades u
LEFT JOIN campus c ON u.id = c.universidad_id;

-- Ver dispositivos por sala
SELECT 
    s.nombre_o_numero as sala,
    e.nombre as edificio,
    d.mac_address,
    d.estado
FROM dispositivos d
JOIN salas s ON d.sala_id = s.id
JOIN edificios e ON s.edificio_id = e.id;

-- Ver últimas lecturas de temperatura
SELECT 
    d.mac_address,
    lt.grados_temperatura,
    lt.fecha_lectura
FROM lecturas_temperatura lt
JOIN dispositivos d ON lt.dispositivo_id = d.id
ORDER BY lt.fecha_lectura DESC
LIMIT 10;
```

---

## 🔍 **Verificar Datos de Prueba**

```sql
-- Usuarios de prueba (contraseña: admin123)
SELECT email, nombre_completo FROM usuarios;

-- Estructura institucional
SELECT 
    u.nombre as universidad,
    c.nombre as campus,
    e.nombre as edificio,
    s.nombre_o_numero as sala
FROM universidades u
JOIN campus c ON u.id = c.universidad_id
JOIN edificios e ON c.id = e.campus_id
JOIN salas s ON e.id = s.edificio_id;
```

---

## 🚨 **Solución de Problemas**

### Si no puedes conectarte:
```bash
# Verificar que PostgreSQL esté ejecutándose
netstat -an | findstr :5432

# Verificar procesos Docker
docker ps

# Ver logs de PostgreSQL
docker logs air_quality_postgres
```

### Credenciales por defecto:
- **Host:** localhost
- **Puerto:** 5432
- **Base de datos:** air_quality_db
- **Usuario:** postgres
- **Contraseña:** password