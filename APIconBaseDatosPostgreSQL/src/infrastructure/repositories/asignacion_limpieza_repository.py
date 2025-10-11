# src/infrastructure/repositories/asignacion_limpieza_repository.py
"""
Implementación del repositorio de asignaciones de limpieza usando SQLAlchemy y PostgreSQL.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc, case
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.domain.entities.asignacion_limpieza import AsignacionLimpieza
from src.domain.ports.asignacion_limpieza_repository import IAsignacionLimpiezaRepository
from src.infrastructure.database.models.asignacion_limpieza import AsignacionLimpieza as AsignacionLimpiezaModel
from src.infrastructure.database.database import get_session


class AsignacionLimpiezaRepository(IAsignacionLimpiezaRepository):
    """
    Implementación PostgreSQL del repositorio de asignaciones de limpieza.

    Maneja todas las operaciones de persistencia de asignaciones usando SQLAlchemy.
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

    def _entity_to_model(self, asignacion: AsignacionLimpieza) -> AsignacionLimpiezaModel:
        """Convierte una entidad de dominio a modelo de base de datos."""
        return AsignacionLimpiezaModel(
            id=asignacion.id,
            sala_id=asignacion.sala_id,
            asignado_por_usuario_id=asignacion.asignado_por_usuario_id,
            asignado_a_usuario_id=asignacion.asignado_a_usuario_id,
            estado=asignacion.estado,
            fecha_creacion=asignacion.fecha_creacion,
            fecha_completado=asignacion.fecha_completado
        )

    def _model_to_entity(self, model: AsignacionLimpiezaModel) -> AsignacionLimpieza:
        """Convierte un modelo de base de datos a entidad de dominio."""
        return AsignacionLimpieza(
            id=model.id,
            sala_id=model.sala_id,
            asignado_por_usuario_id=model.asignado_por_usuario_id,
            asignado_a_usuario_id=model.asignado_a_usuario_id,
            estado=model.estado,
            fecha_creacion=model.fecha_creacion,
            fecha_completado=model.fecha_completado
        )

    def save(self, asignacion: AsignacionLimpieza) -> AsignacionLimpieza:
        """
        Guarda una nueva asignación de limpieza.

        Args:
            asignacion: La entidad AsignacionLimpieza a persistir

        Returns:
            AsignacionLimpieza: La entidad con su ID asignado
        """
        session = self._get_session()
        try:
            model = self._entity_to_model(asignacion)
            session.add(model)
            session.flush()  # Para obtener el ID generado

            # Actualizar la entidad con el ID generado
            asignacion.id = model.id
            session.commit()

            return asignacion

        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error al guardar asignación de limpieza: {str(e)}")

    def find_by_id(self, asignacion_id: int) -> Optional[AsignacionLimpieza]:
        """
        Busca una asignación por su ID.

        Args:
            asignacion_id: El ID de la asignación a buscar

        Returns:
            AsignacionLimpieza o None: La entidad si existe, None en caso contrario
        """
        session = self._get_session()
        try:
            model = session.query(AsignacionLimpiezaModel).filter_by(id=asignacion_id).first()
            return self._model_to_entity(model) if model else None
        except SQLAlchemyError:
            return None

    def find_by_sala(self, sala_id: int) -> List[AsignacionLimpieza]:
        """
        Obtiene todas las asignaciones de limpieza para una sala específica.

        Args:
            sala_id: El ID de la sala

        Returns:
            List[AsignacionLimpieza]: Lista de asignaciones para la sala
        """
        session = self._get_session()
        try:
            models = session.query(AsignacionLimpiezaModel)\
                .filter_by(sala_id=sala_id)\
                .order_by(desc(AsignacionLimpiezaModel.fecha_creacion))\
                .all()
            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def find_by_limpiador(self, usuario_id: int) -> List[AsignacionLimpieza]:
        """
        Obtiene todas las asignaciones asignadas a un limpiador específico.

        Args:
            usuario_id: El ID del usuario limpiador

        Returns:
            List[AsignacionLimpieza]: Lista de asignaciones del limpiador
        """
        session = self._get_session()
        try:
            models = session.query(AsignacionLimpiezaModel)\
                .filter_by(asignado_a_usuario_id=usuario_id)\
                .order_by(desc(AsignacionLimpiezaModel.fecha_creacion))\
                .all()
            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def find_by_conserje(self, usuario_id: int) -> List[AsignacionLimpieza]:
        """
        Obtiene todas las asignaciones creadas por un conserje específico.

        Args:
            usuario_id: El ID del usuario conserje

        Returns:
            List[AsignacionLimpieza]: Lista de asignaciones creadas por el conserje
        """
        session = self._get_session()
        try:
            models = session.query(AsignacionLimpiezaModel)\
                .filter_by(asignado_por_usuario_id=usuario_id)\
                .order_by(desc(AsignacionLimpiezaModel.fecha_creacion))\
                .all()
            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def find_pendientes(self) -> List[AsignacionLimpieza]:
        """
        Obtiene todas las asignaciones pendientes.

        Returns:
            List[AsignacionLimpieza]: Lista de asignaciones pendientes
        """
        session = self._get_session()
        try:
            models = session.query(AsignacionLimpiezaModel)\
                .filter_by(estado='pendiente')\
                .order_by(AsignacionLimpiezaModel.fecha_creacion)\
                .all()
            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def find_pendientes_por_edificio(self, edificio_id: int) -> List[AsignacionLimpieza]:
        """
        Obtiene asignaciones pendientes para un edificio específico.

        Args:
            edificio_id: El ID del edificio

        Returns:
            List[AsignacionLimpieza]: Lista de asignaciones pendientes del edificio
        """
        session = self._get_session()
        try:
            # Join con sala para filtrar por edificio
            models = session.query(AsignacionLimpiezaModel)\
                .join(AsignacionLimpiezaModel.sala)\
                .filter(
                    and_(
                        AsignacionLimpiezaModel.estado == 'pendiente',
                        AsignacionLimpiezaModel.sala.edificio_id == edificio_id
                    )
                )\
                .order_by(AsignacionLimpiezaModel.fecha_creacion)\
                .all()

            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def get_estadisticas_edificio(self, edificio_id: int) -> dict:
        """
        Obtiene estadísticas de asignaciones para un edificio.

        Args:
            edificio_id: El ID del edificio

        Returns:
            dict: Estadísticas como total asignaciones, completadas, pendientes,
                  tiempo promedio de completación, etc.
        """
        session = self._get_session()
        try:
            # Estadísticas usando funciones de agregación
            stats = session.query(
                func.count(AsignacionLimpiezaModel.id).label('total'),
                func.sum(
                    case((AsignacionLimpiezaModel.estado == 'completada', 1), else_=0)
                ).label('completadas'),
                func.sum(
                    case((AsignacionLimpiezaModel.estado == 'pendiente', 1), else_=0)
                ).label('pendientes'),
                func.avg(
                    case(
                        (AsignacionLimpiezaModel.fecha_completado.isnot(None),
                         func.extract('epoch', AsignacionLimpiezaModel.fecha_completado - AsignacionLimpiezaModel.fecha_creacion) / 3600),
                        else_=None
                    )
                ).label('tiempo_promedio_horas')
            )\
            .join(AsignacionLimpiezaModel.sala)\
            .filter(AsignacionLimpiezaModel.sala.edificio_id == edificio_id)\
            .first()

            return {
                'total_asignaciones': stats.total or 0,
                'completadas': stats.completadas or 0,
                'pendientes': stats.pendientes or 0,
                'tiempo_promedio_completacion_horas': float(stats.tiempo_promedio_horas) if stats.tiempo_promedio_horas else None
            }

        except SQLAlchemyError:
            return {
                'total_asignaciones': 0,
                'completadas': 0,
                'pendientes': 0,
                'tiempo_promedio_completacion_horas': None
            }

    def update(self, asignacion: AsignacionLimpieza) -> AsignacionLimpieza:
        """
        Actualiza una asignación existente.

        Args:
            asignacion: La entidad AsignacionLimpieza con los datos actualizados

        Returns:
            AsignacionLimpieza: La entidad actualizada

        Raises:
            ValueError: Si la asignación no existe
        """
        session = self._get_session()
        try:
            model = session.query(AsignacionLimpiezaModel).filter_by(id=asignacion.id).first()
            if not model:
                raise ValueError(f"Asignación con ID {asignacion.id} no encontrada")

            # Actualizar campos
            model.sala_id = asignacion.sala_id
            model.asignado_por_usuario_id = asignacion.asignado_por_usuario_id
            model.asignado_a_usuario_id = asignacion.asignado_a_usuario_id
            model.estado = asignacion.estado
            model.fecha_completado = asignacion.fecha_completado

            session.commit()
            return asignacion

        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error al actualizar asignación: {str(e)}")

    def marcar_completada(self, asignacion_id: int) -> bool:
        """
        Marca una asignación como completada.

        Args:
            asignacion_id: El ID de la asignación

        Returns:
            bool: True si se marcó como completada

        Raises:
            ValueError: Si la asignación no existe o ya está completada
        """
        session = self._get_session()
        try:
            model = session.query(AsignacionLimpiezaModel).filter_by(id=asignacion_id).first()
            if not model:
                raise ValueError(f"Asignación con ID {asignacion_id} no encontrada")

            if model.estado == 'completada':
                raise ValueError(f"La asignación {asignacion_id} ya está completada")

            model.estado = 'completada'
            model.fecha_completado = datetime.now()
            session.commit()

            return True

        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error al marcar asignación como completada: {str(e)}")

    def delete(self, asignacion_id: int) -> bool:
        """
        Elimina una asignación por su ID.

        Args:
            asignacion_id: El ID de la asignación a eliminar

        Returns:
            bool: True si se eliminó correctamente, False si no existía
        """
        session = self._get_session()
        try:
            model = session.query(AsignacionLimpiezaModel).filter_by(id=asignacion_id).first()
            if not model:
                return False

            session.delete(model)
            session.commit()
            return True

        except IntegrityError as e:
            session.rollback()
            raise ValueError(f"No se puede eliminar la asignación {asignacion_id}: {str(e)}")
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error al eliminar asignación: {str(e)}")