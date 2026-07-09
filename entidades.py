"""
entidades.py

Clases del dominio de Software FJ:

    EntidadBase (abstracta) -> Cliente
    Servicio (abstracta)    -> ReservaSala, AlquilerEquipo, AsesoriaEspecializada

EntidadBase y Servicio son ABC porque no tiene sentido crear un objeto
"entidad" o "servicio" genérico, siempre es alguna de sus subclases.
Cliente hereda de EntidadBase; los tres tipos de servicio heredan de
Servicio y cada uno calcula su costo a su manera (ahí está el
polimorfismo). Los atributos van con doble guion bajo y se accede a
ellos por @property, validando antes de guardar cualquier valor.
"""

from abc import ABC, abstractmethod
from excepciones import (
    DatosInvalidosError,
    ParametroFaltanteError,
    CalculoInconsistenteError,
)


class EntidadBase(ABC):
    """Cualquier "cosa" del sistema que tenga id y nombre. No se
    instancia directo: las hijas deben implementar mostrar_informacion()."""

    def __init__(self, id_entidad: str, nombre: str):
        self._id_entidad = id_entidad
        self._nombre = nombre

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @property
    def nombre(self) -> str:
        return self._nombre

    @abstractmethod
    def mostrar_informacion(self) -> str:
        raise NotImplementedError


class Cliente(EntidadBase):
    """Un cliente de Software FJ. Documento, correo y teléfono se
    validan en el setter de cada @property, así que si algo viene mal
    formado se lanza DatosInvalidosError antes de guardar basura."""

    def __init__(self, id_entidad: str, nombre: str, documento: str,
                 correo: str, telefono: str):
        super().__init__(id_entidad, nombre)
        # Pasamos por los setters para que la validación corra también
        # al construir el objeto.
        self.nombre_cliente = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---------- nombre ----------
    @property
    def nombre_cliente(self) -> str:
        return self._nombre

    @nombre_cliente.setter
    def nombre_cliente(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError(
                "El nombre del cliente no puede estar vacío."
            )
        if any(caracter.isdigit() for caracter in valor):
            raise DatosInvalidosError(
                "El nombre del cliente no puede contener números."
            )
        self._nombre = valor.strip()

    # ---------- documento ----------
    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor: str):
        if not valor or not str(valor).isdigit():
            raise DatosInvalidosError(
                "El documento debe contener solo números y no puede "
                "estar vacío."
            )
        if len(str(valor)) < 6:
            raise DatosInvalidosError(
                "El documento debe tener al menos 6 dígitos."
            )
        self._documento = str(valor)

    # ---------- correo ----------
    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            raise DatosInvalidosError(
                f"El correo '{valor}' no tiene un formato válido."
            )
        self._correo = valor.strip().lower()

    # ---------- teléfono ----------
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not str(valor).isdigit():
            raise DatosInvalidosError(
                "El teléfono debe contener solo números."
            )
        if len(str(valor)) < 7:
            raise DatosInvalidosError(
                "El teléfono debe tener al menos 7 dígitos."
            )
        self._telefono = str(valor)

    def mostrar_informacion(self) -> str:
        return (f"Cliente[{self.id_entidad}] {self.nombre_cliente} | "
                f"Doc: {self.documento} | Correo: {self.correo} | "
                f"Tel: {self.telefono}")


class Servicio(ABC):
    """Contrato que debe cumplir cualquier servicio: calcular_costo()
    (cada uno lo hace distinto), describir() y validar_parametros()."""

    def __init__(self, id_servicio: str, nombre_servicio: str,
                 costo_base: float, disponible: bool = True):
        if costo_base is None:
            raise ParametroFaltanteError(
                "Debe indicar el costo_base del servicio."
            )
        if costo_base <= 0:
            raise DatosInvalidosError(
                "El costo base del servicio debe ser mayor a cero."
            )
        self._id_servicio = id_servicio
        self._nombre_servicio = nombre_servicio
        self._costo_base = costo_base
        self._disponible = disponible

    @property
    def id_servicio(self) -> str:
        return self._id_servicio

    @property
    def nombre_servicio(self) -> str:
        return self._nombre_servicio

    @property
    def costo_base(self) -> float:
        return self._costo_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        self._disponible = bool(valor)

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """*args/**kwargs porque cada servicio recibe parámetros
        distintos (horas, días, impuesto, descuento...)."""
        raise NotImplementedError

    @abstractmethod
    def describir(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self, **kwargs) -> None:
        raise NotImplementedError


