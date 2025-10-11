# 📊 Script de Monitoreo en Tiempo Real - API UNI

Write-Host "📊 Iniciando monitoreo en tiempo real..." -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Yellow
Write-Host ""

# Verificar que tenemos el token
if (-not $global:token) {
    Write-Host "❌ No hay token disponible. Ejecuta primero inicio_rapido.ps1" -ForegroundColor Red
    exit
}

$headers = @{ "Authorization" = "Bearer $global:token" }

while ($true) {
    try {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        
        # Obtener datos del dashboard
        $dashboard = Invoke-RestMethod -Uri "http://localhost:5000/api/dashboard" -Headers $headers
        
        # Obtener dispositivos para estado detallado
        $dispositivos = Invoke-RestMethod -Uri "http://localhost:5000/api/dispositivos" -Headers $headers
        
        Clear-Host
        Write-Host "🏫 MONITOREO UNI - CALIDAD DEL AIRE" -ForegroundColor Green
        Write-Host "=" * 50 -ForegroundColor Gray
        Write-Host "🕒 Última actualización: $timestamp" -ForegroundColor Cyan
        Write-Host ""
        
        # Dashboard general
        Write-Host "📊 RESUMEN GENERAL" -ForegroundColor Yellow
        Write-Host "  👥 Total usuarios: $($dashboard.dashboard.total_usuarios)"
        Write-Host "  📱 Total dispositivos: $($dashboard.dashboard.total_dispositivos)"
        Write-Host "  🟢 Conectados: $($dashboard.dashboard.dispositivos_conectados)" -ForegroundColor Green
        Write-Host "  🔴 Desconectados: $($dashboard.dashboard.dispositivos_desconectados)" -ForegroundColor Red
        Write-Host "  🌬️  Calidad aire promedio: $($dashboard.dashboard.calidad_aire_promedio)" -ForegroundColor Cyan
        Write-Host ""
        
        # Estado detallado de dispositivos
        Write-Host "📱 ESTADO DE DISPOSITIVOS" -ForegroundColor Yellow
        foreach ($dispositivo in $dispositivos.dispositivos) {
            $icono = if ($dispositivo.estado -eq "conectado") { "🟢" } else { "🔴" }
            $color = if ($dispositivo.estado -eq "conectado") { "Green" } else { "Red" }
            Write-Host "  $icono $($dispositivo.ubicacion)" -ForegroundColor $color
            Write-Host "    MAC: $($dispositivo.mac_address)"
            Write-Host "    Modelo: $($dispositivo.modelo)"
            Write-Host ""
        }
        
        Write-Host "⏱️  Actualizando en 30 segundos..." -ForegroundColor Gray
        
    } catch {
        Write-Host "❌ Error obteniendo datos: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Reintentando en 30 segundos..." -ForegroundColor Yellow
    }
    
    Start-Sleep -Seconds 30
}