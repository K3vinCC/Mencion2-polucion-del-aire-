# Sistema de Monitoreo de Calidad del Aire

## 📋 Descripción
Sistema de monitoreo de calidad del aire para campus universitarios, implementando una arquitectura hexagonal (puertos y adaptadores) con Flask. El sistema permite gestionar dispositivos de monitoreo, usuarios y datos de calidad del aire en diferentes edificios y campus.

## 🛠️ Tecnologías Utilizadas
- Python 3.x
- Flask (Framework web)
- SQLite (Base de datos)
- JWT (JSON Web Tokens para autenticación)
- bcrypt (Para hash de contraseñas)
- Arquitectura Hexagonal (Puertos y Adaptadores)

## 🏗️ Estructura del Proyecto
```
backend/
├── api_monitoreo/
│   ├── src/
│   │   ├── domain/          # Reglas de negocio y entidades
│   │   ├── application/     # Casos de uso
│   │   ├── infrastructure/  # Configuración y dependencias
│   │   └── adapters/        # Implementaciones concretas
│   ├── schema.sql          # Esquema de la base de datos
│   └── run.py             # Punto de entrada de la aplicación
```

## 🚀 Instalación y Configuración

1. Clonar el repositorio:
```bash
git clone https://github.com/K3vinCC/Mencion2-polucion-del-aire-.git
cd Mencion2-polucion-del-aire-/backend/api_monitoreo
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Unix o MacOS:
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install flask python-dotenv bcrypt PyJWT
```

4. Configurar variables de entorno:
Crear archivo `.env` en la raíz del proyecto:
```env
SECRET_KEY=tu_clave_secreta_aqui
PORT=5000
```

5. Inicializar la base de datos:
```bash
Get-Content schema.sql | sqlite3 database.db
```

## 🔧 Uso

### Iniciar el servidor
```bash
flask run
```
El servidor estará disponible en `http://127.0.0.1:5000`

### Endpoints de la API

#### Registro de Usuario
```http
POST /api/register
Content-Type: application/json

{
    "nombre": "Usuario Ejemplo",
    "correo": "usuario@ejemplo.com",
    "clave": "contraseña123",
    "rol": "administrador"
}
```

#### Inicio de Sesión
```http
POST /api/login
Content-Type: application/json

{
    "correo": "usuario@ejemplo.com",
    "clave": "contraseña123"
}
```

## 📊 Estructura de la Base de Datos

El sistema utiliza SQLite con las siguientes tablas principales:
- `campus`: Registro de campus universitarios
- `edificios`: Edificios dentro de cada campus
- `modelos_dispositivo`: Catálogo de dispositivos de monitoreo
- `dispositivos`: Dispositivos físicos instalados
- `usuarios`: Gestión de usuarios del sistema

## 👥 Integrantes del Proyecto
- Kevin Cortes
- Jonathan Huinca
- Rodrigo Sevilla

## 🔐 Seguridad
- Autenticación mediante JWT
- Contraseñas hasheadas con bcrypt
- Validación de datos de entrada
- Manejo de errores personalizado

## ⚙️ Arquitectura

El proyecto sigue una arquitectura hexagonal (ports & adapters) con las siguientes capas:

1. **Domain**: Entidades y reglas de negocio core
2. **Application**: Casos de uso e interfaces del sistema
3. **Infrastructure**: Configuración y gestión de dependencias
4. **Adapters**: Implementaciones concretas (web, persistencia)

## 📝 Características Principales
- Registro y autenticación de usuarios
- Gestión de roles (administrador, conserje)
- Monitoreo de dispositivos por edificio
- Sistema de mantenimiento y seguimiento
- API RESTful con JWT

## 🤝 Contribución
Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE.md para detalles