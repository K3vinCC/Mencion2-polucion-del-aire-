from typing import List, Optional
from datetime import datetime
from src.domain.ports.dispositivo_repository import IDispositivoRepository
from src.domain.entities.dispositivo import Dispositivo
from src.infrastructure.database.models.dispositivo import DispositivoModel
from src.infrastructure.database.database import Session

class SQLiteDispositivoRepository(IDispositivoRepository):
    """Implementación SQLite del repositorio de dispositivos"""
    
    def __init__(self):
        self.session = Session()
    
    def _to_entity(self, model: DispositivoModel) -> Dispositivo:
        """Convierte un modelo de la base de datos a una entidad del dominio"""
        return Dispositivo(
            id=model.id,
            sala_id=model.sala_id,
            modelo_id=model.modelo_id,
            id_hardware=model.id_hardware,
            api_token_hash=model.api_token_hash,
            fecha_instalacion=model.fecha_instalacion,
            ultimo_mantenimiento=model.ultimo_mantenimiento,
            estado=model.estado,
            ultima_vez_visto=model.ultima_vez_visto
        )
    
    def crear(self, dispositivo: Dispositivo) -> Dispositivo:
        model = DispositivoModel(
            sala_id=dispositivo.sala_id,
            modelo_id=dispositivo.modelo_id,
            id_hardware=dispositivo.id_hardware,
            api_token_hash=dispositivo.api_token_hash,
            fecha_instalacion=dispositivo.fecha_instalacion,
            ultimo_mantenimiento=dispositivo.ultimo_mantenimiento,
            estado=dispositivo.estado,
            ultima_vez_visto=dispositivo.ultima_vez_visto
        )
        self.session.add(model)
        self.session.commit()
        return self._to_entity(model)
    
    def obtener_por_id(self, id: int) -> Optional[Dispositivo]:
        model = self.session.query(DispositivoModel).filter(DispositivoModel.id == id).first()
        return self._to_entity(model) if model else None
    
    def obtener_por_id_hardware(self, id_hardware: str) -> Optional[Dispositivo]:
        model = self.session.query(DispositivoModel).filter(DispositivoModel.id_hardware == id_hardware).first()
        return self._to_entity(model) if model else None
    
    def actualizar_estado(self, id: int, estado: str, ultima_vez_visto: datetime) -> bool:
        model = self.session.query(DispositivoModel).filter(DispositivoModel.id == id).first()
        if model:
            model.estado = estado
            model.ultima_vez_visto = ultima_vez_visto
            self.session.commit()
            return True
        return False
    
    def listar_por_sala(self, sala_id: int) -> List[Dispositivo]:
        models = self.session.query(DispositivoModel).filter(DispositivoModel.sala_id == sala_id).all()
        return [self._to_entity(m) for m in models]
    
    def listar_desconectados(self) -> List[Dispositivo]:
        models = self.session.query(DispositivoModel).filter(
            DispositivoModel.estado == 'desconectado'
        ).all()
        return [self._to_entity(m) for m in models]