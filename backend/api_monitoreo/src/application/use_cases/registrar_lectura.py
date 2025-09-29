# src/application/use_cases/registrar_lectura.py
from datetime import datetime
from src.domain.entities.lectura_calidad_aire import LecturaCalidadAire
from src.domain.ports.lectura_calidad_aire_repository import ILecturaCalidadAireRepository
from src.domain.ports.dispositivo_repository import IDispositivoRepository
from src.application.errors.exceptions import DispositivoNoEncontradoError

class RegistrarLectura:
    """
    Caso de Uso: Registrar una nueva lectura de calidad del aire.
    """

    def __init__(self, lectura_repository: ILecturaCalidadAireRepository,
                 dispositivo_repository: IDispositivoRepository):
        self.lectura_repository = lectura_repository
        self.dispositivo_repository = dispositivo_repository

    def ejecutar(self, token_dispositivo, pm25, pm10, co2, temperatura, humedad):
        """
        Registra una nueva lectura de calidad del aire.

        Args:
            token_dispositivo (str): Token del dispositivo que envía la lectura.
            pm25 (float): Concentración de PM2.5.
            pm10 (float): Concentración de PM10.
            co2 (float): Concentración de CO2.
            temperatura (float): Temperatura.
            humedad (float): Humedad.

        Returns:
            LecturaCalidadAire: La entidad de la lectura recién creada.

        Raises:
            DispositivoNoEncontradoError: Si el dispositivo no existe.
        """
        # Verificar que el dispositivo existe
        dispositivo = self.dispositivo_repository.find_by_token(token_dispositivo)
        if not dispositivo:
            raise DispositivoNoEncontradoError()

        # Crear la lectura
        nueva_lectura = LecturaCalidadAire(
            id=None,
            id_dispositivo=dispositivo.id,
            pm25=pm25,
            pm10=pm10,
            co2=co2,
            temperatura=temperatura,
            humedad=humedad,
            timestamp=datetime.utcnow().isoformat()
        )

        # Actualizar última lectura del dispositivo
        self.dispositivo_repository.update_ultima_lectura(dispositivo.id, nueva_lectura.timestamp)

        # Verificar si se necesita crear una asignación de limpieza
        if self._requiere_limpieza(nueva_lectura):
            # Aquí se podría crear una asignación automáticamente
            pass

        lectura_creada = self.lectura_repository.save(nueva_lectura)
        return lectura_creada

    def _requiere_limpieza(self, lectura):
        """
        Determina si una lectura requiere una asignación de limpieza.
        """
        indice = lectura.calcular_indice_calidad()
        return indice > 150  # Umbral para requerir limpieza