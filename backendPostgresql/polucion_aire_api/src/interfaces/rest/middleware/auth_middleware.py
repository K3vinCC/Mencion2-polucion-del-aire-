from functools import wraps
from flask import request, jsonify, g
import inject
from src.application.auth.auth_service import AuthService

def require_auth(f):
    """Decorator para requerir autenticación en endpoints"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No se proporcionó token de autorización'}), 401
            
        try:
            token_type, token = auth_header.split(' ')
            if token_type.lower() != 'bearer':
                return jsonify({'error': 'Tipo de token inválido'}), 401
                
            auth_service = inject.instance(AuthService)
            usuario = auth_service.validar_token(token)
            
            if not usuario:
                return jsonify({'error': 'Token inválido o expirado'}), 401
                
            # Guardar el usuario en el contexto global de Flask
            g.usuario_actual = usuario
            
            return f(*args, **kwargs)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 401
            
    return decorated

def require_roles(*roles):
    """Decorator para requerir roles específicos"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(g, 'usuario_actual'):
                return jsonify({'error': 'No autenticado'}), 401
                
            if g.usuario_actual.rol_id not in roles:
                return jsonify({'error': 'No autorizado para esta acción'}), 403
                
            return f(*args, **kwargs)
        return decorated
    return decorator