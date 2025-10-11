# src/application/use_cases/crear_asignacion_limpieza.py
from datetime import datetime
from src.domain.entities.asignacion_limpieza import AsignacionLimpieza
from src.domain.ports.asignacion_limpieza_repository import IAsignacionLimpiezaRepository
from src.domain.ports.usuario_repository import IUsuarioRepository
from src.domain.ports.lectura_calidad_aire_repository import ILecturaCalidadAireRepository
from src.application.errors.exceptions import UsuarioNoEncontradoError, LecturaNoEncontradaError

class CrearAsignacionLimpieza:
    """
    Caso de Uso: Crear una asignación de limpieza basada en una lectura.
    """

    def __init__(self, asignacion_repository: IAsignacionLimpiezaRepository,
                 usuario_repository: IUsuarioRepository,
                 lectura_repository: ILecturaCalidadAireRepository):
        self.asignacion_repository = asignacion_repository
        self.usuario_repository = usuario_repository
        self.lectura_repository = lectura_repository

    def ejecutar(self, id_lectura, id_usuario_asignado, descripcion, prioridad='media'):
        """
        Crea una nueva asignación de limpieza.

        Args:
            id_lectura (int): ID de la lectura que generó la asignación.
            id_usuario_asignado (int): ID del usuario asignado.
            descripcion (str): Descripción de la tarea.
            prioridad (str): Prioridad de la asignación.

        Returns:
            AsignacionLimpieza: La entidad de la asignación creada.

        Raises:
            UsuarioNoEncontradoError: Si el usuario no existe.
            LecturaNoEncontradaError: Si la lectura no existe.
        """
        # Verificar que el usuario existe
        usuario = self.usuario_repository.find_by_id(id_usuario_asignado)
        if not usuario:
            raise UsuarioNoEncontradoError()

        # Verificar que la lectura existe
        lectura = self.lectura_repository.find_by_id(id_lectura)
        if not lectura:
            raise LecturaNoEncontradaError()

        nueva_asignacion = AsignacionLimpieza(
            id=None,
            id_lectura=id_lectura,
            id_usuario_asignado=id_usuario_asignado,
            descripcion=descripcion,
            estado='pendiente',
            prioridad=prioridad,
            fecha_asignacion=datetime.utcnow().isoformat()
        )

        asignacion_creada = self.asignacion_repository.save(nueva_asignacion)
        return asignacion_creada