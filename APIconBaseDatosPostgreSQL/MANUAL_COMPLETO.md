# 📚 MANUAL COMPLETO - API de Monitoreo de Calidad del Aire UNI

## 🎯 **Índice**
1. [Introducción](#introducción)
2. [Configuración Inicial](#configuración-inicial)
3. [Autenticación y Tokens JWT](#autenticación-y-tokens-jwt)
4. [Endpoints de la API](#endpoints-de-la-api)
5. [Gestión de Base de Datos](#gestión-de-base-de-datos)
6. [Ejemplos Prácticos](#ejemplos-prácticos)
7. [Troubleshooting](#troubleshooting)
8. [Scripts Útiles](#scripts-útiles)

---

## 🎯 **Introducción**

### **¿Qué es esta API?**
Sistema RESTful para monitoreo de calidad del aire en instituciones educativas, desarrollado para la Universidad Nacional de Ingeniería (UNI).

### **Características principales:**
- ✅ **Autenticación JWT** (12 horas de duración)
- ✅ **Base de datos PostgreSQL** con datos de prueba
- ✅ **Roles de usuario** (SuperAdmin, Admin_Universidad, Conserje, Limpiador)
- ✅ **Gestión de dispositivos IoT**
- ✅ **Monitoreo en tiempo real**
- ✅ **Dashboard con estadísticas**

---

## ⚙️ **Configuración Inicial**

### **1. Verificar que el servidor esté ejecutándose**

```powershell
# Verificar si el puerto 5000 está ocupado
netstat -an | findstr :5000
```

**Si no hay respuesta, iniciar el servidor:**
```powershell
cd "C:\Users\jonaw\Documents\GitHub\Mencion2-polucion-del-aire-\APIconBaseDatosPostgreSQL"
python api_completa.py
```

**Deberías ver:**
```
🚀 Iniciando API COMPLETA de Monitoreo de Calidad del Aire - UNI
======================================================================
🌐 Servidor: http://localhost:5000
🔐 Login: POST /login
...
```

### **2. Verificar que la API responde**

```powershell
curl http://localhost:5000/health
```

**Respuesta esperada:**
```json
{
  "estado": "saludable",
  "mensaje": "🚀 API UNI funcionando correctamente",
  "version": "2.0.0"
}
```

---

## 🔐 **Autenticación y Tokens JWT**

### **Credenciales de Prueba**

| Usuario | Email | Contraseña | Rol |
|---------|-------|------------|-----|
| Admin | `admin@uni.edu.pe` | `admin123` | Admin_Universidad |
| Conserje | `conserje@uni.edu.pe` | `admin123` | Conserje |
| Limpiador | `limpieza@uni.edu.pe` | `admin123` | Limpiador |

### **Paso 1: Hacer Login**

```powershell
# Preparar datos de login
$loginData = @{
    email = "admin@uni.edu.pe"
    clave = "admin123"
} | ConvertTo-Json

# Hacer login
$response = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -ContentType "application/json" -Body $loginData

# Ver respuesta
Write-Host "✅ LOGIN EXITOSO!"
Write-Host "Token: Bearer $($response.token)"
Write-Host "Usuario: $($response.usuario.nombre_completo)"
Write-Host "Rol: $($response.usuario.rol)"

# Guardar token para usar después
$global:token = $response.token
```

**Respuesta esperada:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expira_en": 43200,
  "tipo": "Bearer",
  "usuario": {
    "id": 1,
    "email": "admin@uni.edu.pe",
    "nombre_completo": "Administrador UNI",
    "rol": "Admin_Universidad"
  }
}
```

### **Paso 2: Usar el Token**

Para todos los endpoints protegidos, necesitas incluir el token:

```powershell
$headers = @{ "Authorization" = "Bearer $global:token" }
```

---

## 🌐 **Endpoints de la API**

### **📋 Listado Completo de Endpoints**

| Método | Endpoint | Descripción | Requiere Token |
|--------|----------|-------------|----------------|
| GET | `/` | Información general | ❌ |
| GET | `/health` | Estado del servidor | ❌ |
| POST | `/login` | Autenticación | ❌ |
| GET | `/api/usuarios` | Lista de usuarios | ✅ |
| GET | `/api/dispositivos` | Lista de dispositivos IoT | ✅ |
| GET | `/api/dashboard` | Dashboard con estadísticas | ✅ |

### **🔓 Endpoints Públicos (sin token)**

#### **1. Información General**
```powershell
curl http://localhost:5000/
```

#### **2. Health Check**
```powershell
curl http://localhost:5000/health
```

#### **3. Login**
```powershell
$loginData = @{ email = "admin@uni.edu.pe"; clave = "admin123" } | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -ContentType "application/json" -Body $loginData
```

### **🔒 Endpoints Protegidos (requieren token)**

#### **1. Ver Usuarios**
```powershell
$headers = @{ "Authorization" = "Bearer $global:token" }
$usuarios = Invoke-RestMethod -Uri "http://localhost:5000/api/usuarios" -Headers $headers
$usuarios | ConvertTo-Json -Depth 10
```

**Respuesta:**
```json
{
  "usuarios": [
    {
      "id": 1,
      "email": "admin@uni.edu.pe",
      "nombre_completo": "Administrador UNI",
      "rol": "Admin_Universidad",
      "universidad": "Universidad Nacional de Ingeniería"
    }
  ],
  "total": 3,
  "mensaje": "👥 Usuarios obtenidos exitosamente"
}
```

#### **2. Ver Dispositivos IoT**
```powershell
$dispositivos = Invoke-RestMethod -Uri "http://localhost:5000/api/dispositivos" -Headers $headers
$dispositivos | ConvertTo-Json -Depth 10
```

**Respuesta:**
```json
{
  "dispositivos": [
    {
      "id": 1,
      "mac_address": "AA:BB:CC:DD:EE:FF",
      "ubicacion": "Aula 101 - Edificio Sistemas",
      "estado": "conectado",
      "modelo": "ESP32-DHT22-PMS5003"
    }
  ],
  "total": 3,
  "mensaje": "📱 Dispositivos obtenidos exitosamente"
}
```

#### **3. Ver Dashboard**
```powershell
$dashboard = Invoke-RestMethod -Uri "http://localhost:5000/api/dashboard" -Headers $headers
$dashboard | ConvertTo-Json -Depth 10
```

**Respuesta:**
```json
{
  "dashboard": {
    "total_usuarios": 3,
    "total_dispositivos": 3,
    "dispositivos_conectados": 2,
    "dispositivos_desconectados": 1,
    "calidad_aire_promedio": "Buena"
  },
  "mensaje": "📊 Dashboard obtenido exitosamente"
}
```

---

## 🗄️ **Gestión de Base de Datos**

### **Ver Base de Datos PostgreSQL**

#### **Opción 1: Usando pgAdmin (Interfaz Gráfica)**
1. Abrir pgAdmin 4
2. Conectar a servidor:
   - Host: `localhost`
   - Puerto: `5432`
   - Usuario: `postgres`
   - Contraseña: `password`
3. Expandir `air_quality_db`
4. Ver tablas en `Schemas > public > Tables`

#### **Opción 2: Línea de Comandos**
```powershell
# Conectar a PostgreSQL
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres -h localhost -d air_quality_db

# Ver todas las tablas
\dt

# Ver usuarios
SELECT * FROM usuarios;

# Ver dispositivos
SELECT * FROM dispositivos;

# Salir
\q
```

#### **Opción 3: Script Python**
```powershell
cd "C:\Users\jonaw\Documents\GitHub\Mencion2-polucion-del-aire-\APIconBaseDatosPostgreSQL"
python view_database.py
```

### **Estructura de la Base de Datos**

#### **Tabla: usuarios**
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único |
| email | TEXT | Email único |
| clave_hash | TEXT | Contraseña hasheada |
| nombre_completo | TEXT | Nombre del usuario |
| rol | TEXT | Rol del sistema |
| universidad | TEXT | Universidad |

#### **Tabla: dispositivos**
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único |
| mac_address | TEXT | MAC del dispositivo |
| ubicacion | TEXT | Ubicación física |
| estado | TEXT | conectado/desconectado |
| modelo | TEXT | Modelo del dispositivo |

---

## 💻 **Ejemplos Prácticos**

### **Script Completo de Prueba**

```powershell
# === SCRIPT COMPLETO DE PRUEBA API UNI ===
Write-Host "🚀 Iniciando pruebas de API UNI" -ForegroundColor Green

# 1. Verificar servidor
try {
    $health = Invoke-RestMethod -Uri "http://localhost:5000/health"
    Write-Host "✅ Servidor funcionando: $($health.mensaje)" -ForegroundColor Green
} catch {
    Write-Host "❌ Servidor no disponible" -ForegroundColor Red
    exit
}

# 2. Login
Write-Host "`n🔐 Haciendo login..." -ForegroundColor Yellow
$loginData = @{
    email = "admin@uni.edu.pe"
    clave = "admin123"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -ContentType "application/json" -Body $loginData
    Write-Host "✅ Login exitoso!" -ForegroundColor Green
    Write-Host "Usuario: $($response.usuario.nombre_completo)"
    Write-Host "Rol: $($response.usuario.rol)"
    $global:token = $response.token
} catch {
    Write-Host "❌ Error en login: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

# 3. Headers para requests autenticados
$headers = @{ "Authorization" = "Bearer $global:token" }

# 4. Ver usuarios
Write-Host "`n👥 Obteniendo usuarios..." -ForegroundColor Yellow
try {
    $usuarios = Invoke-RestMethod -Uri "http://localhost:5000/api/usuarios" -Headers $headers
    Write-Host "✅ Usuarios obtenidos: $($usuarios.total)"
    foreach ($usuario in $usuarios.usuarios) {
        Write-Host "  • $($usuario.nombre_completo) ($($usuario.rol))"
    }
} catch {
    Write-Host "❌ Error obteniendo usuarios: $($_.Exception.Message)" -ForegroundColor Red
}

# 5. Ver dispositivos
Write-Host "`n📱 Obteniendo dispositivos..." -ForegroundColor Yellow
try {
    $dispositivos = Invoke-RestMethod -Uri "http://localhost:5000/api/dispositivos" -Headers $headers
    Write-Host "✅ Dispositivos obtenidos: $($dispositivos.total)"
    foreach ($dispositivo in $dispositivos.dispositivos) {
        Write-Host "  • $($dispositivo.ubicacion) - $($dispositivo.estado)"
    }
} catch {
    Write-Host "❌ Error obteniendo dispositivos: $($_.Exception.Message)" -ForegroundColor Red
}

# 6. Ver dashboard
Write-Host "`n📊 Obteniendo dashboard..." -ForegroundColor Yellow
try {
    $dashboard = Invoke-RestMethod -Uri "http://localhost:5000/api/dashboard" -Headers $headers
    Write-Host "✅ Dashboard obtenido!"
    Write-Host "  • Total usuarios: $($dashboard.dashboard.total_usuarios)"
    Write-Host "  • Total dispositivos: $($dashboard.dashboard.total_dispositivos)"
    Write-Host "  • Conectados: $($dashboard.dashboard.dispositivos_conectados)"
    Write-Host "  • Calidad aire: $($dashboard.dashboard.calidad_aire_promedio)"
} catch {
    Write-Host "❌ Error obteniendo dashboard: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎉 Pruebas completadas!" -ForegroundColor Green
```

### **Probando con diferentes usuarios**

```powershell
# Probar con usuario Conserje
$loginConserje = @{
    email = "conserje@uni.edu.pe"
    clave = "admin123"
} | ConvertTo-Json

$responseConserje = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -ContentType "application/json" -Body $loginConserje
$tokenConserje = $responseConserje.token
$headersConserje = @{ "Authorization" = "Bearer $tokenConserje" }

# Ver dispositivos como conserje
$dispositivosConserje = Invoke-RestMethod -Uri "http://localhost:5000/api/dispositivos" -Headers $headersConserje
Write-Host "Dispositivos vistos por conserje: $($dispositivosConserje.total)"
```

---

## 🛠️ **Troubleshooting**

### **Problemas Comunes**

#### **1. Error: "No es posible conectar con el servidor remoto"**
```powershell
# Verificar si el servidor está ejecutándose
netstat -an | findstr :5000

# Si no hay respuesta, iniciar servidor
python "C:\Users\jonaw\Documents\GitHub\Mencion2-polucion-del-aire-\APIconBaseDatosPostgreSQL\api_completa.py"
```

#### **2. Error: "Token inválido o expirado"**
```powershell
# Hacer login nuevamente
$loginData = @{ email = "admin@uni.edu.pe"; clave = "admin123" } | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -ContentType "application/json" -Body $loginData
$global:token = $response.token
```

#### **3. Error: "404 Not Found"**
- Verificar que la URL esté correcta
- Verificar que el endpoint exista en la API

#### **4. Error de CORS**
- Solo aplica en navegadores
- Usar PowerShell o Postman para evitarlo

### **Comandos de Diagnóstico**

```powershell
# Ver procesos Python ejecutándose
Get-Process python

# Detener todos los procesos Python
taskkill /f /im python.exe

# Ver información del sistema
curl http://localhost:5000/

# Verificar base de datos PostgreSQL
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres -h localhost -c "SELECT version();"
```

---

## 📜 **Scripts Útiles**

### **1. Script de Inicio Rápido**

```powershell
# inicio_rapido.ps1
param(
    [string]$Usuario = "admin@uni.edu.pe",
    [string]$Clave = "admin123"
)

Write-Host "🚀 Inicio rápido API UNI" -ForegroundColor Green

# Login
$loginData = @{ email = $Usuario; clave = $Clave } | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -ContentType "application/json" -Body $loginData
$global:token = $response.token
$global:headers = @{ "Authorization" = "Bearer $global:token" }

Write-Host "✅ Login exitoso para: $($response.usuario.nombre_completo)"
Write-Host "Token guardado en `$global:token"
Write-Host "Headers guardados en `$global:headers"
```

### **2. Script de Monitoreo**

```powershell
# monitoreo.ps1
while ($true) {
    try {
        $dashboard = Invoke-RestMethod -Uri "http://localhost:5000/api/dashboard" -Headers $global:headers
        Clear-Host
        Write-Host "📊 DASHBOARD UNI - $(Get-Date)" -ForegroundColor Green
        Write-Host "================================"
        Write-Host "👥 Usuarios: $($dashboard.dashboard.total_usuarios)"
        Write-Host "📱 Dispositivos: $($dashboard.dashboard.total_dispositivos)"
        Write-Host "🟢 Conectados: $($dashboard.dashboard.dispositivos_conectados)"
        Write-Host "🔴 Desconectados: $($dashboard.dashboard.dispositivos_desconectados)"
        Write-Host "🌬️  Calidad aire: $($dashboard.dashboard.calidad_aire_promedio)"
    } catch {
        Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Start-Sleep -Seconds 30
}
```

### **3. Script de Backup de Datos**

```powershell
# backup_datos.ps1
$fecha = Get-Date -Format "yyyy-MM-dd_HH-mm"
$carpeta = "backup_$fecha"
New-Item -ItemType Directory -Name $carpeta

# Exportar usuarios
$usuarios = Invoke-RestMethod -Uri "http://localhost:5000/api/usuarios" -Headers $global:headers
$usuarios | ConvertTo-Json -Depth 10 | Out-File "$carpeta\usuarios.json"

# Exportar dispositivos
$dispositivos = Invoke-RestMethod -Uri "http://localhost:5000/api/dispositivos" -Headers $global:headers
$dispositivos | ConvertTo-Json -Depth 10 | Out-File "$carpeta\dispositivos.json"

# Exportar dashboard
$dashboard = Invoke-RestMethod -Uri "http://localhost:5000/api/dashboard" -Headers $global:headers
$dashboard | ConvertTo-Json -Depth 10 | Out-File "$carpeta\dashboard.json"

Write-Host "✅ Backup completado en carpeta: $carpeta"
```

---

## 🎓 **Conclusión**

### **¿Qué has logrado?**
- ✅ **API completa** de monitoreo de calidad del aire
- ✅ **Autenticación JWT** funcional
- ✅ **Base de datos PostgreSQL** con datos reales
- ✅ **Endpoints protegidos** con roles de usuario
- ✅ **Dashboard** con estadísticas en tiempo real

### **Próximos pasos sugeridos:**
1. **Expandir endpoints** (crear, editar, eliminar)
2. **Agregar más sensores** de calidad del aire
3. **Implementar notificaciones** por Telegram
4. **Crear interfaz web** con React/Vue
5. **Desplegar en producción** con Docker

### **Recursos adicionales:**
- 📖 Documentación PostgreSQL: https://www.postgresql.org/docs/
- 🔐 JWT Tokens: https://jwt.io/
- 🐍 Flask API: https://flask.palletsprojects.com/
- 📊 Swagger UI: https://swagger.io/tools/swagger-ui/

---

**🎉 ¡Tu sistema de monitoreo de calidad del aire está completamente funcional!**

Fecha de creación: Septiembre 2025  
Versión: 2.0.0  
Autor: Sistema UNI