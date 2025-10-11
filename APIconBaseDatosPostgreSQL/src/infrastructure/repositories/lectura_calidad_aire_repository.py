# src/infrastructure/repositories/lectura_calidad_aire_repository.py
"""
Implementación del repositorio de lecturas de calidad del aire usando SQLAlchemy y PostgreSQL.
"""

from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc
from sqlalchemy.exc import SQLAlchemyError

from src.domain.entities.lectura_calidad_aire import LecturaCalidadAire
from src.domain.ports.lectura_calidad_aire_repository import ILecturaCalidadAireRepository
from src.infrastructure.database.models.lectura_calidad_aire import LecturaCalidadAire as LecturaCalidadAireModel
from src.infrastructure.database.database import get_session


class LecturaCalidadAireRepository(ILecturaCalidadAireRepository):
    """
    Implementación PostgreSQL del repositorio de lecturas de calidad del aire.

    Maneja todas las operaciones de persistencia de lecturas usando SQLAlchemy.
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

    def _entity_to_model(self, lectura: LecturaCalidadAire) -> LecturaCalidadAireModel:
        """Convierte una entidad de dominio a modelo de base de datos."""
        return LecturaCalidadAireModel(
            id=lectura.id,
            dispositivo_id=lectura.dispositivo_id,
            valor_pm1=lectura.valor_pm1,
            valor_pm2_5=lectura.valor_pm2_5,
            valor_pm10=lectura.valor_pm10,
            etiqueta=lectura.etiqueta,
            fecha_lectura=lectura.fecha_lectura
        )

    def _model_to_entity(self, model: LecturaCalidadAireModel) -> LecturaCalidadAire:
        """Convierte un modelo de base de datos a entidad de dominio."""
        return LecturaCalidadAire(
            id=model.id,
            dispositivo_id=model.dispositivo_id,
            valor_pm1=model.valor_pm1,
            valor_pm2_5=model.valor_pm2_5,
            valor_pm10=model.valor_pm10,
            etiqueta=model.etiqueta,
            fecha_lectura=model.fecha_lectura
        )

    def save(self, lectura: LecturaCalidadAire) -> LecturaCalidadAire:
        """
        Guarda una nueva lectura de calidad del aire.

        Args:
            lectura: La entidad LecturaCalidadAire a persistir

        Returns:
            LecturaCalidadAire: La entidad con su ID asignado
        """
        session = self._get_session()
        try:
            model = self._entity_to_model(lectura)
            session.add(model)
            session.flush()  # Para obtener el ID generado

            # Actualizar la entidad con el ID generado
            lectura.id = model.id
            session.commit()

            return lectura

        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error al guardar lectura de calidad del aire: {str(e)}")

    def find_by_id(self, lectura_id: int) -> Optional[LecturaCalidadAire]:
        """
        Busca una lectura por su ID.

        Args:
            lectura_id: El ID de la lectura a buscar

        Returns:
            LecturaCalidadAire o None: La entidad si existe, None en caso contrario
        """
        session = self._get_session()
        try:
            model = session.query(LecturaCalidadAireModel).filter_by(id=lectura_id).first()
            return self._model_to_entity(model) if model else None
        except SQLAlchemyError:
            return None

    def find_by_dispositivo(self, dispositivo_id: int, limit: int = 100) -> List[LecturaCalidadAire]:
        """
        Obtiene las últimas lecturas de un dispositivo específico.

        Args:
            dispositivo_id: El ID del dispositivo
            limit: Número máximo de lecturas a retornar (más recientes primero)

        Returns:
            List[LecturaCalidadAire]: Lista de lecturas ordenadas por fecha descendente
        """
        session = self._get_session()
        try:
            models = session.query(LecturaCalidadAireModel)\
                .filter_by(dispositivo_id=dispositivo_id)\
                .order_by(desc(LecturaCalidadAireModel.fecha_lectura))\
                .limit(limit)\
                .all()
            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def find_by_sala(self, sala_id: int, limit: int = 100) -> List[LecturaCalidadAire]:
        """
        Obtiene las últimas lecturas de todos los dispositivos en una sala.

        Args:
            sala_id: El ID de la sala
            limit: Número máximo de lecturas por dispositivo

        Returns:
            List[LecturaCalidadAire]: Lista de lecturas de todos los dispositivos de la sala
        """
        session = self._get_session()
        try:
            # Subquery para obtener los IDs de dispositivos en la sala
            from src.infrastructure.database.models.dispositivo import Dispositivo as DispositivoModel

            dispositivo_ids = session.query(DispositivoModel.id)\
                .filter_by(sala_id=sala_id)\
                .subquery()

            models = session.query(LecturaCalidadAireModel)\
                .filter(LecturaCalidadAireModel.dispositivo_id.in_(dispositivo_ids))\
                .order_by(desc(LecturaCalidadAireModel.fecha_lectura))\
                .limit(limit)\
                .all()

            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def find_by_rango_fechas(
        self,
        dispositivo_id: int,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> List[LecturaCalidadAire]:
        """
        Obtiene lecturas de un dispositivo en un rango de fechas.

        Args:
            dispositivo_id: El ID del dispositivo
            fecha_inicio: Fecha de inicio del rango
            fecha_fin: Fecha de fin del rango

        Returns:
            List[LecturaCalidadAire]: Lista de lecturas en el rango especificado
        """
        session = self._get_session()
        try:
            models = session.query(LecturaCalidadAireModel)\
                .filter(
                    and_(
                        LecturaCalidadAireModel.dispositivo_id == dispositivo_id,
                        LecturaCalidadAireModel.fecha_lectura >= fecha_inicio,
                        LecturaCalidadAireModel.fecha_lectura <= fecha_fin
                    )
                )\
                .order_by(LecturaCalidadAireModel.fecha_lectura)\
                .all()

            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def get_ultima_lectura(self, dispositivo_id: int) -> Optional[LecturaCalidadAire]:
        """
        Obtiene la última lectura de un dispositivo.

        Args:
            dispositivo_id: El ID del dispositivo

        Returns:
            LecturaCalidadAire o None: La última lectura o None si no hay lecturas
        """
        session = self._get_session()
        try:
            model = session.query(LecturaCalidadAireModel)\
                .filter_by(dispositivo_id=dispositivo_id)\
                .order_by(desc(LecturaCalidadAireModel.fecha_lectura))\
                .first()

            return self._model_to_entity(model) if model else None
        except SQLAlchemyError:
            return None

    def get_lecturas_problematicas(self, horas: int = 24) -> List[LecturaCalidadAire]:
        """
        Obtiene lecturas que indican problemas de calidad del aire en las últimas horas.

        Args:
            horas: Número de horas hacia atrás para buscar

        Returns:
            List[LecturaCalidadAire]: Lista de lecturas con calidad deficiente
        """
        session = self._get_session()
        try:
            fecha_limite = datetime.now() - timedelta(hours=horas)

            # Criterios de calidad deficiente (según estándares EPA/OMS)
            # PM2.5 > 35 μg/m³ (insalubre), PM10 > 150 μg/m³ (insalubre)
            models = session.query(LecturaCalidadAireModel)\
                .filter(
                    and_(
                        LecturaCalidadAireModel.fecha_lectura >= fecha_limite,
                        or_(
                            LecturaCalidadAireModel.valor_pm2_5 > 35,
                            LecturaCalidadAireModel.valor_pm10 > 150
                        )
                    )
                )\
                .order_by(desc(LecturaCalidadAireModel.fecha_lectura))\
                .all()

            return [self._model_to_entity(model) for model in models]
        except SQLAlchemyError:
            return []

    def get_promedio_calidad_aire(
        self,
        dispositivo_id: int,
        horas: int = 24
    ) -> Optional[dict]:
        """
        Calcula el promedio de calidad del aire de un dispositivo en las últimas horas.

        Args:
            dispositivo_id: El ID del dispositivo
            horas: Número de horas para el cálculo

        Returns:
            dict o None: Diccionario con promedios de PM1, PM2.5, PM10 y nivel de calidad
        """
        session = self._get_session()
        try:
            fecha_limite = datetime.now() - timedelta(hours=horas)

            # Calcular promedios usando funciones de agregación de SQLAlchemy
            result = session.query(
                func.avg(LecturaCalidadAireModel.valor_pm1).label('avg_pm1'),
                func.avg(LecturaCalidadAireModel.valor_pm2_5).label('avg_pm2_5'),
                func.avg(LecturaCalidadAireModel.valor_pm10).label('avg_pm10'),
                func.count(LecturaCalidadAireModel.id).label('count')
            )\
            .filter(
                and_(
                    LecturaCalidadAireModel.dispositivo_id == dispositivo_id,
                    LecturaCalidadAireModel.fecha_lectura >= fecha_limite
                )
            )\
            .first()

            if result.count == 0:
                return None

            # Determinar nivel de calidad basado en PM2.5 (estándar EPA)
            pm25_avg = float(result.avg_pm2_5) if result.avg_pm2_5 else 0

            if pm25_avg <= 12:
                nivel = "BUENO"
            elif pm25_avg <= 35:
                nivel = "MODERADO"
            elif pm25_avg <= 55:
                nivel = "INSALUBRE_GRUPOS_SENSIBLES"
            elif pm25_avg <= 150:
                nivel = "INSALUBRE"
            else:
                nivel = "NOCIVO"

            return {
                'pm1_promedio': float(result.avg_pm1) if result.avg_pm1 else 0,
                'pm2_5_promedio': pm25_avg,
                'pm10_promedio': float(result.avg_pm10) if result.avg_pm10 else 0,
                'nivel_calidad': nivel,
                'total_lecturas': result.count,
                'horas_analizadas': horas
            }

        except SQLAlchemyError:
            return None

    def delete_antiguas(self, dias: int = 90) -> int:
        """
        Elimina lecturas anteriores a un número de días especificado.

        Args:
            dias: Número de días de antigüedad para eliminar

        Returns:
            int: Número de lecturas eliminadas
        """
        session = self._get_session()
        try:
            fecha_limite = datetime.now() - timedelta(days=dias)

            # Eliminar lecturas antiguas
            deleted_count = session.query(LecturaCalidadAireModel)\
                .filter(LecturaCalidadAireModel.fecha_lectura < fecha_limite)\
                .delete()

            session.commit()
            return deleted_count

        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Error al eliminar lecturas antiguas: {str(e)}")