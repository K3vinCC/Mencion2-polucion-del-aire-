# src/application/use_cases/registrar_lectura_aire.py
"""
Caso de uso: Registrar Lectura de Calidad del Aire
Permite registrar nuevas lecturas de sensores con autenticación doble factor.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from src.domain.ports.dispositivo_repository import IDispositivoRepository
from src.domain.ports.lectura_calidad_aire_repository import ILecturaCalidadAireRepository
from src.domain.entities.lectura_calidad_aire import LecturaCalidadAire


class RegistrarLecturaAire:
    """
    Caso de uso para registrar lecturas de calidad del aire desde sensores.

    Implementa autenticación doble factor (MAC + Token API) y validación
    de datos antes de almacenar las lecturas.
    """

    def __init__(
        self,
        dispositivo_repository: IDispositivoRepository,
        lectura_repository: ILecturaCalidadAireRepository
    ):
        """
        Constructor del caso de uso.

        Args:
            dispositivo_repository: Repositorio de dispositivos inyectado
            lectura_repository: Repositorio de lecturas inyectado
        """
        self.dispositivo_repository = dispositivo_repository
        self.lectura_repository = lectura_repository

    def ejecutar(
        self,
        mac_address: str,
        api_token: str,
        pm1: Optional[float] = None,
        pm2_5: Optional[float] = None,
        pm10: Optional[float] = None,
        etiqueta: Optional[str] = None
    ) -> dict:
        """
        Ejecuta el registro de una nueva lectura de calidad del aire.

        Args:
            mac_address: Dirección MAC del dispositivo sensor
            api_token: Token API del dispositivo
            pm1: Valor de PM1 (opcional)
            pm2_5: Valor de PM2.5 (opcional)
            pm10: Valor de PM10 (opcional)
            etiqueta: Etiqueta opcional para categorizar la lectura

        Returns:
            dict: Información de la lectura registrada incluyendo nivel de calidad

        Raises:
            ValueError: Si la autenticación falla o los datos son inválidos
        """
        # Autenticar dispositivo con doble factor
        dispositivo = self._autenticar_dispositivo(mac_address, api_token)

        # Validar datos de lectura
        self._validar_datos_lectura(pm1, pm2_5, pm10)

        # Crear entidad de lectura
        lectura = LecturaCalidadAire(
            id=None,
            dispositivo_id=dispositivo.id,
            valor_pm1=Decimal(str(pm1)) if pm1 is not None else None,
            valor_pm2_5=Decimal(str(pm2_5)) if pm2_5 is not None else None,
            valor_pm10=Decimal(str(pm10)) if pm10 is not None else None,
            etiqueta=etiqueta,
            fecha_lectura=datetime.now()
        )

        # Guardar lectura
        lectura_guardada = self.lectura_repository.save(lectura)

        # Actualizar estado del dispositivo
        dispositivo.marcar_como_conectado()
        self.dispositivo_repository.update(dispositivo)

        # Preparar respuesta
        return {
            "lectura_id": lectura_guardada.id,
            "dispositivo_id": dispositivo.id,
            "nivel_calidad": lectura_guardada.get_nivel_calidad(),
            "color_calidad": lectura_guardada.get_color_calidad(),
            "calidad_aceptable": lectura_guardada.es_calidad_aceptable(),
            "requiere_accion": lectura_guardada.requiere_accion_inmediata(),
            "fecha_lectura": lectura_guardada.fecha_lectura.isoformat()
        }

    def _autenticar_dispositivo(self, mac_address: str, api_token: str) -> object:
        """
        Autentica un dispositivo usando doble factor: MAC address + Token API.

        Args:
            mac_address: Dirección MAC del dispositivo
            api_token: Token API proporcionado

        Returns:
            Dispositivo: La entidad del dispositivo autenticado

        Raises:
            ValueError: Si la autenticación falla
        """
        # Buscar dispositivo por MAC
        dispositivo = self.dispositivo_repository.find_by_mac(mac_address.upper())
        if not dispositivo:
            raise ValueError("Dispositivo no encontrado")

        # Verificar token API
        if not dispositivo.verificar_token(api_token):
            raise ValueError("Token API inválido")

        return dispositivo

    def _validar_datos_lectura(
        self,
        pm1: Optional[float],
        pm2_5: Optional[float],
        pm10: Optional[float]
    ):
        """
        Valida los datos de la lectura según reglas de negocio.

        Args:
            pm1: Valor PM1
            pm2_5: Valor PM2.5
            pm10: Valor PM10

        Raises:
            ValueError: Si los datos son inválidos
        """
        # Al menos uno de los valores PM debe estar presente
        if all(v is None for v in [pm1, pm2_5, pm10]):
            raise ValueError("Al menos un valor de PM (PM1, PM2.5 o PM10) debe ser proporcionado")

        # Validar rangos de valores
        valores_pm = [('PM1', pm1), ('PM2.5', pm2_5), ('PM10', pm10)]

        for nombre, valor in valores_pm:
            if valor is not None:
                if valor < 0:
                    raise ValueError(f"El valor de {nombre} no puede ser negativo")
                if valor > 1000:  # Límite superior razonable
                    raise ValueError(f"El valor de {nombre} parece irrazonablemente alto")

        # Validar consistencia: PM1 <= PM2.5 <= PM10 (cuando todos están presentes)
        if all(v is not None for v in [pm1, pm2_5, pm10]):
            if not (pm1 <= pm2_5 <= pm10):
                raise ValueError("Los valores PM deben mantener la relación PM1 ≤ PM2.5 ≤ PM10")