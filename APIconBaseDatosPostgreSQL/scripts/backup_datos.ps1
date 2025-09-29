# 💾 Script de Backup y Exportación - API UNI

param(
    [string]$CarpetaDestino = "backup_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss')"
)

Write-Host "💾 Iniciando backup de datos API UNI" -ForegroundColor Green
Write-Host "📁 Carpeta destino: $CarpetaDestino" -ForegroundColor Cyan

# Verificar que tenemos el token
if (-not $global:token) {
    Write-Host "❌ No hay token disponible. Ejecuta primero inicio_rapido.ps1" -ForegroundColor Red
    exit
}

$headers = @{ "Authorization" = "Bearer $global:token" }

# Crear carpeta de backup
try {
    New-Item -ItemType Directory -Name $CarpetaDestino -Force | Out-Null
    Write-Host "✅ Carpeta creada: $CarpetaDestino" -ForegroundColor Green
} catch {
    Write-Host "❌ Error creando carpeta: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

# Función para exportar datos
function Export-Data {
    param(
        [string]$Endpoint,
        [string]$Archivo,
        [string]$Descripcion
    )
    
    Write-Host "`n📤 Exportando $Descripcion..." -ForegroundColor Yellow
    
    try {
        $data = Invoke-RestMethod -Uri "http://localhost:5000$Endpoint" -Headers $headers
        $jsonData = $data | ConvertTo-Json -Depth 10
        $rutaArchivo = Join-Path $CarpetaDestino $Archivo
        $jsonData | Out-File -FilePath $rutaArchivo -Encoding UTF8
        
        Write-Host "   ✅ $Descripcion exportado a: $Archivo" -ForegroundColor Green
        Write-Host "   📊 Tamaño: $((Get-Item $rutaArchivo).Length) bytes"
        
        return $data
    } catch {
        Write-Host "   ❌ Error exportando $Descripcion`: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# === EXPORTAR DATOS ===

# 1. Usuarios
$usuarios = Export-Data -Endpoint "/api/usuarios" -Archivo "usuarios.json" -Descripcion "usuarios"
if ($usuarios) {
    Write-Host "   👥 Total usuarios exportados: $($usuarios.total)"
}

# 2. Dispositivos
$dispositivos = Export-Data -Endpoint "/api/dispositivos" -Archivo "dispositivos.json" -Descripcion "dispositivos"
if ($dispositivos) {
    Write-Host "   📱 Total dispositivos exportados: $($dispositivos.total)"
}

# 3. Dashboard
$dashboard = Export-Data -Endpoint "/api/dashboard" -Archivo "dashboard.json" -Descripcion "dashboard"
if ($dashboard) {
    Write-Host "   📊 Dashboard exportado exitosamente"
}

# === CREAR RESUMEN ===
Write-Host "`n📝 Creando resumen del backup..." -ForegroundColor Yellow

$resumen = @{
    "fecha_backup" = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "version_api" = "2.0.0"
    "total_usuarios" = if ($usuarios) { $usuarios.total } else { 0 }
    "total_dispositivos" = if ($dispositivos) { $dispositivos.total } else { 0 }
    "archivos_exportados" = @()
}

# Listar archivos creados
$archivosCreados = Get-ChildItem -Path $CarpetaDestino -File
foreach ($archivo in $archivosCreados) {
    $resumen.archivos_exportados += @{
        "nombre" = $archivo.Name
        "tamaño_bytes" = $archivo.Length
        "fecha_creacion" = $archivo.CreationTime.ToString("yyyy-MM-dd HH:mm:ss")
    }
}

# Guardar resumen
$resumenJson = $resumen | ConvertTo-Json -Depth 10
$rutaResumen = Join-Path $CarpetaDestino "resumen_backup.json"
$resumenJson | Out-File -FilePath $rutaResumen -Encoding UTF8

# === CREAR ARCHIVO README ===
$readmeContent = @"
# 📋 Backup API UNI - $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## 📊 Resumen
- **Fecha del backup**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
- **Versión API**: 2.0.0
- **Total usuarios**: $($resumen.total_usuarios)
- **Total dispositivos**: $($resumen.total_dispositivos)

## 📁 Archivos incluidos
$(foreach ($archivo in $resumen.archivos_exportados) {
"- **$($archivo.nombre)** - $($archivo.tamaño_bytes) bytes"
})

## 🔄 Cómo restaurar
1. Asegúrate de que la API esté funcionando
2. Ejecuta el script de login: ``inicio_rapido.ps1``
3. Los datos JSON pueden ser importados usando los endpoints POST correspondientes

## 📞 Contacto
Sistema de Monitoreo de Calidad del Aire - UNI
"@

$rutaReadme = Join-Path $CarpetaDestino "README.md"
$readmeContent | Out-File -FilePath $rutaReadme -Encoding UTF8

# === CREAR SCRIPT DE VERIFICACIÓN ===
$scriptVerificacion = @"
# Script de verificación del backup
Write-Host "🔍 Verificando backup..." -ForegroundColor Green

`$archivos = @("usuarios.json", "dispositivos.json", "dashboard.json", "resumen_backup.json")

foreach (`$archivo in `$archivos) {
    if (Test-Path `$archivo) {
        `$tamaño = (Get-Item `$archivo).Length
        Write-Host "✅ `$archivo - `$tamaño bytes" -ForegroundColor Green
    } else {
        Write-Host "❌ `$archivo - NO ENCONTRADO" -ForegroundColor Red
    }
}

Write-Host "`n📊 Resumen del backup:"
`$resumen = Get-Content "resumen_backup.json" | ConvertFrom-Json
Write-Host "   📅 Fecha: `$(`$resumen.fecha_backup)"
Write-Host "   👥 Usuarios: `$(`$resumen.total_usuarios)"
Write-Host "   📱 Dispositivos: `$(`$resumen.total_dispositivos)"
"@

$rutaVerificacion = Join-Path $CarpetaDestino "verificar_backup.ps1"
$scriptVerificacion | Out-File -FilePath $rutaVerificacion -Encoding UTF8

# === RESUMEN FINAL ===
Write-Host "`n" + "=" * 60 -ForegroundColor Gray
Write-Host "🎉 BACKUP COMPLETADO" -ForegroundColor Green
Write-Host "📁 Carpeta: $CarpetaDestino" -ForegroundColor Cyan
Write-Host "📊 Archivos creados:" -ForegroundColor Yellow

Get-ChildItem -Path $CarpetaDestino -File | ForEach-Object {
    Write-Host "   📄 $($_.Name) - $($_.Length) bytes" -ForegroundColor White
}

$tamaño_total = (Get-ChildItem -Path $CarpetaDestino -File | Measure-Object -Property Length -Sum).Sum
Write-Host "`n💾 Tamaño total del backup: $tamaño_total bytes" -ForegroundColor Cyan

Write-Host "`n🔍 Para verificar el backup:"
Write-Host "   cd $CarpetaDestino"
Write-Host "   .\verificar_backup.ps1"

Write-Host "`n✅ Backup completado exitosamente!" -ForegroundColor Green