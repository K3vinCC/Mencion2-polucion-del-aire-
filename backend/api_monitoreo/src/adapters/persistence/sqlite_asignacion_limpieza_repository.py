# src/adapters/persistence/sqlite_asignacion_limpieza_repository.py
import sqlite3
from src.domain.ports.asignacion_limpieza_repository import IAsignacionLimpiezaRepository
from src.domain.entities.asignacion_limpieza import AsignacionLimpieza

class SQLiteAsignacionLimpiezaRepository(IAsignacionLimpiezaRepository):
    """
    Adaptador de persistencia para Asignaciones de Limpieza usando SQLite.
    """

    def __init__(self, db_path):
        self.db_path = db_path

    def _get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def save(self, asignacion):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO asignaciones_limpieza (id_lectura, id_usuario_asignado, descripcion, estado, prioridad, fecha_asignacion)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (asignacion.id_lectura, asignacion.id_usuario_asignado, asignacion.descripcion,
                 asignacion.estado, asignacion.prioridad, asignacion.fecha_asignacion)
            )
            asignacion.id = cursor.lastrowid
            conn.commit()
        return asignacion

    def find_by_id(self, asignacion_id):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM asignaciones_limpieza WHERE id = ?", (asignacion_id,))
            row = cursor.fetchone()
            if row:
                return AsignacionLimpieza(
                    id=row['id'],
                    id_lectura=row['id_lectura'],
                    id_usuario_asignado=row['id_usuario_asignado'],
                    descripcion=row['descripcion'],
                    estado=row['estado'],
                    prioridad=row['prioridad'],
                    fecha_asignacion=row['fecha_asignacion'],
                    fecha_completado=row['fecha_completado']
                )
        return None

    def get_by_usuario(self, id_usuario):
        asignaciones = []
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM asignaciones_limpieza WHERE id_usuario_asignado = ? ORDER BY fecha_asignacion DESC",
                (id_usuario,)
            )
            rows = cursor.fetchall()
            for row in rows:
                asignaciones.append(AsignacionLimpieza(
                    id=row['id'],
                    id_lectura=row['id_lectura'],
                    id_usuario_asignado=row['id_usuario_asignado'],
                    descripcion=row['descripcion'],
                    estado=row['estado'],
                    prioridad=row['prioridad'],
                    fecha_asignacion=row['fecha_asignacion'],
                    fecha_completado=row['fecha_completado']
                ))
        return asignaciones

    def get_pendientes(self):
        asignaciones = []
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM asignaciones_limpieza WHERE estado = 'pendiente' ORDER BY prioridad DESC, fecha_asignacion ASC"
            )
            rows = cursor.fetchall()
            for row in rows:
                asignaciones.append(AsignacionLimpieza(
                    id=row['id'],
                    id_lectura=row['id_lectura'],
                    id_usuario_asignado=row['id_usuario_asignado'],
                    descripcion=row['descripcion'],
                    estado=row['estado'],
                    prioridad=row['prioridad'],
                    fecha_asignacion=row['fecha_asignacion'],
                    fecha_completado=row['fecha_completado']
                ))
        return asignaciones

    def get_by_estado(self, estado):
        asignaciones = []
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM asignaciones_limpieza WHERE estado = ? ORDER BY fecha_asignacion DESC",
                (estado,)
            )
            rows = cursor.fetchall()
            for row in rows:
                asignaciones.append(AsignacionLimpieza(
                    id=row['id'],
                    id_lectura=row['id_lectura'],
                    id_usuario_asignado=row['id_usuario_asignado'],
                    descripcion=row['descripcion'],
                    estado=row['estado'],
                    prioridad=row['prioridad'],
                    fecha_asignacion=row['fecha_asignacion'],
                    fecha_completado=row['fecha_completado']
                ))
        return asignaciones

    def update_estado(self, asignacion_id, estado, fecha_completado=None):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE asignaciones_limpieza SET estado = ?, fecha_completado = ? WHERE id = ?",
                (estado, fecha_completado, asignacion_id)
            )
            conn.commit()