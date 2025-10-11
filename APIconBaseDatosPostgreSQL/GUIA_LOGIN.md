# 🔐 GUÍA COMPLETA DE LOGIN - API SISTEMA UNI

## ✅ CREDENCIALES DE PRUEBA
```
Email: admin@uni.edu.pe
Password: admin123
```

## 🌐 MÉTODO 1: Navegador (Swagger UI)

### Paso 1: Abrir Swagger UI
```
http://localhost:5000/api/docs
```

### Paso 2: Si hay error CORS, usar Postman o hacer login manual

## 💻 MÉTODO 2: PowerShell/Terminal

### Hacer Login:
```powershell
$loginData = @{
    email = "admin@uni.edu.pe"
    password = "admin123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:5000/api/auth/login" -Method POST -ContentType "application/json" -Body $loginData

# Obtener token
$token = $response.token
Write-Host "Token: Bearer $token"
```

### Usar Token para ver datos:
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
}

# Ver usuarios
Invoke-RestMethod -Uri "http://localhost:5000/api/users" -Headers $headers

# Ver dispositivos  
Invoke-RestMethod -Uri "http://localhost:5000/api/devices" -Headers $headers
```

## 🛠️ MÉTODO 3: Postman

### 1. Login (POST)
```
URL: http://localhost:5000/api/auth/login
Method: POST
Headers: Content-Type: application/json
Body (raw JSON):
{
  "email": "admin@uni.edu.pe", 
  "password": "admin123"
}
```

### 2. Copiar Token de la respuesta

### 3. Usar en otros endpoints:
```
Headers: Authorization: Bearer [tu_token]
```

## 🔧 MÉTODO 4: Desactivar CORS en Chrome

Cerrar Chrome y ejecutar desde terminal:
```
chrome.exe --user-data-dir="C:/temp/chrome" --disable-web-security --disable-features=VizDisplayCompositor
```

## 📊 ENDPOINTS DISPONIBLES

Con el token puedes acceder a:

### 👥 Usuarios
- `GET /api/users` - Ver todos los usuarios
- `POST /api/users` - Crear usuario  
- `GET /api/users/{id}` - Ver usuario específico

### 📱 Dispositivos IoT
- `GET /api/devices` - Ver dispositivos
- `POST /api/devices` - Registrar dispositivo
- `GET /api/devices/{id}` - Ver dispositivo específico

### 📊 Lecturas de Sensores  
- `POST /api/readings/air-quality` - Enviar lectura de calidad del aire
- `GET /api/readings/air-quality` - Ver lecturas de aire
- `POST /api/readings/temperature` - Enviar temperatura
- `GET /api/readings/temperature` - Ver temperaturas

### 🧹 Asignaciones de Limpieza
- `POST /api/assignments` - Crear asignación
- `GET /api/assignments` - Ver asignaciones

### 📈 Dashboard
- `GET /api/dashboard/university/{id}` - Dashboard universidad
- `GET /api/dashboard/building/{id}` - Dashboard edificio

## 🎯 EJEMPLO COMPLETO

```json
// 1. Login Response:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 43200,
  "user": {
    "id": 1,
    "email": "admin@uni.edu.pe",
    "name": "Administrador UNI", 
    "role": "Admin_Universidad"
  }
}

// 2. Usar token en headers:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

// 3. Acceder a cualquier endpoint protegido
```

---
**💡 Recomendación: Usar Postman o PowerShell para evitar problemas de CORS**