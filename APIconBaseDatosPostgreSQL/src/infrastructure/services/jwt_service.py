# src/infrastructure/services/jwt_service.py
"""
Servicio de autenticación JWT.
Implementa la creación, validación y gestión de tokens JWT.
"""

import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet

from src.config import get_config


class JWTService:
    """
    Servicio para manejo de autenticación JWT.

    Proporciona métodos para crear tokens, validarlos y extraer información.
    """

    def __init__(self):
        """Inicializa el servicio con la configuración."""
        self.config = get_config()
        self.secret_key = self.config.JWT_SECRET_KEY
        self.algorithm = self.config.JWT_ALGORITHM
        self.expiration_hours = self.config.JWT_EXPIRATION_HOURS

        # Servicio de encriptación para datos sensibles
        encryption_key = self.config.ENCRYPTION_KEY
        if encryption_key:
            self.cipher = Fernet(encryption_key.encode())
        else:
            self.cipher = None

    def hash_password(self, password: str) -> str:
        """
        Hashea una contraseña usando bcrypt.

        Args:
            password: Contraseña en texto plano

        Returns:
            str: Hash de la contraseña
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verifica si una contraseña coincide con su hash.

        Args:
            password: Contraseña en texto plano
            hashed: Hash de la contraseña

        Returns:
            bool: True si coincide, False en caso contrario
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def create_token(self, user_id: int, email: str, role: str, universidad_id: Optional[int] = None) -> str:
        """
        Crea un token JWT para un usuario.

        Args:
            user_id: ID del usuario
            email: Email del usuario
            role: Rol del usuario
            universidad_id: ID de la universidad (opcional)

        Returns:
            str: Token JWT
        """
        now = datetime.utcnow()
        expiration = now + timedelta(hours=self.expiration_hours)

        payload = {
            'user_id': user_id,
            'email': email,
            'role': role,
            'universidad_id': universidad_id,
            'iat': now,
            'exp': expiration,
            'iss': 'air_quality_api',
            'aud': 'air_quality_clients'
        }

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def create_device_token(self, device_id: int, mac_address: str) -> str:
        """
        Crea un token JWT para un dispositivo IoT.

        Args:
            device_id: ID del dispositivo
            mac_address: Dirección MAC del dispositivo

        Returns:
            str: Token JWT para dispositivo
        """
        now = datetime.utcnow()
        # Tokens de dispositivo expiran en 24 horas
        expiration = now + timedelta(hours=24)

        payload = {
            'device_id': device_id,
            'mac_address': mac_address,
            'type': 'device',
            'iat': now,
            'exp': expiration,
            'iss': 'air_quality_api',
            'aud': 'air_quality_devices'
        }

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Valida un token JWT y retorna su payload si es válido.

        Args:
            token: Token JWT a validar

        Returns:
            dict o None: Payload del token si es válido, None en caso contrario
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                audience=['air_quality_clients', 'air_quality_devices'],
                issuer='air_quality_api'
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception:
            return None

    def validate_user_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Valida un token JWT de usuario.

        Args:
            token: Token JWT a validar

        Returns:
            dict o None: Payload del token si es válido y es de usuario
        """
        payload = self.validate_token(token)
        if payload and payload.get('type') != 'device':
            return payload
        return None

    def validate_device_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Valida un token JWT de dispositivo.

        Args:
            token: Token JWT a validar

        Returns:
            dict o None: Payload del token si es válido y es de dispositivo
        """
        payload = self.validate_token(token)
        if payload and payload.get('type') == 'device':
            return payload
        return None

    def get_token_expiration(self, token: str) -> Optional[datetime]:
        """
        Obtiene la fecha de expiración de un token.

        Args:
            token: Token JWT

        Returns:
            datetime o None: Fecha de expiración si el token es válido
        """
        payload = self.validate_token(token)
        if payload and 'exp' in payload:
            return datetime.fromtimestamp(payload['exp'])
        return None

    def refresh_token(self, token: str) -> Optional[str]:
        """
        Refresca un token JWT si aún no ha expirado.

        Args:
            token: Token JWT a refrescar

        Returns:
            str o None: Nuevo token si el refresh fue exitoso
        """
        payload = self.validate_token(token)
        if not payload or payload.get('type') == 'device':
            return None

        # Crear nuevo token con la misma información
        return self.create_token(
            user_id=payload['user_id'],
            email=payload['email'],
            role=payload['role'],
            universidad_id=payload.get('universidad_id')
        )

    def encrypt_data(self, data: str) -> str:
        """
        Encripta datos sensibles usando Fernet.

        Args:
            data: Datos a encriptar

        Returns:
            str: Datos encriptados en base64

        Raises:
            ValueError: Si el servicio de encriptación no está configurado
        """
        if not self.cipher:
            raise ValueError("Servicio de encriptación no configurado")

        encrypted = self.cipher.encrypt(data.encode('utf-8'))
        return encrypted.decode('utf-8')

    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Desencripta datos usando Fernet.

        Args:
            encrypted_data: Datos encriptados en base64

        Returns:
            str: Datos desencriptados

        Raises:
            ValueError: Si el servicio de encriptación no está configurado
        """
        if not self.cipher:
            raise ValueError("Servicio de encriptación no configurado")

        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode('utf-8'))
            return decrypted.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Error al desencriptar datos: {str(e)}")

    def generate_api_token(self) -> str:
        """
        Genera un token API aleatorio para dispositivos.

        Returns:
            str: Token API encriptado
        """
        import secrets
        token = secrets.token_hex(32)
        return self.encrypt_data(token) if self.cipher else token

    def validate_api_token(self, encrypted_token: str, plain_token: str) -> bool:
        """
        Valida un token API comparándolo con su versión encriptada.

        Args:
            encrypted_token: Token encriptado almacenado
            plain_token: Token en texto plano a validar

        Returns:
            bool: True si coinciden
        """
        if not self.cipher:
            return encrypted_token == plain_token

        try:
            decrypted = self.decrypt_data(encrypted_token)
            return decrypted == plain_token
        except:
            return False