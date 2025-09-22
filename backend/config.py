import os

DB_NAME = "nombre_bd"
DB_USER = "usuario"
DB_PASSWORD = "contraseña"
DB_HOST = "dirección_host"
DB_PORT = "puerto"

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
