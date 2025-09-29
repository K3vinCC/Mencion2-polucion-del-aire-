# src/adapters/persistence/sqlite_lectura_calidad_aire_repository.py
import sqlite3
from datetime import datetime, timedelta
from src.domain.ports.lectura_calidad_aire_repository import ILecturaCalidadAireRepository
from src.domain.entities.lectura_calidad_aire import LecturaCalidadAire

class SQLiteLecturaCalidadAireRepository(ILecturaCalidadAireRepository):
    """
    Adaptador de persistencia para Lecturas de Calidad del Aire usando SQLite.
    """

    def __init__(self, db_path):
        self.db_path = db_path

    def _get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def save(self, lectura):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO lecturas_calidad_aire (id_dispositivo, pm25, pm10, co2, temperatura, humedad, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (lectura.id_dispositivo, lectura.pm25, lectura.pm10, lectura.co2,
                 lectura.temperatura, lectura.humedad, lectura.timestamp)
            )
            lectura.id = cursor.lastrowid
            conn.commit()
        return lectura

    def find_by_id(self, lectura_id):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lecturas_calidad_aire WHERE id = ?", (lectura_id,))
            row = cursor.fetchone()
            if row:
                return LecturaCalidadAire(
                    id=row['id'],
                    id_dispositivo=row['id_dispositivo'],
                    pm25=row['pm25'],
                    pm10=row['pm10'],
                    co2=row['co2'],
                    temperatura=row['temperatura'],
                    humedad=row['humedad'],
                    timestamp=row['timestamp']
                )
        return None

    def get_by_dispositivo(self, id_dispositivo, limit=100):
        lecturas = []
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM lecturas_calidad_aire WHERE id_dispositivo = ? ORDER BY timestamp DESC LIMIT ?",
                (id_dispositivo, limit)
            )
            rows = cursor.fetchall()
            for row in rows:
                lecturas.append(LecturaCalidadAire(
                    id=row['id'],
                    id_dispositivo=row['id_dispositivo'],
                    pm25=row['pm25'],
                    pm10=row['pm10'],
                    co2=row['co2'],
                    temperatura=row['temperatura'],
                    humedad=row['humedad'],
                    timestamp=row['timestamp']
                ))
        return lecturas

    def get_by_edificio(self, id_edificio, limit=100):
        lecturas = []
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT l.* FROM lecturas_calidad_aire l
                JOIN dispositivos d ON l.id_dispositivo = d.id
                WHERE d.id_edificio = ?
                ORDER BY l.timestamp DESC LIMIT ?
                """,
                (id_edificio, limit)
            )
            rows = cursor.fetchall()
            for row in rows:
                lecturas.append(LecturaCalidadAire(
                    id=row['id'],
                    id_dispositivo=row['id_dispositivo'],
                    pm25=row['pm25'],
                    pm10=row['pm10'],
                    co2=row['co2'],
                    temperatura=row['temperatura'],
                    humedad=row['humedad'],
                    timestamp=row['timestamp']
                ))
        return lecturas

    def get_lecturas_recientes(self, horas=24):
        lecturas = []
        tiempo_limite = (datetime.utcnow() - timedelta(hours=horas)).isoformat()
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM lecturas_calidad_aire WHERE timestamp >= ? ORDER BY timestamp DESC",
                (tiempo_limite,)
            )
            rows = cursor.fetchall()
            for row in rows:
                lecturas.append(LecturaCalidadAire(
                    id=row['id'],
                    id_dispositivo=row['id_dispositivo'],
                    pm25=row['pm25'],
                    pm10=row['pm10'],
                    co2=row['co2'],
                    temperatura=row['temperatura'],
                    humedad=row['humedad'],
                    timestamp=row['timestamp']
                ))
        return lecturas

    def get_promedio_calidad(self, id_edificio, horas=24):
        tiempo_limite = (datetime.utcnow() - timedelta(hours=horas)).isoformat()
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT AVG(pm25) as avg_pm25, AVG(pm10) as avg_pm10, AVG(co2) as avg_co2,
                       AVG(temperatura) as avg_temp, AVG(humedad) as avg_hum
                FROM lecturas_calidad_aire l
                JOIN dispositivos d ON l.id_dispositivo = d.id
                WHERE d.id_edificio = ? AND l.timestamp >= ?
                """,
                (id_edificio, tiempo_limite)
            )
            row = cursor.fetchone()
            if row and any(row):
                return {
                    'pm25': row['avg_pm25'],
                    'pm10': row['avg_pm10'],
                    'co2': row['avg_co2'],
                    'temperatura': row['avg_temp'],
                    'humedad': row['avg_hum']
                }
        return None