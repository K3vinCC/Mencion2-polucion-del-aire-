from typing import List, Optional
from src.domain.ports.usuario_repository import IUsuarioRepository
from src.domain.entities.usuario import Usuario
from src.infrastructure.database.models.usuario import UsuarioModel
from src.infrastructure.database.database import Session

class SQLiteUsuarioRepository(IUsuarioRepository):
    """Implementación SQLite del repositorio de usuarios"""
    
    def __init__(self):
        self.session = Session()
    
    def _to_entity(self, model: UsuarioModel) -> Usuario:
        """Convierte un modelo de la base de datos a una entidad del dominio"""
        return Usuario(
            id=model.id,
            email=model.email,
            nombre_completo=model.nombre_completo,
            rol_id=model.rol_id,
            universidad_id=model.universidad_id,
            fecha_creacion=model.fecha_creacion,
            clave_hash=model.clave_hash
        )
    
    def crear(self, usuario: Usuario) -> Usuario:
        model = UsuarioModel(
            email=usuario.email,
            clave_hash=usuario.clave_hash,
            nombre_completo=usuario.nombre_completo,
            rol_id=usuario.rol_id,
            universidad_id=usuario.universidad_id
        )
        self.session.add(model)
        self.session.commit()
        return self._to_entity(model)
    
    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        model = self.session.query(UsuarioModel).filter(UsuarioModel.id == id).first()
        return self._to_entity(model) if model else None
    
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        model = self.session.query(UsuarioModel).filter(UsuarioModel.email == email).first()
        return self._to_entity(model) if model else None
    
    def actualizar(self, usuario: Usuario) -> Usuario:
        model = self.session.query(UsuarioModel).filter(UsuarioModel.id == usuario.id).first()
        if model:
            model.email = usuario.email
            if usuario.clave_hash:
                model.clave_hash = usuario.clave_hash
            model.nombre_completo = usuario.nombre_completo
            model.rol_id = usuario.rol_id
            model.universidad_id = usuario.universidad_id
            self.session.commit()
            return self._to_entity(model)
        return None
    
    def eliminar(self, id: int) -> bool:
        model = self.session.query(UsuarioModel).filter(UsuarioModel.id == id).first()
        if model:
            self.session.delete(model)
            self.session.commit()
            return True
        return False
    
    def listar_por_universidad(self, universidad_id: int) -> List[Usuario]:
        models = self.session.query(UsuarioModel).filter(
            UsuarioModel.universidad_id == universidad_id
        ).all()
        return [self._to_entity(m) for m in models]