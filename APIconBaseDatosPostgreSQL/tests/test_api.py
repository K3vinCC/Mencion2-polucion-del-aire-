# tests/test_api.py
"""
Tests básicos para verificar el funcionamiento de la API.
"""

import pytest
import json
from src.main import create_app
from src.infrastructure.database.connection import db


@pytest.fixture
def client():
    """Cliente de prueba para la aplicación Flask."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_health_check(client):
    """Test del endpoint de health check."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'service' in data


def test_root_endpoint(client):
    """Test del endpoint raíz."""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'endpoints' in data


def test_404_error(client):
    """Test de error 404 para rutas inexistentes."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data


def test_method_not_allowed(client):
    """Test de error 405 para métodos no permitidos."""
    response = client.post('/health')
    assert response.status_code == 405
    data = json.loads(response.data)
    assert 'error' in data