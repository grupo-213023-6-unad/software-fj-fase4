"""
excepciones.py

Excepciones propias del sistema. Las creamos en vez de usar solo
ValueError/TypeError de Python porque así podemos capturar justo lo
que nos interesa (con except SoftwareFJError) y dar mensajes que
tengan sentido para el negocio, no genéricos.

Todas cuelgan de SoftwareFJError.
"""


class SoftwareFJError(Exception):
    """Excepción base. De aquí heredan todas las demás."""
    pass


class DatosInvalidosError(SoftwareFJError):
    """Un dato no cumple las reglas del negocio (nombre vacío, correo
    sin arroba, documento con letras, etc.)."""
    pass


class ParametroFaltanteError(SoftwareFJError):
    """Falta un parámetro obligatorio, por ejemplo crear un servicio
    sin costo_base."""
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    """Se intenta algo que el estado actual del objeto no permite,
    como cancelar una reserva que ya está cancelada."""
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Los datos de una reserva no cuadran (duración <= 0, cliente o
    servicio inválido, etc.)."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio que se quiere reservar no está disponible."""
    pass


class CalculoInconsistenteError(SoftwareFJError):
    """El resultado de un cálculo de costos no tiene sentido: costo
    negativo, descuento mayor al 100%, etc."""
    pass