class ReservaSala(Servicio):
    """Reserva de salas de reuniones."""

    def __init__(self, id_servicio: str, nombre_servicio: str,
                 costo_base: float, capacidad: int, disponible: bool = True):
        super().__init__(id_servicio, nombre_servicio, costo_base, disponible)
        if capacidad is None or capacidad <= 0:
            raise DatosInvalidosError(
                "La capacidad de la sala debe ser mayor a cero."
            )
        self._capacidad = capacidad

    @property
    def capacidad(self) -> int:
        return self._capacidad

    def validar_parametros(self, **kwargs) -> None:
        horas = kwargs.get("horas")
        if horas is None:
            raise ParametroFaltanteError(
                "Debe indicar 'horas' para reservar la sala."
            )
        if horas <= 0:
            raise DatosInvalidosError("Las horas deben ser mayores a cero.")

    def calcular_costo(self, horas: float, impuesto: float = 0.0,
                        descuento: float = 0.0) -> float:
        """costo_base * horas, más impuesto, menos descuento. Se
        puede llamar solo con horas, o agregando impuesto y/o
        descuento (los tres son opcionales menos horas)."""
        self.validar_parametros(horas=horas)
        if not (0 <= impuesto <= 1) or not (0 <= descuento <= 1):
            raise CalculoInconsistenteError(
                "El impuesto o el descuento deben estar entre 0 y 1 "
                "(0% - 100%)."
            )
        costo = self.costo_base * horas
        costo = costo + (costo * impuesto) - (costo * descuento)
        if costo < 0:
            raise DatosInvalidosError(
                "El costo calculado no puede ser negativo."
            )
        return round(costo, 2)

    def describir(self) -> str:
        return (f"Reserva de Sala '{self.nombre_servicio}' "
                f"(capacidad: {self.capacidad} personas) - "
                f"Costo base por hora: ${self.costo_base}")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: proyectores, computadores, etc."""

    def __init__(self, id_servicio: str, nombre_servicio: str,
                 costo_base: float, tipo_equipo: str, disponible: bool = True):
        super().__init__(id_servicio, nombre_servicio, costo_base, disponible)
        if not tipo_equipo or not tipo_equipo.strip():
            raise DatosInvalidosError("Debe indicar el tipo de equipo.")
        self._tipo_equipo = tipo_equipo

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    def validar_parametros(self, **kwargs) -> None:
        dias = kwargs.get("dias")
        if dias is None:
            raise ParametroFaltanteError(
                "Debe indicar 'dias' para alquilar el equipo."
            )
        if dias <= 0:
            raise DatosInvalidosError("Los días deben ser mayores a cero.")

    def calcular_costo(self, dias: int, impuesto: float = 0.0) -> float:
        """costo_base * dias, más impuesto."""
        self.validar_parametros(dias=dias)
        if not (0 <= impuesto <= 1):
            raise CalculoInconsistenteError(
                "El impuesto debe estar entre 0 y 1 (0% - 100%)."
            )
        costo = self.costo_base * dias
        costo += costo * impuesto
        return round(costo, 2)

    def describir(self) -> str:
        return (f"Alquiler de Equipo '{self.nombre_servicio}' "
                f"(tipo: {self.tipo_equipo}) - "
                f"Costo base por día: ${self.costo_base}")


class AsesoriaEspecializada(Servicio):
    """Asesorías / consultorías especializadas."""

    def __init__(self, id_servicio: str, nombre_servicio: str,
                 costo_base: float, area_experticia: str,
                 disponible: bool = True):
        super().__init__(id_servicio, nombre_servicio, costo_base, disponible)
        if not area_experticia or not area_experticia.strip():
            raise DatosInvalidosError("Debe indicar el área de experticia.")
        self._area_experticia = area_experticia

    @property
    def area_experticia(self) -> str:
        return self._area_experticia

    def validar_parametros(self, **kwargs) -> None:
        horas = kwargs.get("horas")
        if horas is None:
            raise ParametroFaltanteError(
                "Debe indicar 'horas' para la asesoría."
            )
        if horas <= 0:
            raise DatosInvalidosError("Las horas deben ser mayores a cero.")

    def calcular_costo(self, horas: float, descuento: float = 0.0) -> float:
        """costo_base * horas, menos descuento."""
        self.validar_parametros(horas=horas)
        if not (0 <= descuento <= 1):
            raise CalculoInconsistenteError(
                "El descuento debe estar entre 0 y 1 (0% - 100%)."
            )
        costo = self.costo_base * horas
        costo -= costo * descuento
        if costo < 0:
            raise DatosInvalidosError(
                "El costo calculado no puede ser negativo."
            )
        return round(costo, 2)

    def describir(self) -> str:
        return (f"Asesoría Especializada '{self.nombre_servicio}' "
                f"(área: {self.area_experticia}) - "
                f"Costo base por hora: ${self.costo_base}")
