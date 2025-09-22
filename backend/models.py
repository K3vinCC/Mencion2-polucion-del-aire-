from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# --------------------- Modelos ---------------------
class Universidad(db.Model):
    __tablename__ = 'universidades'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique=True, nullable=False)
    pais = db.Column(db.String)

class Campus(db.Model):
    __tablename__ = 'campus'
    id = db.Column(db.Integer, primary_key=True)
    universidad_id = db.Column(db.Integer, db.ForeignKey('universidades.id'), nullable=False)
    nombre = db.Column(db.String, nullable=False)
    direccion = db.Column(db.String)

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique=True, nullable=False)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    clave_hash = db.Column(db.String, nullable=False)
    nombre_completo = db.Column(db.String, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    universidad_id = db.Column(db.Integer, db.ForeignKey('universidades.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        self.clave_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.clave_hash, password)

class Edificio(db.Model):
    __tablename__ = 'edificios'
    id = db.Column(db.Integer, primary_key=True)
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'), nullable=False)
    nombre = db.Column(db.String, nullable=False)
    __table_args__ = (db.UniqueConstraint('campus_id', 'nombre', name='uq_campus_edificio'),)

class Sala(db.Model):
    __tablename__ = 'salas'
    id = db.Column(db.Integer, primary_key=True)
    edificio_id = db.Column(db.Integer, db.ForeignKey('edificios.id'), nullable=False)
    piso = db.Column(db.Integer)
    nombre_o_numero = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String)
    __table_args__ = (db.UniqueConstraint('edificio_id', 'nombre_o_numero', name='uq_edificio_sala'),)

class ModeloDispositivo(db.Model):
    __tablename__ = 'modelos_dispositivos'
    id = db.Column(db.Integer, primary_key=True)
    nombre_modelo = db.Column(db.String, nullable=False, unique=True)
    fabricante = db.Column(db.String)
    especificaciones = db.Column(db.String)

class Dispositivo(db.Model):
    __tablename__ = 'dispositivos'
    id = db.Column(db.Integer, primary_key=True)
    sala_id = db.Column(db.Integer, db.ForeignKey('salas.id'), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelos_dispositivos.id'), nullable=False)
    id_hardware = db.Column(db.String, nullable=False, unique=True)
    api_token_hash = db.Column(db.String, nullable=False)
    fecha_instalacion = db.Column(db.Date)
    ultimo_mantenimiento = db.Column(db.Date)
    estado = db.Column(db.String, default='desconectado', nullable=False)
    ultima_vez_visto = db.Column(db.DateTime)

    def set_token(self, token: str):
        self.api_token_hash = generate_password_hash(token)

    def check_token(self, token: str) -> bool:
        return check_password_hash(self.api_token_hash, token)
