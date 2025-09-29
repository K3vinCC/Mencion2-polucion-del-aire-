# 🎯 GUÍA DE INICIO RÁPIDO - API UNI

## ⚡ **En 3 pasos, tendrás tu API funcionando:**

### **Paso 1: Iniciar el servidor** 🚀
```powershell
cd "C:\Users\jonaw\Documents\GitHub\Mencion2-polucion-del-aire-\APIconBaseDatosPostgreSQL"
python api_completa.py
```
*Deberías ver: "🚀 Iniciando API COMPLETA de Monitoreo de Calidad del Aire - UNI"*

### **Paso 2: Hacer login** 🔐
```powershell
# Abrir otra terminal PowerShell y ejecutar:
.\scripts\inicio_rapido.ps1
```
*Esto te dará acceso completo a la API*

### **Paso 3: Probar la API** 🧪
```powershell
# Ver usuarios
Invoke-RestMethod -Uri "http://localhost:5000/api/usuarios" -Headers $global:headers

# Ver dispositivos
Invoke-RestMethod -Uri "http://localhost:5000/api/dispositivos" -Headers $global:headers

# Ver dashboard
Invoke-RestMethod -Uri "http://localhost:5000/api/dashboard" -Headers $global:headers
```

## 🎉 **¡Listo!** Ya tienes:
- ✅ API completa funcionando
- ✅ Autenticación JWT
- ✅ Base de datos PostgreSQL
- ✅ 3 usuarios de prueba
- ✅ 3 dispositivos IoT simulados
- ✅ Dashboard con estadísticas

## 📚 **Documentación completa:**
- 📖 **Manual detallado**: `MANUAL_COMPLETO.md`
- ⚡ **Comandos rápidos**: `COMANDOS_RAPIDOS.md`
- 🧪 **Scripts útiles**: Carpeta `scripts/`

## 🆘 **¿Problemas?**
```powershell
# Verificar que el servidor funciona:
curl http://localhost:5000/health

# Si hay errores, reiniciar:
taskkill /f /im python.exe
python api_completa.py
```

**🎯 Usuario de prueba:**
- Email: `admin@uni.edu.pe`
- Contraseña: `admin123`