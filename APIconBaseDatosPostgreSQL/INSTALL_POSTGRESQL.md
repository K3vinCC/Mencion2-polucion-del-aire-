# 🚀 Guía de Instalación PostgreSQL - Sistema UNI

## ✅ Estado Actual
- **Configuración**: ✅ Completa y correcta
- **Dependencias Python**: ✅ SQLAlchemy 2.0.23, psycopg2 2.9.7 instaladas
- **Scripts**: ✅ Base de datos PostgreSQL lista
- **Faltante**: PostgreSQL servidor ejecutándose

## 🐘 Opciones de Instalación PostgreSQL

### Opción 1: Docker (RECOMENDADA) 🐳

```bash
# 1. Instalar Docker Desktop
# Descargar desde: https://www.docker.com/products/docker-desktop

# 2. Verificar instalación
docker --version

# 3. Ejecutar PostgreSQL con nuestro proyecto
cd "C:\Users\jonaw\Documents\GitHub\Mencion2-polucion-del-aire-\APIconBaseDatosPostgreSQL"
docker compose up -d

# 4. Verificar contenedores
docker compose ps
```

### Opción 2: PostgreSQL Local 🏠

```bash
# 1. Descargar PostgreSQL 15
# https://www.postgresql.org/download/windows/

# 2. Durante la instalación configurar:
Usuario: postgres
Contraseña: password
Puerto: 5432

# 3. Crear base de datos
psql -U postgres
CREATE DATABASE air_quality_db;
\q

# 4. Ejecutar nuestro script de inicialización
psql -U postgres -d air_quality_db -f init-db.sql
```

### Opción 3: PostgreSQL Portable ⚡

```bash
# 1. Descargar PostgreSQL Portable
# https://sourceforge.net/projects/postgresqlportable/

# 2. Extraer y ejecutar
# 3. Configurar igual que la opción 2
```

## 🧪 Verificar Instalación

```bash
# Ejecutar nuestro script de prueba
cd "C:\Users\jonaw\Documents\GitHub\Mencion2-polucion-del-aire-\APIconBaseDatosPostgreSQL"
python test_connection.py
```

## 📊 Que verás cuando funcione

```
🚀 Script de Prueba PostgreSQL - Sistema UNI
==================================================
✅ Archivo .env encontrado
✅ DATABASE_URL: postgresql://postgres:password@localhost:5432/air_quality_db
✅ Conexión exitosa!
🐘 PostgreSQL versión: PostgreSQL 15.x
📊 Verificando tablas...
✅ Tablas encontradas (12):
   • asignaciones_limpieza
   • campus
   • dispositivos
   • edificios
   • lecturas_calidad_aire
   • lecturas_humedad
   • lecturas_temperatura
   • modelos_dispositivos
   • roles
   • salas
   • universidades
   • usuarios
👥 Verificando usuarios de prueba...
✅ Usuarios encontrados (3):
   • admin@uni.edu.pe - Administrador UNI
   • conserje@uni.edu.pe - Juan Pérez Conserje
   • limpieza@uni.edu.pe - María García Limpiadora
🎉 ¡Todas las pruebas pasaron exitosamente!
```

## 🔧 Solución de Problemas

### Error: "Connection refused"
- PostgreSQL no está ejecutándose
- Verificar puerto 5432: `netstat -an | findstr :5432`

### Error: "Authentication failed"
- Verificar usuario/contraseña en .env
- Resetear contraseña PostgreSQL

### Error: "Database does not exist"
- Crear base de datos: `CREATE DATABASE air_quality_db;`
- Ejecutar init-db.sql

## 🎯 Próximos Pasos

Una vez que PostgreSQL esté funcionando:

1. ✅ Ejecutar `python test_connection.py` - debe pasar todas las pruebas
2. 🚀 Iniciar la aplicación Flask: `python run.py`
3. 📖 Acceder a Swagger UI: `http://localhost:5000/api/docs`
4. 🧪 Probar endpoints con usuarios de prueba

## 🔑 Credenciales de Prueba

| Usuario | Email | Contraseña | Rol |
|---------|-------|------------|-----|
| Admin | `admin@uni.edu.pe` | `admin123` | Admin_Universidad |
| Conserje | `conserje@uni.edu.pe` | `admin123` | Conserje |
| Limpiador | `limpieza@uni.edu.pe` | `admin123` | Limpiador |

## 📁 Estructura de Archivos

```
APIconBaseDatosPostgreSQL/
├── 📄 .env                    # ✅ Variables de entorno
├── 📄 docker-compose.yml      # ✅ Docker PostgreSQL
├── 📄 init-db.sql            # ✅ Script inicialización
├── 📄 test_connection.py     # ✅ Prueba de conexión
└── 📄 INSTALL_POSTGRESQL.md  # 📖 Esta guía
```

---
**💡 Recomendación:** Usar Docker para desarrollo es más rápido y evita conflictos con otras instalaciones.