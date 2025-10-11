# src/application/use_cases/crear_asignacion_limpieza.py
"""
Caso de uso: Crear Asignación de Limpieza
Permite crear asignaciones de tareas de limpieza cuando hay problemas de calidad del aire.
"""

from src.domain.ports.asignacion_limpieza_repository import IAsignacionLimpiezaRepository
from src.domain.ports.usuario_repository import IUsuarioRepository
from src.domain.ports.notificacion_service import INotificacionService
from src.domain.entities.asignacion_limpieza import AsignacionLimpieza


class CrearAsignacionLimpieza:
    """
    Caso de uso para crear asignaciones de limpieza.

    Maneja la creación de tareas de limpieza cuando se detectan
    problemas de calidad del aire, incluyendo notificaciones.
    """

    def __init__(
        self,
        asignacion_repository: IAsignacionLimpiezaRepository,
        usuario_repository: IUsuarioRepository,
        notificacion_service: INotificacionService
    ):
        """
        Constructor del caso de uso.

        Args:
            asignacion_repository: Repositorio de asignaciones inyectado
            usuario_repository: Repositorio de usuarios inyectado
            notificacion_service: Servicio de notificaciones inyectado
        """
        self.asignacion_repository = asignacion_repository
        self.usuario_repository = usuario_repository
        self.notificacion_service = notificacion_service

    def ejecutar(
        self,
        sala_id: int,
        asignado_por_usuario_id: int,
        asignado_a_usuario_id: int,
        mensaje_personalizado: str = None
    ) -> AsignacionLimpieza:
        """
        Ejecuta la creación de una nueva asignación de limpieza.

        Args:
            sala_id: ID de la sala que necesita limpieza
            asignado_por_usuario_id: ID del usuario que crea la asignación
            asignado_a_usuario_id: ID del usuario limpiador asignado
            mensaje_personalizado: Mensaje adicional para el limpiador

        Returns:
            AsignacionLimpieza: La entidad de la asignación creada

        Raises:
            ValueError: Si los datos son inválidos o hay conflictos
        """
        # Validar datos de entrada
        self._validar_datos(sala_id, asignado_por_usuario_id, asignado_a_usuario_id)

        # Verificar permisos del usuario que asigna
        usuario_asignador = self.usuario_repository.find_by_id(asignado_por_usuario_id)
        if not usuario_asignador or not usuario_asignador.es_conserje():
            raise ValueError("Solo los conserjes pueden crear asignaciones de limpieza")

        # Verificar que el usuario asignado sea un limpiador
        usuario_limpiador = self.usuario_repository.find_by_id(asignado_a_usuario_id)
        if not usuario_limpiador or not usuario_limpiador.es_limpiador():
            raise ValueError("El usuario asignado debe ser un limpiador")

        # Verificar que ambos usuarios pertenezcan a la misma universidad
        if usuario_asignador.universidad_id != usuario_limpiador.universidad_id:
            raise ValueError("El conserje y el limpiador deben pertenecer a la misma universidad")

        # Verificar que no haya una asignación pendiente para la misma sala
        asignaciones_pendientes = self.asignacion_repository.find_pendientes_por_sala(sala_id)
        if asignaciones_pendientes:
            raise ValueError("Ya existe una asignación pendiente para esta sala")

        # Crear asignación
        asignacion = AsignacionLimpieza(
            id=None,
            sala_id=sala_id,
            asignado_por_usuario_id=asignado_por_usuario_id,
            asignado_a_usuario_id=asignado_a_usuario_id,
            estado='pendiente'
        )

        # Guardar asignación
        asignacion_creada = self.asignacion_repository.save(asignacion)

        # Enviar notificación al limpiador
        self._enviar_notificacion(asignacion_creada, mensaje_personalizado)

        return asignacion_creada

    def _validar_datos(self, sala_id: int, asignado_por_id: int, asignado_a_id: int):
        """
        Valida los datos de entrada.

        Args:
            sala_id: ID de la sala
            asignado_por_id: ID del usuario asignador
            asignado_a_id: ID del usuario asignado

        Raises:
            ValueError: Si algún dato es inválido
        """
        if not sala_id or sala_id <= 0:
            raise ValueError("ID de sala inválido")

        if not asignado_por_id or asignado_por_id <= 0:
            raise ValueError("ID del usuario asignador inválido")

        if not asignado_a_id or asignado_a_id <= 0:
            raise ValueError("ID del usuario asignado inválido")

        if asignado_por_id == asignado_a_id:
            raise ValueError("El usuario no puede asignarse tareas a sí mismo")

    def _enviar_notificacion(self, asignacion: AsignacionLimpieza, mensaje_personalizado: str = None):
        """
        Envía notificación al limpiador asignado.

        Args:
            asignacion: La asignación creada
            mensaje_personalizado: Mensaje adicional opcional
        """
        try:
            # Aquí necesitaríamos información adicional de la sala y edificio
            # Por ahora enviamos una notificación básica
            mensaje = mensaje_personalizado or "Se ha asignado una tarea de limpieza en su edificio"

            self.notificacion_service.enviar_asignacion_limpieza(
                usuario_id=asignacion.asignado_a_usuario_id,
                sala_id=asignacion.sala_id,
                mensaje_instrucciones=mensaje
            )
        except Exception as e:
            # Loggear error pero no fallar la creación de la asignación
            print(f"Error enviando notificación: {e}")
            # En un sistema real, aquí usaríamos un logger