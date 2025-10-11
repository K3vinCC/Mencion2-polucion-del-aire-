# 🧪 Script de Pruebas Completas - API UNI

Write-Host "🧪 Iniciando pruebas completas de la API UNI" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Gray

$errores = 0
$exitos = 0

function Test-Endpoint {
    param(
        [string]$Nombre,
        [string]$Url,
        [hashtable]$Headers = @{},
        [string]$Metodo = "GET",
        [string]$Body = $null
    )
    
    Write-Host "`n🔍 Probando: $Nombre" -ForegroundColor Cyan
    Write-Host "   URL: $Url" -ForegroundColor Gray
    
    try {
        if ($Body) {
            $result = Invoke-RestMethod -Uri $Url -Method $Metodo -Headers $Headers -ContentType "application/json" -Body $Body
        } else {
            $result = Invoke-RestMethod -Uri $Url -Method $Metodo -Headers $Headers
        }
        
        Write-Host "   ✅ ÉXITO" -ForegroundColor Green
        $script:exitos++
        return $result
    } catch {
        Write-Host "   ❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
        $script:errores++
        return $null
    }
}

# === PRUEBAS SIN AUTENTICACIÓN ===
Write-Host "`n🔓 PRUEBAS SIN AUTENTICACIÓN" -ForegroundColor Yellow

# 1. Health Check
$health = Test-Endpoint -Nombre "Health Check" -Url "http://localhost:5000/health"
if ($health) {
    Write-Host "   📊 Estado: $($health.estado)"
    Write-Host "   💬 Mensaje: $($health.mensaje)"
}

# 2. Información general
$info = Test-Endpoint -Nombre "Información General" -Url "http://localhost:5000/"
if ($info) {
    Write-Host "   🏫 Proyecto: $($info.proyecto)"
    Write-Host "   🎯 Propósito: $($info.proposito)"
}

# === PRUEBAS DE AUTENTICACIÓN ===
Write-Host "`n🔐 PRUEBAS DE AUTENTICACIÓN" -ForegroundColor Yellow

# Usuarios de prueba
$usuarios_prueba = @(
    @{ email = "admin@uni.edu.pe"; clave = "admin123"; esperado = "Admin_Universidad" }
    @{ email = "conserje@uni.edu.pe"; clave = "admin123"; esperado = "Conserje" }
    @{ email = "limpieza@uni.edu.pe"; clave = "admin123"; esperado = "Limpiador" }
)

$tokens = @{}

foreach ($usuario in $usuarios_prueba) {
    $loginData = @{
        email = $usuario.email
        clave = $usuario.clave
    } | ConvertTo-Json
    
    $response = Test-Endpoint -Nombre "Login $($usuario.email)" -Url "http://localhost:5000/login" -Metodo "POST" -Body $loginData
    
    if ($response) {
        Write-Host "   👤 Usuario: $($response.usuario.nombre_completo)"
        Write-Host "   🎭 Rol: $($response.usuario.rol)"
        Write-Host "   ⏰ Expira en: $($response.expira_en) segundos"
        
        if ($response.usuario.rol -eq $usuario.esperado) {
            Write-Host "   ✅ Rol correcto" -ForegroundColor Green
        } else {
            Write-Host "   ❌ Rol incorrecto. Esperado: $($usuario.esperado)" -ForegroundColor Red
        }
        
        $tokens[$usuario.email] = $response.token
    }
}

# === PRUEBAS CON AUTENTICACIÓN ===
Write-Host "`n🔒 PRUEBAS CON AUTENTICACIÓN" -ForegroundColor Yellow

