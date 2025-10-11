# 🔧 Manual de Comandos Rápidos - API UNI

## 🚀 COMANDOS DE INICIO

### Iniciar el servidor API
```powershell
cd "C:\Users\jonaw\Documents\GitHub\Mencion2-polucion-del-aire-\APIconBaseDatosPostgreSQL"
python api_completa.py
```

### Verificar que el servidor funciona
```powershell
curl http://localhost:5000/health
```

### Login rápido (ejecutar en PowerShell)
```powershell
# Script automático de login
.\scripts\inicio_rapido.ps1

# Login manual
$loginData = @{ email = "admin@uni.edu.pe"; clave = "admin123" } | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -ContentType "application/json" -Body $loginData
$global:token = $response.token
$global:headers = @{ "Authorization" = "Bearer $global:token" }
```

## 📊 COMANDOS DE CONSULTA

### Ver usuarios
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/usuarios" -Headers $global:headers | ConvertTo-Json -Depth 10
```

### Ver dispositivos
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/dispositivos" -Headers $global:headers | ConvertTo-Json -Depth 10
```

### Ver dashboard
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/dashboard" -Headers $global:headers | ConvertTo-Json -Depth 10
```

### Información general de la API
```powershell
curl http://localhost:5000/
```

## 🔐 COMANDOS DE AUTENTICACIÓN

### Login con diferentes usuarios
```powershell
# Admin
$admin = @{ email = "admin@uni.edu.pe"; clave = "admin123" } | ConvertTo-Json
$responseAdmin = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -ContentType "application/json" -Body $admin

# Conserje
$conserje = @{ email = "conserje@uni.edu.pe"; clave = "admin123" } | ConvertTo-Json
$responseConserje = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -ContentType "application/json" -Body $conserje

# Limpiador
$limpieza = @{ email = "limpieza@uni.edu.pe"; clave = "admin123" } | ConvertTo-Json
$responseLimpieza = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -ContentType "application/json" -Body $limpieza
```

### Verificar token actual
```powershell
Write-Host "Token actual: $global:token"
```

## 🗄️ COMANDOS DE BASE DE DATOS

### Ver base de datos PostgreSQL
```powershell
# Conectar a PostgreSQL
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres -h localhost -d air_quality_db

# Una vez conectado, usar estos comandos SQL:
# \dt                    # Ver todas las tablas
# SELECT * FROM usuarios;  # Ver usuarios
# SELECT * FROM dispositivos;  # Ver dispositivos
# \q                     # Salir
```

### Ver base de datos con script Python
```powershell
cd "C:\Users\jonaw\Documents\GitHub\Mencion2-polucion-del-aire-\APIconBaseDatosPostgreSQL"
python view_database.py
```

## 🛠️ COMANDOS DE DIAGNÓSTICO

### Verificar procesos Python
```powershell
Get-Process python
```

### Verificar puerto 5000
```powershell
netstat -an | findstr :5000
```

### Detener todos los procesos Python
```powershell
taskkill /f /im python.exe
```

### Verificar PostgreSQL
```powershell
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres -h localhost -c "SELECT version();"
```

## 🧪 COMANDOS DE PRUEBAS

### Ejecutar pruebas completas
```powershell
.\scripts\pruebas_completas.ps1
```

### Monitoreo en tiempo real
```powershell
.\scripts\monitoreo.ps1
```

### Backup de datos
```powershell
.\scripts\backup_datos.ps1
```

## 📱 COMANDOS AVANZADOS

### Crear headers personalizados
```powershell
$headers = @{ 
    "Authorization" = "Bearer $global:token"
    "Content-Type" = "application/json"
    "User-Agent" = "PowerShell-UNI-Client/1.0"
}
```

### Request con manejo de errores
```powershell
try {
    $result = Invoke-RestMethod -Uri "http://localhost:5000/api/usuarios" -Headers $global:headers
    Write-Host "✅ Éxito: $($result.mensaje)" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}
```

### Guardar respuesta en archivo
```powershell
$usuarios = Invoke-RestMethod -Uri "http://localhost:5000/api/usuarios" -Headers $global:headers
$usuarios | ConvertTo-Json -Depth 10 | Out-File "usuarios_$(Get-Date -Format 'yyyy-MM-dd').json"
```

### Monitoreo de un solo comando
```powershell
while ($true) {
    Clear-Host
    $dashboard = Invoke-RestMethod -Uri "http://localhost:5000/api/dashboard" -Headers $global:headers
    Write-Host "📊 Dashboard UNI - $(Get-Date)"
    Write-Host "Dispositivos conectados: $($dashboard.dashboard.dispositivos_conectados)"
    Start-Sleep -Seconds 10
}
```

## 🔄 COMANDOS DE MANTENIMIENTO

### Reiniciar servidor
```powershell
# Detener
taskkill /f /im python.exe

# Esperar
Start-Sleep -Seconds 3

# Iniciar
cd "C:\Users\jonaw\Documents\GitHub\Mencion2-polucion-del-aire-\APIconBaseDatosPostgreSQL"
python api_completa.py
```

### Limpiar cache de Python
```powershell
Get-ChildItem -Path . -Include "__pycache__" -Recurse -Directory | Remove-Item -Recurse -Force
```

### Ver logs del servidor (si estuviera configurado)
```powershell
Get-Content -Path "api.log" -Tail 50 -Wait
```

## 🎯 COMANDOS ÚTILES DE UNA LÍNEA

```powershell
# Login rápido y ver usuarios
$r = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -ContentType "application/json" -Body (@{email="admin@uni.edu.pe";clave="admin123"}|ConvertTo-Json); $h = @{"Authorization"="Bearer $($r.token)"}; Invoke-RestMethod -Uri "http://localhost:5000/api/usuarios" -Headers $h

# Verificar salud y hacer login
curl http://localhost:5000/health; $r = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -ContentType "application/json" -Body (@{email="admin@uni.edu.pe";clave="admin123"}|ConvertTo-Json); Write-Host "Token: $($r.token)"

# Dashboard rápido
$r = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -ContentType "application/json" -Body (@{email="admin@uni.edu.pe";clave="admin123"}|ConvertTo-Json); Invoke-RestMethod -Uri "http://localhost:5000/api/dashboard" -Headers @{"Authorization"="Bearer $($r.token)"}
```

## 📚 COMANDOS DE DOCUMENTACIÓN

### Generar documentación de endpoints
```powershell
curl http://localhost:5000/ | ConvertFrom-Json | ConvertTo-Json -Depth 10 | Out-File "endpoints_disponibles.json"
```

### Exportar toda la información
```powershell
.\scripts\backup_datos.ps1 -CarpetaDestino "exportacion_completa"
```

---

**💡 TIP:** Guarda estos comandos en un archivo `.ps1` para reutilizarlos fácilmente.

**🎯 Para automatizar:** Crea alias en tu perfil de PowerShell para los comandos más usados.

```powershell
# Agregar al perfil de PowerShell
Set-Alias -Name "uni-login" -Value "C:\ruta\a\inicio_rapido.ps1"
Set-Alias -Name "uni-test" -Value "C:\ruta\a\pruebas_completas.ps1"
```