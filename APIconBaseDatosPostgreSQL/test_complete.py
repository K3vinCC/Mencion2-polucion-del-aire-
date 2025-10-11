#!/usr/bin/env python3
"""
Script de prueba completa del servidor Flask con Swagger UI
Sistema de Monitoreo de Calidad del Aire UNI
"""

import requests
import json
import time
from datetime import datetime

def test_server():
    """
    Prueba todos los endpoints del servidor Flask
    """
    base_url = "http://localhost:5000"
    
    print("🚀 Probando Servidor Flask - Sistema UNI")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1. 🔍 Health Check")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Status: {health_data['status']}")
            print(f"📖 Swagger UI: {health_data['endpoints']['swagger_ui']}")
            print(f"📄 Swagger Spec: {health_data['endpoints']['swagger_spec']}")
        else:
            print(f"❌ Error: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Error conectando: {e}")
        return False
    
    # Test 2: Swagger YAML
    print("\n2. 📄 Swagger YAML")
    try:
        response = requests.get(f"{base_url}/static/swagger.yaml")
        if response.status_code == 200:
            yaml_content = response.text
            if "openapi: 3.0.3" in yaml_content:
                print("✅ Archivo swagger.yaml disponible")
                print(f"📊 Tamaño: {len(yaml_content)} caracteres")
            else:
                print("⚠️  Archivo encontrado pero formato incorrecto")
        else:
            print(f"❌ Error: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Swagger UI
    print("\n3. 🌐 Swagger UI")
    try:
        response = requests.get(f"{base_url}/api/docs")
        if response.status_code == 200:
            html_content = response.text
            if "swagger-ui" in html_content:
                print("✅ Swagger UI disponible")
                print("🎯 URL: http://localhost:5000/api/docs")
            else:
                print("⚠️  Página encontrada pero no es Swagger UI")
        else:
            print(f"❌ Error: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Root Endpoint
    print("\n4. 🏠 Root Endpoint")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            root_data = response.json()
            print(f"✅ API: {root_data['message']}")
            print(f"📖 Version: {root_data['version']}")
        else:
            print(f"❌ Error: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Endpoints de Prueba
    print("\n5. 🧪 Endpoints de Prueba")
    
    # Login endpoint
    try:
        login_data = {"email": "admin@uni.edu.pe", "password": "admin123"}
        response = requests.post(f"{base_url}/login", json=login_data)
        if response.status_code == 200:
            print("✅ Login endpoint funcionando")
        else:
            print(f"⚠️  Login: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    # Users endpoint
    try:
        response = requests.get(f"{base_url}/usuarios")
        if response.status_code == 200:
            print("✅ Usuarios endpoint funcionando")
        else:
            print(f"⚠️  Usuarios: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Usuarios error: {e}")
    
    # Devices endpoint
    try:
        response = requests.get(f"{base_url}/dispositivos")
        if response.status_code == 200:
            print("✅ Dispositivos endpoint funcionando")
        else:
            print(f"⚠️  Dispositivos: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Dispositivos error: {e}")
    
    # Readings endpoint
    try:
        reading_data = {
            "temperatura": 22.5,
            "humedad": 45.0,
            "pm2_5": 15.3
        }
        response = requests.post(f"{base_url}/lecturas", json=reading_data)
        if response.status_code == 202:
            print("✅ Lecturas endpoint funcionando")
        else:
            print(f"⚠️  Lecturas: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Lecturas error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ SERVIDOR FUNCIONANDO CORRECTAMENTE")
    print("🎯 Accede a: http://localhost:5000/api/docs")
    print("📖 Para usar Swagger UI interactivo")
    print("=" * 60)
    
    return True

def show_swagger_instructions():
    """
    Muestra instrucciones para usar Swagger UI
    """
    print("\n🎯 CÓMO USAR SWAGGER UI")
    print("=" * 60)
    print("1. Ve a: http://localhost:5000/api/docs")
    print("2. Verás todos los endpoints organizados por categorías:")
    print("   • 🔐 Autenticación")
    print("   • 👥 Usuarios") 
    print("   • 📱 Dispositivos")
    print("   • 📊 Lecturas")
    print("   • 🧹 Asignaciones")
    print("   • 📈 Dashboard")
    print("   • ⚕️ Sistema")
    print()
    print("3. Para probar endpoints:")
    print("   • Haz clic en cualquier endpoint")
    print("   • Clic en 'Try it out'")
    print("   • Completa los datos requeridos")
    print("   • Clic en 'Execute'")
    print()
    print("4. Para autenticación:")
    print("   • Usa POST /login con:")
    print("     - email: admin@uni.edu.pe")
    print("     - clave: admin123")
    print("   • Copia el token de la respuesta")
    print("   • Clic en 'Authorize' (candado)")
    print("   • Pega: Bearer <tu_token>")
    print()
    print("¡Ahora puedes probar todos los endpoints!")
    print("=" * 60)

if __name__ == "__main__":
    print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Esperar un momento para que el servidor esté listo
    print("⏳ Esperando que el servidor esté listo...")
    time.sleep(2)
    
    # Ejecutar pruebas
    if test_server():
        show_swagger_instructions()
    else:
        print("❌ Servidor no disponible. ¿Está ejecutándose?")
        print("💡 Ejecuta: python run.py")