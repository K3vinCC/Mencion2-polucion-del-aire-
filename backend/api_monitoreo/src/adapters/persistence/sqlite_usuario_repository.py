# src/adapters/persistence/sqlite_usuario_repository.py
import sqlite3
from src.domain.ports.usuario_repository import IUsuarioRepository
from src.domain.entities.usuario import Usuario

class SQLiteUsuarioRepository(IUsuarioRepository):
    """
    Adaptador de persistencia que implementa la interfaz IUsuarioRepository
    utilizando una base de datos SQLite.
    
    Este es un "Adaptador de Salida" en la Arquitectura Hexagonal. Su responsabilidad
    es conectar el núcleo de la aplicación (el dominio) con un sistema externo,
    en este caso, una base de datos SQLite.
    """

    def __init__(self, db_path):
        """
        Constructor del repositorio.
        
        Args:
            db_path (str): La ruta al archivo de la base de datos SQLite.
        """
        self.db_path = db_path

    def _get_db_connection(self):
        """Crea y devuelve una nueva conexión a la base de datos."""
        conn = sqlite3.connect(self.db_path)
        # Permite acceder a las filas por nombre de columna
        conn.row_factory = sqlite3.Row
        return conn

    def save(self, usuario):
        """
        Guarda un nuevo usuario en la base de datos SQLite.
        
        Args:
            usuario (Usuario): La entidad de dominio Usuario a persistir.
            
        Returns:
            Usuario: La entidad Usuario con su ID actualizado después de la inserción.
        """
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO usuarios (nombre, correo, clave_hash, rol, numero_contacto, url_imagen_perfil, id_edificio_asignado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (usuario.nombre, usuario.correo, usuario.clave_hash, usuario.rol, usuario.numero_contacto, usuario.url_imagen_perfil, usuario.id_edificio_asignado)
            )
            usuario.id = cursor.lastrowid
            conn.commit()
        return usuario

    def find_by_email(self, correo):
        """
        Busca un usuario por su correo electrónico.
        
        Args:
            correo (str): El correo del usuario a buscar.
            
        Returns:
            Usuario or None: Una entidad Usuario si se encuentra, de lo contrario None.
        """
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
            row = cursor.fetchone()

            if row:
                # Mapea la fila de la base de datos de vuelta a una entidad de dominio
                return Usuario(
                    id=row['id'],
                    nombre=row['nombre'],
                    correo=row['correo'],
                    clave_hash=row['clave_hash'],
                    rol=row['rol'],
                    numero_contacto=row['numero_contacto'],
                    url_imagen_perfil=row['url_imagen_perfil'],
                    id_edificio_asignado=row['id_edificio_asignado'],
                    fecha_creacion=row['fecha_creacion']
                )
        return None

    def find_by_id(self, usuario_id):
        """
        Busca un usuario por su ID.
        
        Args:
            usuario_id (int): El ID del usuario a buscar.
            
        Returns:
            Usuario or None: Una entidad Usuario si se encuentra, de lo contrario None.
        """
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
            row = cursor.fetchone()
            if row:
                return Usuario(
                    id=row['id'],
                    nombre=row['nombre'],
                    correo=row['correo'],
                    clave_hash=row['clave_hash'],
                    rol=row['rol'],
                    numero_contacto=row['numero_contacto'],
                    url_imagen_perfil=row['url_imagen_perfil'],
                    id_edificio_asignado=row['id_edificio_asignado'],
                    fecha_creacion=row['fecha_creacion']
                )
        return None
    
    def get_all(self):
        """
        Devuelve una lista de todos los usuarios.
        
        Returns:
            list[Usuario]: Una lista de entidades Usuario.
        """
        usuarios = []
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            rows = cursor.fetchall()

            for row in rows:
                usuarios.append(
                     Usuario(
                        id=row['id'],
                        nombre=row['nombre'],
                        correo=row['correo'],
                        clave_hash=row['clave_hash'],
                        rol=row['rol'],
                        numero_contacto=row['numero_contacto'],
                        url_imagen_perfil=row['url_imagen_perfil'],
                        id_edificio_asignado=row['id_edificio_asignado'],
                        fecha_creacion=row['fecha_creacion']
                    )
                )
        return usuarios