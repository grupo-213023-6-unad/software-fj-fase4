"""
reserva.py

Une un Cliente con un Servicio y maneja su ciclo de vida:
pendiente -> confirmada -> cancelada.

Acá se usan try/except/else/finally y el encadenamiento de
excepciones (raise ... from ...) al procesar el pago, para no perder
la causa original si algo falla.
"""

from datetime import datetime
from entidades import Cliente, Servicio
from excepciones import (
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
)


class Reserva:
    """Reserva de un servicio hecha por un cliente."""

    ESTADOS_VALIDOS = ("pendiente", "confirmada", "cancelada")

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio,
                 duracion: float):
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError(
                "La reserva requiere un objeto Cliente válido."
            )
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError(
                "La reserva requiere un objeto Servicio válido."
            )
        if duracion is None or duracion <= 0:
            raise ReservaInvalidaError(
                "La duración de la reserva debe ser mayor a cero."
            )
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre_servicio}' no está "
                "disponible actualmente."
            )

        self._id_reserva = id_reserva
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "pendiente"
        self._costo_final = None
        self._fecha_creacion = datetime.now()

    @property
    def id_reserva(self) -> str:
        return self._id_reserva

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def costo_final(self):
        return self._costo_final

    def confirmar(self, **kwargs_costo) -> float:
        """Calcula el costo final y pasa la reserva a 'confirmada'.
        kwargs_costo se pasa tal cual a calcular_costo() del
        servicio, que es quien sabe qué parámetros acepta."""
        if self._estado != "pendiente":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado "
                f"'{self._estado}'."
            )
        costo = self._servicio.calcular_costo(self._duracion, **kwargs_costo)
        self._costo_final = costo
        self._estado = "confirmada"
        return costo

    def cancelar(self, motivo: str = "No especificado") -> None:
        if self._estado == "cancelada":
            raise OperacionNoPermitidaError(
                "La reserva ya se encuentra cancelada."
            )
        self._estado = "cancelada"
        self._motivo_cancelacion = motivo

    def procesar_pago(self) -> str:
        """Simula el pago de una reserva confirmada. Si el cálculo de
        la cuota falla por algún motivo (ej. ZeroDivisionError), se
        relanza como ReservaInvalidaError sin perder el error
        original (raise ... from error_original)."""
        if self._estado != "confirmada":
            raise OperacionNoPermitidaError(
                "Solo se puede procesar el pago de una reserva "
                "confirmada."
            )
        try:
            cuotas = 1
            valor_cuota = self._costo_final / cuotas
        except ZeroDivisionError as error_original:
            raise ReservaInvalidaError(
                "No fue posible calcular el valor de la cuota."
            ) from error_original
        else:
            return (f"Pago procesado: ${valor_cuota:.2f} en {cuotas} "
                    f"cuota(s) para la reserva {self._id_reserva}.")
        finally:
            self._ultimo_intento_pago = datetime.now()

    def __str__(self):
        return (f"Reserva[{self.id_reserva}] Cliente: "
                f"{self.cliente.nombre_cliente} | Servicio: "
                f"{self.servicio.nombre_servicio} | Estado: {self.estado} "
                f"| Costo: {self.costo_final}")
