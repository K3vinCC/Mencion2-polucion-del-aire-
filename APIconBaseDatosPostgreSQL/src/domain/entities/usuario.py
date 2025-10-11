# src/domain/entities/usuario.py
"""
Entidad de dominio Usuario.
Representa un usuario del sistema con sus atributos y reglas de negocio.
"""

from datetime import datetime
from typing import Optional


class Usuario:
    """
    Entidad Usuario del dominio.

    Representa a cualquier usuario del sistema: SuperAdmin, Admin_Universidad,
    Conserje o Limpiador.
    """

    def __init__(
        self,
        id: Optional[int],
        email: str,
        clave_hash: str,
        nombre_completo: str,
        rol_id: int,
        universidad_id: Optional[int] = None,
        fecha_creacion: Optional[datetime] = None
    ):
        """
        Constructor de la entidad Usuario.

        Args:
            id: Identificador único del usuario
            email: Correo electrónico único del usuario
            clave_hash: Hash de la contraseña (nunca se almacena en texto plano)
            nombre_completo: Nombre completo del usuario
            rol_id: ID del rol del usuario
            universidad_id: ID de la universidad (opcional, solo para usuarios no SuperAdmin)
            fecha_creacion: Fecha de creación del usuario
        """
        self.id = id
        self.email = email
        self.clave_hash = clave_hash
        self.nombre_completo = nombre_completo
        self.rol_id = rol_id
        self.universidad_id = universidad_id
        self.fecha_creacion = fecha_creacion or datetime.now()

        # Validaciones de negocio
        self._validar_email()
        self._validar_rol()

    def _validar_email(self):
        """Valida que el email tenga un formato correcto."""
        if not self.email or '@' not in self.email:
            raise ValueError("Email inválido")

    def _validar_rol(self):
        """Valida que el rol sea uno de los permitidos."""
        roles_validos = [1, 2, 3, 4]  # SuperAdmin, Admin_Universidad, Conserje, Limpiador
        if self.rol_id not in roles_validos:
            raise ValueError("Rol inválido")

    def es_super_admin(self) -> bool:
        """Verifica si el usuario es SuperAdmin."""
        return self.rol_id == 1

    def es_admin_universidad(self) -> bool:
        """Verifica si el usuario es Admin_Universidad."""
        return self.rol_id == 2

    def es_conserje(self) -> bool:
        """Verifica si el usuario es Conserje."""
        return self.rol_id == 3

    def es_limpiador(self) -> bool:
        """Verifica si el usuario es Limpiador."""
        return self.rol_id == 4

    def puede_gestionar_universidad(self, universidad_id: int) -> bool:
        """
        Verifica si el usuario puede gestionar una universidad específica.

        SuperAdmin puede gestionar cualquier universidad.
        Admin_Universidad solo puede gestionar su universidad asignada.
        """
        if self.es_super_admin():
            return True
        return self.universidad_id == universidad_id

    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario (útil para respuestas JSON).

        Excluye información sensible como el hash de la contraseña.
        """
        return {
            "id": self.id,
            "email": self.email,
            "nombre_completo": self.nombre_completo,
            "rol_id": self.rol_id,
            "universidad_id": self.universidad_id,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

    def __eq__(self, other):
        """Compara dos usuarios por su ID."""
        if not isinstance(other, Usuario):
            return False
        return self.id == other.id

    def __hash__(self):
        """Hash basado en el ID para usar en sets y diccionarios."""
        return hash(self.id)

    def __repr__(self):
        """Representación string del usuario."""
        return f"Usuario(id={self.id}, email='{self.email}', rol_id={self.rol_id})"