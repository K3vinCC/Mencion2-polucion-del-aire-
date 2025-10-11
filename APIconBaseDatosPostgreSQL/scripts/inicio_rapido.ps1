# 🚀 Scripts Útiles - API UNI

## inicio_rapido.ps1
param(
    [string]$Usuario = "admin@uni.edu.pe",
    [string]$Clave = "admin123"
)

Write-Host "🚀 Inicio rápido API UNI" -ForegroundColor Green

# Verificar servidor
try {
    $health = Invoke-RestMethod -Uri "http://localhost:5000/health"
    Write-Host "✅ Servidor funcionando: $($health.mensaje)" -ForegroundColor Green
} catch {
    Write-Host "❌ Servidor no disponible. Iniciando servidor..." -ForegroundColor Red
    Write-Host "Ejecuta en otra terminal: python api_completa.py"
    exit
}

# Login
$loginData = @{ email = $Usuario; clave = $Clave } | ConvertTo-Json
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/login" -Method POST -ContentType "application/json" -Body $loginData
    $global:token = $response.token
    $global:headers = @{ "Authorization" = "Bearer $global:token" }

    Write-Host "✅ Login exitoso para: $($response.usuario.nombre_completo)" -ForegroundColor Green
    Write-Host "Rol: $($response.usuario.rol)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Variables creadas:" -ForegroundColor Yellow
    Write-Host "  `$global:token   - Token JWT"
    Write-Host "  `$global:headers - Headers con Authorization"
    Write-Host ""
    Write-Host "Ejemplos de uso:" -ForegroundColor Yellow
    Write-Host "  Invoke-RestMethod -Uri 'http://localhost:5000/api/usuarios' -Headers `$global:headers"
    Write-Host "  Invoke-RestMethod -Uri 'http://localhost:5000/api/dispositivos' -Headers `$global:headers"
    Write-Host "  Invoke-RestMethod -Uri 'http://localhost:5000/api/dashboard' -Headers `$global:headers"
} catch {
    Write-Host "❌ Error en login: $($_.Exception.Message)" -ForegroundColor Red
}