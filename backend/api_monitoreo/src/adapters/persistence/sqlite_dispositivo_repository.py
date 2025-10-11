# src/adapters/persistence/sqlite_dispositivo_repository.py
import sqlite3
from src.domain.ports.dispositivo_repository import IDispositivoRepository
from src.domain.entities.dispositivo import Dispositivo

class SQLiteDispositivoRepository(IDispositivoRepository):
    """
    Adaptador de persistencia para Dispositivos usando SQLite.
    """

    def __init__(self, db_path):
        self.db_path = db_path

    def _get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def save(self, dispositivo):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO dispositivos (nombre, ubicacion, token_acceso, id_edificio, estado, fecha_instalacion)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (dispositivo.nombre, dispositivo.ubicacion, dispositivo.token_acceso,
                 dispositivo.id_edificio, dispositivo.estado, dispositivo.fecha_instalacion)
            )
            dispositivo.id = cursor.lastrowid
            conn.commit()
        return dispositivo

    def find_by_id(self, dispositivo_id):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dispositivos WHERE id = ?", (dispositivo_id,))
            row = cursor.fetchone()
            if row:
                return Dispositivo(
                    id=row['id'],
                    nombre=row['nombre'],
                    ubicacion=row['ubicacion'],
                    token_acceso=row['token_acceso'],
                    id_edificio=row['id_edificio'],
                    estado=row['estado'],
                    fecha_instalacion=row['fecha_instalacion'],
                    ultima_lectura=row['ultima_lectura']
                )
        return None

    def find_by_token(self, token):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dispositivos WHERE token_acceso = ?", (token,))
            row = cursor.fetchone()
            if row:
                return Dispositivo(
                    id=row['id'],
                    nombre=row['nombre'],
                    ubicacion=row['ubicacion'],
                    token_acceso=row['token_acceso'],
                    id_edificio=row['id_edificio'],
                    estado=row['estado'],
                    fecha_instalacion=row['fecha_instalacion'],
                    ultima_lectura=row['ultima_lectura']
                )
        return None

    def get_all(self):
        dispositivos = []
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dispositivos")
            rows = cursor.fetchall()
            for row in rows:
                dispositivos.append(Dispositivo(
                    id=row['id'],
                    nombre=row['nombre'],
                    ubicacion=row['ubicacion'],
                    token_acceso=row['token_acceso'],
                    id_edificio=row['id_edificio'],
                    estado=row['estado'],
                    fecha_instalacion=row['fecha_instalacion'],
                    ultima_lectura=row['ultima_lectura']
                ))
        return dispositivos

    def get_by_edificio(self, id_edificio):
        dispositivos = []
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dispositivos WHERE id_edificio = ?", (id_edificio,))
            rows = cursor.fetchall()
            for row in rows:
                dispositivos.append(Dispositivo(
                    id=row['id'],
                    nombre=row['nombre'],
                    ubicacion=row['ubicacion'],
                    token_acceso=row['token_acceso'],
                    id_edificio=row['id_edificio'],
                    estado=row['estado'],
                    fecha_instalacion=row['fecha_instalacion'],
                    ultima_lectura=row['ultima_lectura']
                ))
        return dispositivos

    def update_ultima_lectura(self, dispositivo_id, timestamp):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE dispositivos SET ultima_lectura = ? WHERE id = ?",
                (timestamp, dispositivo_id)
            )
            conn.commit()