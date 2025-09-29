# API de Monitoreo de Calidad del Aire - Universidad Nacional

Sistema completo para el monitoreo de calidad del aire (temperatura, humedad, material particulado) en salas de clases universitarias con notificaciones automatizadas vía Telegram.

## 🚀 Características Principales

- **Base de datos PostgreSQL exclusiva** según documento maestro
- **Arquitectura Hexagonal** (Clean Architecture + DDD)
- **Autenticación JWT manual** con expiración de 12 horas
- **API RESTful completa** con documentación Swagger/OpenAPI
- **Roles de usuario**: SuperAdmin, Admin_Universidad, Conserje, Limpiador
- **Dispositivos IoT**: Autenticación por MAC + API Token
- **Notificaciones Telegram** para asignaciones de limpieza

## 📋 Requisitos Previos

### Opción 1: Docker (Recomendado)
```bash
# Instalar Docker y Docker Compose
docker --version
docker-compose --version
```

### Opción 2: Instalación Local
```bash
# PostgreSQL 15+
psql --version

# Python 3.10+
python --version

# Dependencias Python
pip install -r requirements.txt
```

## 🛠️ Instalación y Configuración

### Configuración con Docker (Fácil)

1. **Clonar el repositorio**:
```bash
git clone https://github.com/tu-usuario/air-quality-monitoring.git
cd air-quality-monitoring/APIconBaseDatosPostgreSQL
```

2. **Configurar variables de entorno**:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

3. **Iniciar con Docker**:
```bash
# Levantar PostgreSQL + API
docker-compose up -d

# Verificar que funciona
curl http://localhost:5000/health
```

### Configuración Local (PostgreSQL existente)

1. **Crear base de datos PostgreSQL**:
```sql
CREATE DATABASE air_quality_db;
CREATE USER postgres WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE air_quality_db TO postgres;
```

2. **Configurar .env**:
```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/air_quality_db
FLASK_ENV=development
JWT_SECRET_KEY=tu-clave-jwt-segura
TELEGRAM_BOT_TOKEN=tu-token-telegram
TELEGRAM_CHAT_ID=tu-chat-id
```

3. **Instalar dependencias e inicializar**:
```bash
pip install -r requirements.txt
python run.py
```

## 📊 Estructura de Base de Datos

El sistema utiliza **exclusivamente PostgreSQL** con el siguiente esquema:

```sql
-- Jerarquía Institucional
universidades → campus → edificios → salas

-- Usuarios y Roles
roles → usuarios (SuperAdmin, Admin_Universidad, Conserje, Limpiador)

-- Dispositivos IoT
modelos_dispositivos → dispositivos (MAC + API Token)

-- Lecturas de Sensores
dispositivos → lecturas_temperatura
            → lecturas_humedad  
            → lecturas_calidad_aire

-- Operaciones
asignaciones_limpieza (Conserje asigna a Limpiador)
```

## 🔐 Autenticación y Roles

### JWT Manual (Sin librerías externas)
- **Algoritmo**: HMAC-SHA256
- **Expiración**: 12 horas (configurable)
- **Header**: `Authorization: Bearer <token>`

### Roles del Sistema

| Rol | Permisos | Endpoints |
|-----|----------|-----------|
| **SuperAdmin** | Acceso global, gestiona universidades | Todos los endpoints |
| **Admin_Universidad** | Gestiona su universidad | `/usuarios`, `/dispositivos`, `/dashboard/universidad/{id}` |
| **Conserje** | Monitorea edificio asignado | `/asignaciones`, `/dashboard/edificio/{id}` |
| **Limpiador** | Solo notificaciones Telegram | Ninguno (solo Telegram) |

## 📡 Endpoints de la API

### Autenticación
```http
POST /api/login
Content-Type: application/json

{
  "email": "admin@uni.edu.pe",
  "clave": "admin123"
}
```

### Gestión de Usuarios (Admin_Universidad)
```http
POST /api/usuarios
GET /api/usuarios
GET /api/usuarios/{id}
```

### Gestión de Dispositivos (Admin_Universidad)
```http
POST /api/dispositivos
GET /api/dispositivos
```

### Recepción de Datos IoT (Dispositivos)
```http
POST /api/lecturas
Headers: 
  X-API-Token: <token_dispositivo>
  X-Device-MAC: <mac_address>
```

### Asignaciones de Limpieza (Conserje)
```http
POST /api/asignaciones
GET /api/asignaciones
```

### Dashboards
```http
GET /api/dashboard/universidad/{id}  # Admin_Universidad
GET /api/dashboard/edificio/{id}     # Conserje
```

## 🤖 Integración IoT (Dispositivos)

### Autenticación de Doble Factor
1. **MAC Address**: Identificador físico único del dispositivo
2. **API Token**: Token secreto generado por el servidor

### Ejemplo de código ESP32:
```cpp
// Headers requeridos
headers["X-API-Token"] = "tu_token_secreto";
headers["X-Device-MAC"] = WiFi.macAddress();

// Payload encriptado
{
  "temperatura": 22.5,
  "humedad": 45.1,
  "pm2_5": 15.7
}
```

## 📱 Notificaciones Telegram

### Configuración del Bot
1. Crear bot con @BotFather
2. Obtener token del bot
3. Configurar en `.env`:
```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ
TELEGRAM_CHAT_ID=@tu_canal_o_chat_id
```

### Flujo de Notificación
```
Conserje detecta problema → Selecciona Limpiador → Sistema envía Telegram
```

## 📚 Documentación API

### Swagger UI
- **URL**: `http://localhost:5000/api/docs`
- **Especificación**: `http://localhost:5000/static/swagger.yaml`

### Ejemplos de Uso

#### Login y obtener token:
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@uni.edu.pe", "clave": "admin123"}'
```

#### Crear nuevo dispositivo:
```bash
curl -X POST http://localhost:5000/api/dispositivos \
  -H "Authorization: Bearer <tu-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "mac_address": "3C:71:BF:4F:9D:E4",
    "modelo_id": 1,
    "sala_id": 101
  }'
```

## 🔧 Desarrollo

### Estructura del Proyecto
```
src/
├── domain/           # Entidades y reglas de negocio
├── application/      # Casos de uso
├── infrastructure/   # Adaptadores externos
│   ├── controllers/  # REST API endpoints
│   ├── database/     # PostgreSQL models
│   ├── services/     # JWT, Telegram, etc.
│   └── repositories/ # Persistencia de datos
└── config/          # Configuración de la aplicación
```

### Comandos de Desarrollo

```bash
# Ejecutar aplicación en desarrollo
python run.py

# Ejecutar tests
pytest

# Verificar calidad de código
flake8 src/
black src/

# Docker development
docker-compose up --build
```

## 🚀 Deployment en Producción

### Variables de Entorno Requeridas
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
JWT_SECRET_KEY=clave-super-segura-produccion
FLASK_SECRET_KEY=clave-flask-segura
TELEGRAM_BOT_TOKEN=token-real-telegram
TELEGRAM_CHAT_ID=chat-id-real
CORS_ORIGINS=https://tu-dominio.com
```

### Docker Compose (Production)
```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: air_quality_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  
  app:
    build: .
    environment:
      FLASK_ENV: production
      DATABASE_URL: postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/air_quality_db
```

## 📞 Soporte

- **Documentación completa**: Ver `/api/docs` en la aplicación
- **Issues**: Crear issue en GitHub
- **Email**: soporte@uni.edu.pe

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

**Universidad Nacional de Ingeniería - Facultad de Ingeniería de Sistemas**  
*Sistema de Monitoreo de Calidad del Aire v1.2*