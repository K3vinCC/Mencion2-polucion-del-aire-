# src/domain/entities/asignacion_limpieza.py

class AsignacionLimpieza:
    """
    Entidad que representa una asignación de tarea de limpieza basada en lecturas de calidad del aire.
    """

    def __init__(self, id, id_lectura, id_usuario_asignado, descripcion, estado='pendiente', prioridad='media', fecha_asignacion=None, fecha_completado=None):
        """
        Constructor para la entidad AsignacionLimpieza.

        Args:
            id (int): Identificador único de la asignación
            id_lectura (int): ID de la lectura que generó la asignación
            id_usuario_asignado (int): ID del usuario (conserje) asignado
            descripcion (str): Descripción detallada de la tarea
            estado (str): Estado de la asignación ('pendiente', 'en_progreso', 'completada', 'cancelada')
            prioridad (str): Prioridad de la tarea ('baja', 'media', 'alta', 'urgente')
            fecha_asignacion (str, optional): Fecha de asignación
            fecha_completado (str, optional): Fecha de completado
        """
        self.id = id
        self.id_lectura = id_lectura
        self.id_usuario_asignado = id_usuario_asignado
        self.descripcion = descripcion
        self.estado = estado
        self.prioridad = prioridad
        self.fecha_asignacion = fecha_asignacion
        self.fecha_completado = fecha_completado

    def to_dict(self):
        """
        Convierte la entidad AsignacionLimpieza en un diccionario.
        """
        return {
            "id": self.id,
            "id_lectura": self.id_lectura,
            "id_usuario_asignado": self.id_usuario_asignado,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "prioridad": self.prioridad,
            "fecha_asignacion": self.fecha_asignacion,
            "fecha_completado": self.fecha_completado
        }

    def marcar_completada(self):
        """
        Marca la asignación como completada.
        """
        self.estado = 'completada'
        # Aquí se podría agregar lógica para timestamp

    def es_urgente(self):
        """
        Verifica si la asignación es urgente.
        """
        return self.prioridad in ['alta', 'urgente']