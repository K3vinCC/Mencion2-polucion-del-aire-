# src/domain/entities/asignacion_limpieza.py
"""
Entidad de dominio AsignacionLimpieza.
Representa una asignación de tarea de limpieza a un limpiador.
"""

from datetime import datetime
from typing import Optional


class AsignacionLimpieza:
    """
    Entidad AsignacionLimpieza del dominio.

    Representa la asignación de una tarea de limpieza a un usuario limpiador
    cuando una sala presenta condiciones ambientales deficientes.
    """

    ESTADOS_VALIDOS = ['pendiente', 'en_progreso', 'completada', 'cancelada']

    def __init__(
        self,
        id: Optional[int],
        sala_id: int,
        asignado_por_usuario_id: int,
        asignado_a_usuario_id: int,
        estado: str = 'pendiente',
        fecha_creacion: Optional[datetime] = None,
        fecha_completado: Optional[datetime] = None
    ):
        """
        Constructor de la entidad AsignacionLimpieza.

        Args:
            id: Identificador único de la asignación
            sala_id: ID de la sala que necesita limpieza
            asignado_por_usuario_id: ID del usuario que creó la asignación
            asignado_a_usuario_id: ID del usuario limpiador asignado
            estado: Estado de la asignación
            fecha_creacion: Fecha de creación de la asignación
            fecha_completado: Fecha de completación (si aplica)
        """
        self.id = id
        self.sala_id = sala_id
        self.asignado_por_usuario_id = asignado_por_usuario_id
        self.asignado_a_usuario_id = asignado_a_usuario_id
        self.estado = estado
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.fecha_completado = fecha_completado

        # Validaciones de negocio
        self._validar_estado()
        self._validar_usuarios_diferentes()

    def _validar_estado(self):
        """Valida que el estado sea uno de los permitidos."""
        if self.estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Debe ser uno de: {self.ESTADOS_VALIDOS}")

    def _validar_usuarios_diferentes(self):
        """Valida que el asignador y el asignado sean usuarios diferentes."""
        if self.asignado_por_usuario_id == self.asignado_a_usuario_id:
            raise ValueError("El usuario asignador no puede ser el mismo que el asignado")

    def marcar_en_progreso(self):
        """Marca la asignación como en progreso."""
        if self.estado != 'pendiente':
            raise ValueError("Solo las asignaciones pendientes pueden marcarse como en progreso")
        self.estado = 'en_progreso'

    def marcar_completada(self):
        """Marca la asignación como completada y registra la fecha."""
        if self.estado not in ['pendiente', 'en_progreso']:
            raise ValueError("Solo las asignaciones pendientes o en progreso pueden completarse")
        self.estado = 'completada'
        self.fecha_completado = datetime.now()

    def cancelar(self):
        """Cancela la asignación."""
        if self.estado in ['completada', 'cancelada']:
            raise ValueError("No se pueden cancelar asignaciones ya completadas o canceladas")
        self.estado = 'cancelada'

    def esta_pendiente(self) -> bool:
        """Verifica si la asignación está pendiente."""
        return self.estado == 'pendiente'

    def esta_en_progreso(self) -> bool:
        """Verifica si la asignación está en progreso."""
        return self.estado == 'en_progreso'

    def esta_completada(self) -> bool:
        """Verifica si la asignación está completada."""
        return self.estado == 'completada'

    def esta_cancelada(self) -> bool:
        """Verifica si la asignación está cancelada."""
        return self.estado == 'cancelada'

    def tiempo_transcurrido(self) -> Optional[float]:
        """
        Calcula el tiempo transcurrido desde la creación en horas.

        Returns:
            float: Horas transcurridas, o None si no hay fecha de creación
        """
        if not self.fecha_creacion:
            return None

        tiempo_total = datetime.now() - self.fecha_creacion
        return tiempo_total.total_seconds() / 3600  # Convertir a horas

    def tiempo_para_completar(self) -> Optional[float]:
        """
        Calcula el tiempo que tomó completar la asignación en horas.

        Returns:
            float: Horas para completar, o None si no está completada
        """
        if not self.esta_completada() or not self.fecha_completado:
            return None

        tiempo_total = self.fecha_completado - self.fecha_creacion
        return tiempo_total.total_seconds() / 3600  # Convertir a horas

    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario (útil para respuestas JSON).
        """
        return {
            "id": self.id,
            "sala_id": self.sala_id,
            "asignado_por_usuario_id": self.asignado_por_usuario_id,
            "asignado_a_usuario_id": self.asignado_a_usuario_id,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_completado": self.fecha_completado.isoformat() if self.fecha_completado else None,
            "tiempo_transcurrido_horas": self.tiempo_transcurrido(),
            "tiempo_completado_horas": self.tiempo_para_completar()
        }

    def __eq__(self, other):
        """Compara dos asignaciones por su ID."""
        if not isinstance(other, AsignacionLimpieza):
            return False
        return self.id == other.id

    def __hash__(self):
        """Hash basado en el ID para usar en sets y diccionarios."""
        return hash(self.id)

    def __repr__(self):
        """Representación string de la asignación."""
        return f"AsignacionLimpieza(id={self.id}, sala_id={self.sala_id}, estado='{self.estado}')"