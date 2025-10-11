import jwt
import bcrypt
import os
from datetime import datetime, timedelta
from src.domain.ports.usuario_repository import IUsuarioRepository
from src.domain.entities.usuario import Usuario
import inject

class AuthService:
    """Servicio de autenticación"""
    
    @inject.autoparams()
    def __init__(self, usuario_repository: IUsuarioRepository):
        self.usuario_repository = usuario_repository
        self.secret_key = os.getenv('JWT_SECRET_KEY')
        self.algorithm = os.getenv('JWT_ALGORITHM', 'HS256')
        self.token_expiration = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 43200))
    
    def _generar_token(self, usuario: Usuario) -> str:
        """
        Genera un token JWT para un usuario
        """
        payload = {
            'sub': usuario.id,
            'email': usuario.email,
            'rol': usuario.rol_id,
            'universidad': usuario.universidad_id,
            'exp': datetime.utcnow() + timedelta(seconds=self.token_expiration)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def crear_usuario(self, usuario: Usuario) -> Usuario:
        """
        Crea un nuevo usuario en el sistema
        """
        # Verificar si ya existe un usuario con ese email
        if self.usuario_repository.obtener_por_email(usuario.email):
            raise ValueError(f"Ya existe un usuario con el email {usuario.email}")
        
        return self.usuario_repository.crear(usuario)
    
    def login(self, email: str, password: str) -> str:
        """
        Autentica un usuario y retorna un token JWT
        """
        usuario = self.usuario_repository.obtener_por_email(email)
        if not usuario:
            return None
            
        if bcrypt.checkpw(password.encode(), usuario.clave_hash.encode()):
            return self._generar_token(usuario)
        return None
    
    def validar_token(self, token: str) -> Usuario:
        """
        Valida un token JWT y retorna el usuario
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            usuario = self.usuario_repository.obtener_por_id(payload['sub'])
            return usuario
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def puede_ver_dispositivo(self, usuario: Usuario, dispositivo_id: int) -> bool:
        """
        Verifica si un usuario tiene permiso para ver un dispositivo
        """
        # SuperAdmin puede ver todo
        if usuario.es_super_admin:
            return True
            
        # TODO: Implementar lógica de permisos basada en la jerarquía
        # Universidad -> Campus -> Edificio -> Sala -> Dispositivo
        return False