# Makefile para el proyecto API de Calidad del Aire

.PHONY: help install run test clean docker-build docker-run docker-stop init-db format lint

# Variables
PYTHON := python
PIP := pip
DOCKER_COMPOSE := docker-compose

# Ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  install      - Instalar dependencias"
	@echo "  run          - Ejecutar la aplicación en modo desarrollo"
	@echo "  test         - Ejecutar tests"
	@echo "  clean        - Limpiar archivos temporales"
	@echo "  docker-build - Construir imagen Docker"
	@echo "  docker-run   - Ejecutar con Docker Compose"
	@echo "  docker-stop  - Detener contenedores Docker"
	@echo "  init-db      - Inicializar base de datos con datos de prueba"
	@echo "  format       - Formatear código con black e isort"
	@echo "  lint         - Verificar código con flake8"

# Instalar dependencias
install:
	@echo "Instalando dependencias..."
	$(PIP) install -r requirements.txt

# Ejecutar aplicación
run:
	@echo "Ejecutando aplicación..."
	$(PYTHON) run.py

# Ejecutar tests
test:
	@echo "Ejecutando tests..."
	pytest --cov=src --cov-report=html --cov-report=term

# Limpiar archivos temporales
clean:
	@echo "Limpiando archivos temporales..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	rm -rf logs/*.log

# Docker
docker-build:
	@echo "Construyendo imagen Docker..."
	$(DOCKER_COMPOSE) build

docker-run:
	@echo "Ejecutando con Docker Compose..."
	$(DOCKER_COMPOSE) up -d

docker-stop:
	@echo "Deteniendo contenedores Docker..."
	$(DOCKER_COMPOSE) down

docker-logs:
	@echo "Mostrando logs de Docker..."
	$(DOCKER_COMPOSE) logs -f app

# Base de datos
init-db:
	@echo "Inicializando base de datos..."
	$(PYTHON) -m src.infrastructure.database.init_db

reset-db:
	@echo "Reiniciando base de datos..."
	$(PYTHON) -c "from src.infrastructure.database.database import reset_db; reset_db()"

# Formateo y linting
format:
	@echo "Formateando código..."
	black src/
	isort src/

lint:
	@echo "Verificando código..."
	flake8 src/

# Desarrollo completo
dev-setup: install init-db
	@echo "Configuración de desarrollo completada"

dev-run: run

# Producción
prod-build: clean format lint test docker-build
	@echo "Build de producción completado"