# 🗄️ GUÍA RÁPIDA: INSTALAR POSTGRESQL

## ✅ Estado Actual
- ✅ **API Flask**: Funcionando perfectamente en http://localhost:5000
- ✅ **Swagger UI**: Funcionando en http://localhost:5000/api/docs
- ❌ **PostgreSQL**: No instalado (necesario para base de datos)

## 🚀 Opción 1: Instalación Rápida PostgreSQL

### 1. Descargar PostgreSQL 15
```
🌐 URL: https://www.postgresql.org/download/windows/
📦 Archivo: postgresql-15.4-1-windows-x64.exe (aprox. 150MB)
```

### 2. Instalación (5 minutos)
```
Usuario: postgres
Contraseña: password  (¡Importante! Usar exactamente esta contraseña)
Puerto: 5432
```

### 3. Verificar Instalación
```bash
# Abrir Command Prompt como Administrador
psql -U postgres -h localhost -p 5432
# Cuando pida contraseña, escribir: password
```

## 🐳 Opción 2: Docker (Si tienes Docker instalado)

```bash
# Ejecutar PostgreSQL en Docker
docker run --name postgres-air-quality -e POSTGRES_PASSWORD=password -e POSTGRES_DB=air_quality_db -p 5432:5432 -d postgres:15

# Verificar que funciona
docker ps
```

## 🧪 Opción 3: Usar SQLite (Temporal para pruebas)

Si quieres probar la API inmediatamente sin instalar PostgreSQL:

```bash
# Modificar .env temporalmente
DATABASE_URL=sqlite:///air_quality_test.db
```

## ✅ Después de Instalar PostgreSQL

### 1. Verificar Conexión
```bash
cd "C:\Users\jonaw\Documents\GitHub\Mencion2-polucion-del-aire-\APIconBaseDatosPostgreSQL"
python view_database.py
```

### 2. Inicializar Base de Datos
```bash
# Conectar a PostgreSQL
psql -U postgres -h localhost

# Crear base de datos
CREATE DATABASE air_quality_db;
\q

# Ejecutar script de inicialización
psql -U postgres -d air_quality_db -f init-db.sql
```

### 3. ¡Usar la API Completa!
```
🌐 API: http://localhost:5000
📚 Swagger: http://localhost:5000/api/docs
🔐 Login: admin@uni.edu.pe / admin123
```

## 💡 Recomendación

**Para desarrollo rápido**: Opción 1 (PostgreSQL local)
**Para producción**: Opción 2 (Docker)
**Para pruebas inmediatas**: Opción 3 (SQLite temporal)

## 🎯 Lo que ya funciona SIN PostgreSQL

- ✅ Servidor Flask
- ✅ Swagger UI completo 
- ✅ Documentación API
- ✅ Estructura de endpoints
- ❌ Solo falta la base de datos para almacenar datos

---
**¡La API ya está 90% lista! Solo necesitas PostgreSQL para el 10% restante.**