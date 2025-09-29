# Dockerfile
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY src/ ./src/
COPY run.py .
COPY .env.example ./.env

# Crear directorio de logs
RUN mkdir -p logs

# Exponer puerto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]