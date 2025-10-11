# src/infrastructure/repositories/dispositivo_repository.py
"""
Implementación del repositorio de dispositivos usando SQLAlchemy y PostgreSQL.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.domain.entities.dispositivo import Dispositivo
from src.domain.ports.dispositivo_repository import IDispositivoRepository
from src.infrastructure.database.models.dispositivo import Dispositivo as DispositivoModel
from src.infrastructure.database.database import get_session


class DispositivoRepository(IDispositivoRepository):
    """
    Implementación PostgreSQL del repositorio de dispositivos.

    Maneja todas las operaciones de persistencia de dispositivos usando SQLAlchemy.
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

    def _entity_to_model(self, dispositivo: Dispositivo) -> DispositivoModel:
        """Convierte una entidad de dominio a modelo de base de datos."""
        return DispositivoModel(
            id=dispositivo.id,
            sala_id=dispositivo.sala_id,
            modelo_id=dispositivo.modelo_id,
            mac_address=dispositivo.mac_address,
            api_token_hash=dispositivo.api_token_hash,
            fecha_instalacion=dispositivo.fecha_instalacion,
            ultimo_mantenimiento=dispositivo.ultimo_mantenimiento,
            estado=dispositivo.estado,
            ultima_vez_visto=dispositivo.ultima_vez_visto
        )

    def _model_to_entity(self, model: DispositivoModel) -> Dispositivo:
        """Convierte un modelo de base de datos a entidad de dominio."""
        return Dispositivo(
            id=model.id,
            sala_id=model.sala_id,
            modelo_id=model.modelo_id,
            mac_address=model.mac_address,
            api_token_hash=model.api_token_hash,
            fecha_instalacion=model.fecha_instalacion,
            ultimo_mantenimiento=model.ultimo_mantenimiento,
            estado=model.estado,
            ultima_vez_visto=model.ultima_vez_visto
        )

    def save(self, dispositivo: Dispositivo) -> Dispositivo:
        """
        Guarda un nuevo dispositivo en la base de datos.

        Args:
            dispositivo: La entidad Dispositivo a persistir

        Returns:
            Dispositivo: La entidad con su ID asignado

        Raises:
            ValueError: Si ya existe un dispositivo con la misma MAC
        """
        session = self._get_session()
        try:
            # Verificar si ya existe un dispositivo con la misma MAC
            existing = session.query(DispositivoModel).filter_by(mac_address=dispositivo.mac_address).first()
            if existing:
                raise ValueError(f"Ya existe un dispositivo con la MAC: {dispositivo.mac_address}")

            # Crear el modelo y guardarlo
            model = self._entity_to_model(dispositivo)
            session.add(model)
            session.flush()  # Para obtener el ID generado

            # Actualizar la entidad con el ID generado
            dispositivo.id = model.id
            session.commit()

            return dispositivo

        except IntegrityError as e:
            session.rollback()
            if "unique constraint" in str(e).lower() and "mac_address" in str(e).lower():
                raise ValueError(f"Ya existe un dispositivo con la MAC: {dispositivo.mac_address}")
            raise ValueError(f"Error de integridad al guardar dispositivo: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error al guardar dispositivo: {str(e)}")

    def find_by_id(self, dispositivo_id: int) -> Optional[Dispositivo]:
        """
        Busca un dispositivo por su ID.

        Args:
            dispositivo_id: El ID del dispositivo a buscar

        Returns:
            Dispositivo o None: La entidad Dispositivo si existe, None en caso contrario
        """
        session = self._get_session()
        try:
            model = session.query(DispositivoModel).filter_by(id=dispositivo_id).first()
            return self._model_to_entity(model) if model else None
        except SQLAlchemyError:
            return None

    def find_by_mac(self, mac_address: str) -> Optional[Dispositivo]:
        """
        Busca un dispositivo por su dirección MAC.

        Args:
            mac_address: La dirección MAC del dispositivo

        Returns:
            Dispositivo o None: La entidad Dispositivo si existe, None en caso contrario
        """
        session = self._get_session()
        try:
            model = session.query(DispositivoModel).filter_by(mac_address=mac_address).first()
            return self._model_to_entity(model) if model else None
        except SQLAlchemyError:
            return None

    def find_by_sala(self, sala_id: int) -> List[Dispositivo]:
        """
        Obtiene todos los dispositivos instalados en una sala específica.

        Args:
            sala_id: El ID de la sala

        Returns:
            List[Dispositivo]: Lista de dispositivos en la sala
        """
        session = self._get_session()
        try:
            models = session.query(DispositivoModel).filter_by(sala_id=sala_id).all()
            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def find_by_universidad(self, universidad_id: int) -> List[Dispositivo]:
        """
        Obtiene todos los dispositivos de una universidad específica.

        Args:
            universidad_id: El ID de la universidad

        Returns:
            List[Dispositivo]: Lista de dispositivos de la universidad
        """
        session = self._get_session()
        try:
            # Join con sala -> edificio -> campus -> universidad
            models = session.query(DispositivoModel)\
                .join(DispositivoModel.sala)\
                .join(DispositivoModel.sala.edificio)\
                .join(DispositivoModel.sala.edificio.campus)\
                .filter(DispositivoModel.sala.edificio.campus.universidad_id == universidad_id)\
                .all()
            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def get_all(self) -> List[Dispositivo]:
        """
        Obtiene todos los dispositivos del sistema.

        Returns:
            List[Dispositivo]: Lista completa de dispositivos
        """
        session = self._get_session()
        try:
            models = session.query(DispositivoModel).all()
            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def get_conectados(self) -> List[Dispositivo]:
        """
        Obtiene todos los dispositivos que están conectados.

        Returns:
            List[Dispositivo]: Lista de dispositivos conectados
        """
        session = self._get_session()
        try:
            models = session.query(DispositivoModel).filter_by(estado='conectado').all()
            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def get_desconectados(self) -> List[Dispositivo]:
        """
        Obtiene todos los dispositivos que están desconectados.

        Returns:
            List[Dispositivo]: Lista de dispositivos desconectados
        """
        session = self._get_session()
        try:
            models = session.query(DispositivoModel).filter_by(estado='desconectado').all()
            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def update(self, dispositivo: Dispositivo) -> Dispositivo:
        """
        Actualiza un dispositivo existente.

        Args:
            dispositivo: La entidad Dispositivo con los datos actualizados

        Returns:
            Dispositivo: La entidad actualizada

        Raises:
            ValueError: Si el dispositivo no existe
        """
        session = self._get_session()
        try:
            model = session.query(DispositivoModel).filter_by(id=dispositivo.id).first()
            if not model:
                raise ValueError(f"Dispositivo con ID {dispositivo.id} no encontrado")

            # Actualizar campos
            model.sala_id = dispositivo.sala_id
            model.modelo_id = dispositivo.modelo_id
            model.mac_address = dispositivo.mac_address
            model.api_token_hash = dispositivo.api_token_hash
            model.fecha_instalacion = dispositivo.fecha_instalacion
            model.ultimo_mantenimiento = dispositivo.ultimo_mantenimiento
            model.estado = dispositivo.estado
            model.ultima_vez_visto = dispositivo.ultima_vez_visto

            session.commit()
            return dispositivo

        except IntegrityError as e:
            session.rollback()
            if "unique constraint" in str(e).lower() and "mac_address" in str(e).lower():
                raise ValueError(f"Ya existe otro dispositivo con la MAC: {dispositivo.mac_address}")
            raise ValueError(f"Error de integridad al actualizar dispositivo: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error al actualizar dispositivo: {str(e)}")

    def update_estado(self, dispositivo_id: int, estado: str) -> bool:
        """
        Actualiza solo el estado de un dispositivo.

        Args:
            dispositivo_id: El ID del dispositivo
            estado: El nuevo estado ('conectado' o 'desconectado')

        Returns:
            bool: True si se actualizó correctamente

        Raises:
            ValueError: Si el dispositivo no existe o el estado es inválido
        """
        if estado not in ['conectado', 'desconectado']:
            raise ValueError(f"Estado inválido: {estado}. Debe ser 'conectado' o 'desconectado'")

        session = self._get_session()
        try:
            model = session.query(DispositivoModel).filter_by(id=dispositivo_id).first()
            if not model:
                raise ValueError(f"Dispositivo con ID {dispositivo_id} no encontrado")

            model.estado = estado
            session.commit()
            return True

        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error al actualizar estado del dispositivo: {str(e)}")

    def delete(self, dispositivo_id: int) -> bool:
        """
        Elimina un dispositivo por su ID.

        Args:
            dispositivo_id: El ID del dispositivo a eliminar

        Returns:
            bool: True si se eliminó correctamente, False si no existía

        Raises:
            ValueError: Si no se puede eliminar (restricciones de integridad)
        """
        session = self._get_session()
        try:
            model = session.query(DispositivoModel).filter_by(id=dispositivo_id).first()
            if not model:
                return False

            session.delete(model)
            session.commit()
            return True

        except IntegrityError as e:
            session.rollback()
            raise ValueError(f"No se puede eliminar el dispositivo {dispositivo_id}: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error al eliminar dispositivo: {str(e)}")