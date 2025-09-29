#!/usr/bin/env python3
"""
Script de prueba para login API
"""

import requests
import json

def test_login():
    """Probar el endpoint de login"""
    
    url = "http://localhost:5000/api/auth/login"
    
    # Datos de login
    login_data = {
        "email": "admin@uni.edu.pe",
        "password": "admin123"
    }
    
    try:
        print("🔐 Probando login...")
        print(f"URL: {url}")
        print(f"Datos: {login_data}")
        
        response = requests.post(url, json=login_data)
        
        print(f"\n📊 Respuesta:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ LOGIN EXITOSO!")
            print(f"Token: {data.get('token', 'No token')}")
            print(f"Usuario: {data.get('user', {})}")
            
            # Guardar token para usar en otras pruebas
            token = data.get('token')
            if token:
                print(f"\n🔑 Token JWT:")
                print(f"Bearer {token}")
                
                # Probar un endpoint protegido
                headers = {"Authorization": f"Bearer {token}"}
                users_response = requests.get("http://localhost:5000/api/users", headers=headers)
                print(f"\n👥 Prueba endpoint usuarios:")
                print(f"Status: {users_response.status_code}")
                print(f"Respuesta: {users_response.text}")
                
        else:
            print(f"\n❌ ERROR EN LOGIN:")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. ¿Está ejecutándose en localhost:5000?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login()