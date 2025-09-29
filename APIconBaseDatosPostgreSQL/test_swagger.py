#!/usr/bin/env python3
"""
Script para probar el endpoint de swagger.yaml
"""

import time
import requests
import subprocess
import sys
import os

def test_swagger_endpoint():
    """Probar el endpoint de swagger.yaml"""
    try:
        # Esperar a que el servidor inicie
        time.sleep(2)

        # Hacer la petición
        response = requests.get('http://localhost:5000/static/swagger.yaml', timeout=10)

        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")

        if response.status_code == 200:
            print("✅ Endpoint funcionando correctamente")
            print("Primeras líneas del contenido:")
            lines = response.text.split('\n')[:10]
            for i, line in enumerate(lines, 1):
                print("2")
        else:
            print("❌ Error en el endpoint")
            print(f"Respuesta: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == '__main__':
    test_swagger_endpoint()