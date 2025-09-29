# src/infrastructure/middleware/__init__.py
"""
Módulo de middlewares de infraestructura.
Contiene decoradores y middlewares para autenticación y autorización.
"""

from .auth_middleware import (
    token_required,
    role_required,
    device_token_required,
    universidad_required,
    log_request,
    rate_limit
)

__all__ = [
    'token_required',
    'role_required',
    'device_token_required',
    'universidad_required',
    'log_request',
    'rate_limit'
]