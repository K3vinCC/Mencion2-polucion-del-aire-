# API de Monitoreo de Calidad del Aire - Universidad Nacional

Sistema completo de monitoreo de calidad del aire desarrollado siguiendo principios de arquitectura hexagonal (Hexagonal Architecture), SOLID, DDD (Domain-Driven Design) y ACID para PostgreSQL.

## Arquitectura

El proyecto sigue una arquitectura hexagonal limpia con tres capas principales:

- **Domain**: Contiene las entidades de negocio, puertos (interfaces) y lógica de dominio pura
- **Application**: Contiene los casos de uso que orquestan la lógica de negocio
- **Infrastructure**: Contiene las implementaciones concretas (repositorios, servicios externos, base de datos)

## Características Principales

- ✅ **Autenticación JWT** con expiración de 12 horas
- ✅ **Base de datos PostgreSQL** con SQLAlchemy 2.0
- ✅ **Encriptación de datos** para comunicaciones seguras con dispositivos
- ✅ **Autenticación de doble factor** para dispositivos IoT
- ✅ **Sistema de roles** (Administrador, Operador, Limpiador)
- ✅ **Notificaciones Telegram** para alertas y asignaciones
- ✅ **Monitoreo en tiempo real** de temperatura, humedad y calidad del aire
- ✅ **Sistema de asignaciones de limpieza** basado en niveles de contaminación
- ✅ **API REST completa** con documentación
- ✅ **Control de acceso basado en roles** (RBAC)

## Tecnologías Utilizadas

- **Backend**: Python 3.8+, Flask, SQLAlchemy 2.0
- **Base de datos**: PostgreSQL
- **Autenticación**: JWT (implementación manual)
- **Encriptación**: cryptography, bcrypt
- **Notificaciones**: python-telegram-bot
- **Testing**: pytest
- **Contenedor**: Docker
- **Documentación**: OpenAPI/Swagger

## Requisitos del Sistema

- Python 3.8 o superior
- PostgreSQL 12 o superior
- Docker (opcional, para desarrollo)

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Mencion2-polucion-del-aire-/APIconBaseDatosPostgreSQL
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL

Crear una base de datos PostgreSQL:

```sql
CREATE DATABASE air_quality_db;
CREATE USER air_quality_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE air_quality_db TO air_quality_user;
```

### 5. Configurar variables de entorno

Copiar el archivo de ejemplo y configurar las variables:

```bash
cp .env.example .env
```

Editar `.env` con sus valores reales:

```env
DATABASE_URL=postgresql://air_quality_user:your_password@localhost:5432/air_quality_db
JWT_SECRET_KEY=your-super-secret-jwt-key-here
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
ENCRYPTION_KEY=your-32-byte-encryption-key-here
```

### 6. Inicializar la base de datos

```bash
python scripts/init_db.py
```

Este comando creará todas las tablas, insertará datos de prueba y mostrará las credenciales de acceso.

### 7. Ejecutar la aplicación

```bash
python src/main.py
```

La API estará disponible en `http://localhost:5000`

Para verificar que funciona correctamente, visita `http://localhost:5000/health`

## Estructura del Proyecto

```
src/
├── domain/
│   ├── entities/          # Entidades de dominio
│   │   ├── usuario.py
│   │   ├── dispositivo.py
│   │   ├── lectura_calidad_aire.py
│   │   └── ...
│   └── ports/             # Interfaces (puertos)
│       ├── repositories/
│       └── services/
├── application/
│   └── use_cases/         # Casos de uso
├── infrastructure/
│   ├── database/          # Configuración de BD y modelos
│   ├── repositories/      # Implementaciones de repositorios
│   ├── services/          # Servicios externos (Telegram, etc.)
│   ├── controllers/       # Controladores REST
│   └── middleware/        # Middleware de autenticación
├── config/                # Configuración general
└── utils/                 # Utilidades
```

## API Endpoints

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/refresh` - Refrescar token JWT

### Usuarios
- `GET /api/users` - Listar usuarios (Admin/Operador)
- `POST /api/users` - Crear usuario (Admin)
- `GET /api/users/{id}` - Obtener usuario
- `PUT /api/users/{id}` - Actualizar usuario
- `DELETE /api/users/{id}` - Eliminar usuario (Admin)

### Dispositivos
- `GET /api/devices` - Listar dispositivos
- `POST /api/devices` - Registrar dispositivo
- `GET /api/devices/{id}` - Obtener dispositivo
- `PUT /api/devices/{id}` - Actualizar dispositivo
- `DELETE /api/devices/{id}` - Eliminar dispositivo

### Lecturas
- `GET /api/readings/air-quality` - Obtener lecturas de calidad del aire
- `POST /api/readings/air-quality` - Registrar nueva lectura (Dispositivo)
- `GET /api/readings/temperature` - Obtener lecturas de temperatura
- `GET /api/readings/humidity` - Obtener lecturas de humedad

### Asignaciones de Limpieza
- `GET /api/assignments` - Listar asignaciones
- `POST /api/assignments` - Crear asignación
- `PUT /api/assignments/{id}` - Actualizar asignación
- `DELETE /api/assignments/{id}` - Eliminar asignación
- `GET /api/assignments/stats` - Estadísticas de asignaciones

## Uso del Sistema

### 1. Autenticación

```python
import requests

# Iniciar sesión
response = requests.post('http://localhost:5000/api/auth/login', json={
    "email": "admin@uninacional.edu.co",
    "password": "admin123"
})

token = response.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}
```

### 2. Registrar un dispositivo

```python
# Obtener token de dispositivo (solo para dispositivos IoT)
device_response = requests.post('http://localhost:5000/api/devices/register', json={
    "mac_address": "AA:BB:CC:DD:EE:FF",
    "model_id": 1,
    "room_id": 1
})

device_token = device_response.json()['device_token']
```

### 3. Enviar lecturas desde dispositivo

```python
# Enviar datos de calidad del aire
requests.post('http://localhost:5000/api/readings/air-quality', json={
    "pm2_5": 25.8,
    "pm10": 35.4,
    "temperature": 25.5,
    "humidity": 65.0
}, headers={'Authorization': f'Bearer {device_token}'})
```

## Desarrollo

### Ejecutar tests

```bash
pytest
```

### Ejecutar con Docker

```bash
docker-compose up --build
```

### Formateo de código

```bash
black src/
isort src/
```

## Contribución

1. Crear rama feature desde `develop`
2. Implementar cambios siguiendo los principios SOLID y arquitectura hexagonal
3. Agregar tests para nueva funcionalidad
4. Hacer pull request con descripción detallada

## Licencia

Este proyecto está bajo la Licencia MIT.

## Contacto

Para preguntas o soporte, contactar al equipo de desarrollo.