# Usar token del admin para las pruebas
$adminToken = $tokens["admin@uni.edu.pe"]
if ($adminToken) {
    $headers = @{ "Authorization" = "Bearer $adminToken" }
    
    # 1. Usuarios
    $usuarios = Test-Endpoint -Nombre "Lista de Usuarios" -Url "http://localhost:5000/api/usuarios" -Headers $headers
    if ($usuarios) {
        Write-Host "   👥 Total usuarios: $($usuarios.total)"
        Write-Host "   📝 Usuarios encontrados:"
        foreach ($u in $usuarios.usuarios) {
            Write-Host "      • $($u.nombre_completo) ($($u.rol))"
        }
    }
    
    # 2. Dispositivos
    $dispositivos = Test-Endpoint -Nombre "Lista de Dispositivos" -Url "http://localhost:5000/api/dispositivos" -Headers $headers
    if ($dispositivos) {
        Write-Host "   📱 Total dispositivos: $($dispositivos.total)"
        Write-Host "   📍 Dispositivos encontrados:"
        foreach ($d in $dispositivos.dispositivos) {
            $icono = if ($d.estado -eq "conectado") { "🟢" } else { "🔴" }
            Write-Host "      $icono $($d.ubicacion) - $($d.estado)"
        }
    }
    
    # 3. Dashboard
    $dashboard = Test-Endpoint -Nombre "Dashboard" -Url "http://localhost:5000/api/dashboard" -Headers $headers
    if ($dashboard) {
        Write-Host "   📊 Estadísticas del dashboard:"
        Write-Host "      👥 Usuarios: $($dashboard.dashboard.total_usuarios)"
        Write-Host "      📱 Dispositivos: $($dashboard.dashboard.total_dispositivos)"
        Write-Host "      🟢 Conectados: $($dashboard.dashboard.dispositivos_conectados)"
        Write-Host "      🔴 Desconectados: $($dashboard.dashboard.dispositivos_desconectados)"
        Write-Host "      🌬️  Calidad aire: $($dashboard.dashboard.calidad_aire_promedio)"
    }
} else {
    Write-Host "❌ No se pudo obtener token de admin para pruebas autenticadas" -ForegroundColor Red
    $errores += 3
}

# === PRUEBAS DE AUTORIZACIÓN ===
Write-Host "`n🛡️ PRUEBAS DE AUTORIZACIÓN" -ForegroundColor Yellow

# Probar acceso con token de conserje
$conserjeToken = $tokens["conserje@uni.edu.pe"]
if ($conserjeToken) {
    $conserjeHeaders = @{ "Authorization" = "Bearer $conserjeToken" }
    
    $usuariosConserje = Test-Endpoint -Nombre "Usuarios (como Conserje)" -Url "http://localhost:5000/api/usuarios" -Headers $conserjeHeaders
    if ($usuariosConserje) {
        Write-Host "   ✅ Conserje puede ver usuarios" -ForegroundColor Green
    }
}

# === PRUEBAS DE ERRORES ===
Write-Host "`n🚨 PRUEBAS DE MANEJO DE ERRORES" -ForegroundColor Yellow

# Token inválido
$headersBad = @{ "Authorization" = "Bearer token_invalido" }
Test-Endpoint -Nombre "Token Inválido" -Url "http://localhost:5000/api/usuarios" -Headers $headersBad

# Credenciales incorrectas
$loginBad = @{ email = "inexistente@test.com"; clave = "wrongpass" } | ConvertTo-Json
Test-Endpoint -Nombre "Credenciales Incorrectas" -Url "http://localhost:5000/login" -Metodo "POST" -Body $loginBad

# Endpoint inexistente
Test-Endpoint -Nombre "Endpoint Inexistente" -Url "http://localhost:5000/api/inexistente" -Headers $headers

# === RESUMEN FINAL ===
Write-Host "`n" + "=" * 60 -ForegroundColor Gray
Write-Host "📈 RESUMEN DE PRUEBAS" -ForegroundColor Green
Write-Host "✅ Pruebas exitosas: $exitos" -ForegroundColor Green
Write-Host "❌ Pruebas fallidas: $errores" -ForegroundColor Red
Write-Host "📊 Total ejecutadas: $($exitos + $errores)"

$porcentaje = if (($exitos + $errores) -gt 0) { [math]::Round(($exitos / ($exitos + $errores)) * 100, 2) } else { 0 }
Write-Host "🎯 Porcentaje de éxito: $porcentaje%" -ForegroundColor Cyan

if ($errores -eq 0) {
    Write-Host "`n🎉 ¡TODAS LAS PRUEBAS PASARON! API funcionando perfectamente." -ForegroundColor Green
} elseif ($porcentaje -ge 80) {
    Write-Host "`n⚠️  API funcionando con algunos errores menores." -ForegroundColor Yellow
} else {
    Write-Host "`n🚨 API tiene problemas significativos que requieren atención." -ForegroundColor Red
}

Write-Host "`nFecha de prueba: $(Get-Date)" -ForegroundColor Gray