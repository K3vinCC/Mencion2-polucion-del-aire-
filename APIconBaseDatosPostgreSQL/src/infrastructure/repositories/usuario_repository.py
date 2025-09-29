# src/infrastructure/repositories/usuario_repository.py
"""
Implementación del repositorio de usuarios usando SQLAlchemy y PostgreSQL.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.domain.entities.usuario import Usuario
from src.domain.ports.usuario_repository import IUsuarioRepository
from src.infrastructure.database.models.usuario import Usuario as UsuarioModel
from src.infrastructure.database.database import get_session


class UsuarioRepository(IUsuarioRepository):
    """
    Implementación PostgreSQL del repositorio de usuarios.

    Maneja todas las operaciones de persistencia de usuarios usando SQLAlchemy.
    """

    def __init__(self, session: Optional[Session] = None):
        """
        Inicializa el repositorio.

        Args:
            session: Sesión de SQLAlchemy opcional. Si no se proporciona,
                    se obtendrá automáticamente.
        """
        self._session = session

    def _get_session(self) -> Session:
        """Obtiene la sesión actual o crea una nueva."""
        return self._session or get_session()

    def _entity_to_model(self, usuario: Usuario) -> UsuarioModel:
        """Convierte una entidad de dominio a modelo de base de datos."""
        return UsuarioModel(
            id=usuario.id,
            email=usuario.email,
            clave_hash=usuario.clave_hash,
            nombre_completo=usuario.nombre_completo,
            rol_id=usuario.rol_id,
            universidad_id=usuario.universidad_id,
            campus_id=usuario.campus_id,
            fecha_creacion=usuario.fecha_creacion
        )

    def _model_to_entity(self, model: UsuarioModel) -> Usuario:
        """Convierte un modelo de base de datos a entidad de dominio."""
        return Usuario(
            id=model.id,
            email=model.email,
            clave_hash=model.clave_hash,
            nombre_completo=model.nombre_completo,
            rol_id=model.rol_id,
            universidad_id=model.universidad_id,
            campus_id=model.campus_id,
            fecha_creacion=model.fecha_creacion
        )

    def save(self, usuario: Usuario) -> Usuario:
        """
        Guarda un nuevo usuario en la base de datos.

        Args:
            usuario: La entidad Usuario a persistir

        Returns:
            Usuario: La entidad con su ID asignado

        Raises:
            ValueError: Si ya existe un usuario con el mismo email
        """
        session = self._get_session()
        try:
            # Verificar si ya existe un usuario con el mismo email
            existing = session.query(UsuarioModel).filter_by(email=usuario.email).first()
            if existing:
                raise ValueError(f"Ya existe un usuario con el email: {usuario.email}")

            # Crear el modelo y guardarlo
            model = self._entity_to_model(usuario)
            session.add(model)
            session.flush()  # Para obtener el ID generado

            # Actualizar la entidad con el ID generado
            usuario.id = model.id
            session.commit()

            return usuario

        except IntegrityError as e:
            session.rollback()
            if "unique constraint" in str(e).lower() and "email" in str(e).lower():
                raise ValueError(f"Ya existe un usuario con el email: {usuario.email}")
            raise ValueError(f"Error de integridad al guardar usuario: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error al guardar usuario: {str(e)}")

    def find_by_id(self, usuario_id: int) -> Optional[Usuario]:
        """
        Busca un usuario por su ID.

        Args:
            usuario_id: El ID del usuario a buscar

        Returns:
            Usuario o None: La entidad Usuario si existe, None en caso contrario
        """
        session = self._get_session()
        try:
            model = session.query(UsuarioModel).filter_by(id=usuario_id).first()
            return self._model_to_entity(model) if model else None
        except SQLAlchemyError:
            return None

    def find_by_email(self, email: str) -> Optional[Usuario]:
        """
        Busca un usuario por su email.

        Args:
            email: El email del usuario a buscar

        Returns:
            Usuario o None: La entidad Usuario si existe, None en caso contrario
        """
        session = self._get_session()
        try:
            model = session.query(UsuarioModel).filter_by(email=email).first()
            return self._model_to_entity(model) if model else None
        except SQLAlchemyError:
            return None

    def find_by_universidad(self, universidad_id: int) -> List[Usuario]:
        """
        Obtiene todos los usuarios de una universidad específica.

        Args:
            universidad_id: El ID de la universidad

        Returns:
            List[Usuario]: Lista de usuarios de la universidad
        """
        session = self._get_session()
        try:
            models = session.query(UsuarioModel).filter_by(universidad_id=universidad_id).all()
            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def find_by_rol(self, rol_id: int) -> List[Usuario]:
        """
        Obtiene todos los usuarios con un rol específico.

        Args:
            rol_id: El ID del rol

        Returns:
            List[Usuario]: Lista de usuarios con ese rol
        """
        session = self._get_session()
        try:
            models = session.query(UsuarioModel).filter_by(rol_id=rol_id).all()
            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def get_all(self) -> List[Usuario]:
        """
        Obtiene todos los usuarios del sistema.

        Returns:
            List[Usuario]: Lista completa de usuarios
        """
        session = self._get_session()
        try:
            models = session.query(UsuarioModel).all()
            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def update(self, usuario: Usuario) -> Usuario:
        """
        Actualiza un usuario existente.

        Args:
            usuario: La entidad Usuario con los datos actualizados

        Returns:
            Usuario: La entidad actualizada

        Raises:
            ValueError: Si el usuario no existe
        """
        session = self._get_session()
        try:
            model = session.query(UsuarioModel).filter_by(id=usuario.id).first()
            if not model:
                raise ValueError(f"Usuario con ID {usuario.id} no encontrado")

            # Actualizar campos
            model.email = usuario.email
            model.clave_hash = usuario.clave_hash
            model.nombre_completo = usuario.nombre_completo
            model.rol_id = usuario.rol_id
            model.universidad_id = usuario.universidad_id
            model.campus_id = usuario.campus_id

            session.commit()
            return usuario

        except IntegrityError as e:
            session.rollback()
            if "unique constraint" in str(e).lower() and "email" in str(e).lower():
                raise ValueError(f"Ya existe otro usuario con el email: {usuario.email}")
            raise ValueError(f"Error de integridad al actualizar usuario: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error al actualizar usuario: {str(e)}")

    def delete(self, usuario_id: int) -> bool:
        """
        Elimina un usuario por su ID.

        Args:
            usuario_id: El ID del usuario a eliminar

        Returns:
            bool: True si se eliminó correctamente, False si no existía

        Raises:
            ValueError: Si no se puede eliminar (restricciones de integridad)
        """
        session = self._get_session()
        try:
            model = session.query(UsuarioModel).filter_by(id=usuario_id).first()
            if not model:
                return False

            session.delete(model)
            session.commit()
            return True

        except IntegrityError as e:
            session.rollback()
            raise ValueError(f"No se puede eliminar el usuario {usuario_id}: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error al eliminar usuario: {str(e)}")