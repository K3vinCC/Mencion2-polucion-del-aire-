# src/infrastructure/services/jwt_service_new.py
"""
Servicio JWT manual para autenticación sin librerías externas.
Implementación según documento maestro con expiración de 12 horas.
"""

import json
import hmac
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import os

class JWTService:
    """
    Implementación manual de JWT siguiendo RFC 7519.
    Token con expiración de 12 horas según documento maestro.
    """
    
    def __init__(self):
        """Inicializa el servicio JWT con configuración del entorno."""
        self.secret_key = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
        self.algorithm = os.getenv('JWT_ALGORITHM', 'HS256')
        self.expiration_hours = int(os.getenv('JWT_EXPIRATION_HOURS', '12'))
        
        if self.algorithm != 'HS256':
            raise ValueError("Solo se soporta el algoritmo HS256")
    
    def _base64_url_encode(self, data: bytes) -> str:
        """Codifica datos en base64url (RFC 4648 section 5)."""
        return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')
    
    def _base64_url_decode(self, data: str) -> bytes:
        """Decodifica datos de base64url."""
        # Agregar padding si es necesario
        padding = 4 - (len(data) % 4)
        if padding != 4:
            data += '=' * padding
        
        return base64.urlsafe_b64decode(data.encode('utf-8'))
    
    def generate_token(self, payload: Dict[str, Any]) -> str:
        """
        Genera un token JWT con expiración de 12 horas.
        
        Args:
            payload: Datos del usuario/dispositivo
            
        Returns:
            Token JWT firmado
        """
        # Header JWT
        header = {
            'alg': self.algorithm,
            'typ': 'JWT'
        }
        
        # Payload con timestamps
        now = datetime.utcnow()
        token_payload = payload.copy()
        token_payload.update({
            'iat': int(now.timestamp()),  # Issued at
            'exp': int((now + timedelta(hours=self.expiration_hours)).timestamp()),  # Expires
            'iss': 'air-quality-monitoring-api'  # Issuer
        })
        
        # Codificar header y payload
        encoded_header = self._base64_url_encode(
            json.dumps(header, separators=(',', ':')).encode('utf-8')
        )
        encoded_payload = self._base64_url_encode(
            json.dumps(token_payload, separators=(',', ':')).encode('utf-8')
        )
        
        # Crear firma HMAC-SHA256
        message = f"{encoded_header}.{encoded_payload}"
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        encoded_signature = self._base64_url_encode(signature)
        
        # Token completo: header.payload.signature
        return f"{message}.{encoded_signature}"
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verifica y decodifica un token JWT.
        
        Args:
            token: Token JWT a verificar
            
        Returns:
            Payload del token si es válido, None si inválido o expirado
        """
        try:
            # Dividir token en sus 3 partes
            parts = token.split('.')
            if len(parts) != 3:
                return None
            
            header_b64, payload_b64, signature_b64 = parts
            
            # Verificar firma
            message = f"{header_b64}.{payload_b64}"
            expected_signature = hmac.new(
                self.secret_key.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).digest()
            
            received_signature = self._base64_url_decode(signature_b64)
            
            # Comparación segura de firmas
            if not hmac.compare_digest(expected_signature, received_signature):
                return None
            
            # Decodificar payload
            payload_data = self._base64_url_decode(payload_b64)
            payload = json.loads(payload_data.decode('utf-8'))
            
            # Verificar expiración
            now = datetime.utcnow().timestamp()
            if payload.get('exp', 0) <= now:
                return None
            
            return payload
            
        except Exception:
            return None
    
    def create_device_token(self, device_id: int, mac_address: str) -> str:
        """
        Crea un token específico para dispositivos IoT.
        
        Args:
            device_id: ID del dispositivo
            mac_address: Dirección MAC del dispositivo
            
        Returns:
            Token JWT para dispositivo
        """
        payload = {
            'device_id': device_id,
            'mac_address': mac_address,
            'type': 'device'
        }
        
        return self.generate_token(payload)
    
    def validate_user_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Valida un token de usuario y retorna el payload si es válido.
        
        Args:
            token: Token a validar
            
        Returns:
            Payload del usuario si el token es válido
        """
        payload = self.verify_token(token)
        
        if payload and payload.get('type') != 'device':
            return payload
        
        return None
    
    def validate_device_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Valida un token de dispositivo.
        
        Args:
            token: Token a validar
            
        Returns:
            Payload del dispositivo si el token es válido
        """
        payload = self.verify_token(token)
        
        if payload and payload.get('type') == 'device':
            return payload
        
        return None
    
    def refresh_token(self, token: str) -> Optional[str]:
        """
        Refresca un token JWT existente si aún es válido.
        
        Args:
            token: Token actual
            
        Returns:
            Nuevo token si el actual es válido, None si no
        """
        payload = self.verify_token(token)
        if not payload:
            return None
        
        # Remover timestamps del payload original para regenerar
        new_payload = {k: v for k, v in payload.items() 
                      if k not in ['iat', 'exp', 'iss']}
        
        return self.generate_token(new_payload)


def validate_api_token(stored_hash: str, provided_token: str) -> bool:
    """
    Valida un token API de dispositivo contra su hash almacenado.
    
    Args:
        stored_hash: Hash bcrypt almacenado en base de datos
        provided_token: Token proporcionado por el dispositivo
        
    Returns:
        True si el token es válido
    """
    try:
        import bcrypt
        return bcrypt.checkpw(
            provided_token.encode('utf-8'),
            stored_hash.encode('utf-8')
        )
    except Exception:
        return False


def generate_api_token() -> str:
    """
    Genera un token API aleatorio para dispositivos.
    
    Returns:
        Token API de 32 caracteres
    """
    import secrets
    return secrets.token_urlsafe(32)