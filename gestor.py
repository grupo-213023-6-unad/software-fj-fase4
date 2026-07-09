"""
gestor.py

GestorFJ es quien orquesta todo: mantiene listas en memoria de
clientes, servicios y reservas (nada de base de datos) y expone los
métodos para registrar, crear y consultar.

La idea en cada método público es simple: se intenta la operación, si
falla se captura la excepción puntual y se manda al log, y el
programa sigue corriendo pase lo que pase.
"""

from entidades import Cliente, Servicio
from reserva import Reserva
from excepciones import SoftwareFJError
from logger_config import obtener_logger


class GestorFJ:
    """Clientes, servicios y reservas de Software FJ, todo en listas
    internas."""

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        self._logger = obtener_logger()
        self._logger.info("Sistema Software FJ iniciado.")

    # ------------------------------------------------------------------
    # CLIENTES
    # ------------------------------------------------------------------
    def registrar_cliente(self, cliente: Cliente) -> bool:
        """True si el registro fue exitoso, False si falló (el error
        queda en el log pero el programa sigue)."""
        try:
            if any(c.documento == cliente.documento for c in self._clientes):
                raise SoftwareFJError(
                    f"Ya existe un cliente con documento "
                    f"{cliente.documento}."
                )
            self._clientes.append(cliente)
        except SoftwareFJError as error:
            self._logger.error(f"Error al registrar cliente: {error}")
            return False
        else:
            self._logger.info(
                f"Cliente registrado correctamente: "
                f"{cliente.mostrar_informacion()}"
            )
            return True
        finally:
            # Esto corre siempre, sirva o no el registro.
            self._logger.info(
                f"Intento de registro de cliente procesado "
                f"(documento intentado: {getattr(cliente, '_documento', '??')})."
            )

    def listar_clientes(self):
        return list(self._clientes)

    # ------------------------------------------------------------------
    # SERVICIOS
    # ------------------------------------------------------------------
    def registrar_servicio(self, servicio: Servicio) -> bool:
        try:
            if any(s.id_servicio == servicio.id_servicio
                   for s in self._servicios):
                raise SoftwareFJError(
                    f"Ya existe un servicio con id {servicio.id_servicio}."
                )
            self._servicios.append(servicio)
        except SoftwareFJError as error:
            self._logger.error(f"Error al registrar servicio: {error}")
            return False
        else:
            self._logger.info(
                f"Servicio registrado correctamente: {servicio.describir()}"
            )
            return True

    def listar_servicios(self):
        return list(self._servicios)

    def buscar_servicio(self, id_servicio: str):
        for servicio in self._servicios:
            if servicio.id_servicio == id_servicio:
                return servicio
        return None

    # ------------------------------------------------------------------
    # RESERVAS
    # ------------------------------------------------------------------
    def crear_reserva(self, id_reserva: str, cliente: Cliente,
                       servicio: Servicio, duracion: float,
                       **kwargs_costo):
        """Crea y confirma una reserva. Devuelve el objeto Reserva si
        todo salió bien, o None si algo falló (queda en el log)."""
        try:
            nueva_reserva = Reserva(id_reserva, cliente, servicio, duracion)
            nueva_reserva.confirmar(**kwargs_costo)
        except SoftwareFJError as error:
            self._logger.error(
                f"No se pudo crear/confirmar la reserva {id_reserva}: "
                f"{error}"
            )
            return None
        except Exception as error_inesperado:
            # Cualquier cosa no prevista también se registra, para que
            # el programa no se caiga por una excepción que no pensamos.
            self._logger.error(
                f"Error inesperado creando la reserva {id_reserva}: "
                f"{error_inesperado}"
            )
            return None
        else:
            self._reservas.append(nueva_reserva)
            self._logger.info(f"Reserva creada y confirmada: "
                               f"{nueva_reserva}")
            return nueva_reserva

    def cancelar_reserva(self, id_reserva: str, motivo: str) -> bool:
        reserva = self._buscar_reserva(id_reserva)
        if reserva is None:
            self._logger.error(
                f"No existe la reserva {id_reserva} para cancelar."
            )
            return False
        try:
            reserva.cancelar(motivo)
        except SoftwareFJError as error:
            self._logger.error(
                f"No se pudo cancelar la reserva {id_reserva}: {error}"
            )
            return False
        else:
            self._logger.info(f"Reserva {id_reserva} cancelada. "
                               f"Motivo: {motivo}")
            return True

    def _buscar_reserva(self, id_reserva: str):
        for reserva in self._reservas:
            if reserva.id_reserva == id_reserva:
                return reserva
        return None

    def listar_reservas(self):
        return list(self._reservas)
