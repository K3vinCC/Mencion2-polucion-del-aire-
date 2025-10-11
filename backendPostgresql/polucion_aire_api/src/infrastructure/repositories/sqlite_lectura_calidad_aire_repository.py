from typing import List, Optional, Tuple
from datetime import datetime
from sqlalchemy import func
from src.domain.ports.lectura_calidad_aire_repository import ILecturaCalidadAireRepository
from src.domain.entities.lectura_calidad_aire import LecturaCalidadAire
from src.infrastructure.database.models.lectura_calidad_aire import LecturaCalidadAireModel
from src.infrastructure.database.database import Session

class SQLiteLecturaCalidadAireRepository(ILecturaCalidadAireRepository):
    """Implementación SQLite del repositorio de lecturas de calidad del aire"""
    
    def __init__(self):
        self.session = Session()
    
    def _to_entity(self, model: LecturaCalidadAireModel) -> LecturaCalidadAire:
        """Convierte un modelo de la base de datos a una entidad del dominio"""
        return LecturaCalidadAire(
            id=model.id,
            dispositivo_id=model.dispositivo_id,
            valor_pm1=model.valor_pm1,
            valor_pm2_5=model.valor_pm2_5,
            valor_pm10=model.valor_pm10,
            etiqueta=model.etiqueta,
            fecha_lectura=model.fecha_lectura
        )
    
    def crear(self, lectura: LecturaCalidadAire) -> LecturaCalidadAire:
        model = LecturaCalidadAireModel(
            dispositivo_id=lectura.dispositivo_id,
            valor_pm1=lectura.valor_pm1,
            valor_pm2_5=lectura.valor_pm2_5,
            valor_pm10=lectura.valor_pm10,
            etiqueta=lectura.etiqueta,
            fecha_lectura=lectura.fecha_lectura
        )
        self.session.add(model)
        self.session.commit()
        return self._to_entity(model)
    
    def obtener_ultimas_lecturas(self, dispositivo_id: int, limite: int = 10) -> List[LecturaCalidadAire]:
        models = self.session.query(LecturaCalidadAireModel)\
            .filter(LecturaCalidadAireModel.dispositivo_id == dispositivo_id)\
            .order_by(LecturaCalidadAireModel.fecha_lectura.desc())\
            .limit(limite)\
            .all()
        return [self._to_entity(m) for m in models]
    
    def obtener_promedio_periodo(
        self,
        dispositivo_id: int,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> Tuple[float, float, float]:
        result = self.session.query(
            func.avg(LecturaCalidadAireModel.valor_pm1),
            func.avg(LecturaCalidadAireModel.valor_pm2_5),
            func.avg(LecturaCalidadAireModel.valor_pm10)
        ).filter(
            LecturaCalidadAireModel.dispositivo_id == dispositivo_id,
            LecturaCalidadAireModel.fecha_lectura >= fecha_inicio,
            LecturaCalidadAireModel.fecha_lectura <= fecha_fin
        ).first()
        
        return (
            float(result[0]) if result[0] else 0.0,
            float(result[1]) if result[1] else 0.0,
            float(result[2]) if result[2] else 0.0
        )
    
    def obtener_lecturas_criticas(
        self,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> List[LecturaCalidadAire]:
        # Consideramos críticas las lecturas con PM2.5 > 55.4 (nivel "Nocivo" o peor)
        models = self.session.query(LecturaCalidadAireModel)\
            .filter(
                LecturaCalidadAireModel.fecha_lectura >= fecha_inicio,
                LecturaCalidadAireModel.fecha_lectura <= fecha_fin,
                LecturaCalidadAireModel.valor_pm2_5 > 55.4
            )\
            .order_by(LecturaCalidadAireModel.valor_pm2_5.desc())\
            .all()
        return [self._to_entity(m) for m in models]