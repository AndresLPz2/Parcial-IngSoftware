"""Cálculo de envíos EnvíaYa, personalizado para el código 0182310057."""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Protocol

PESO_MAXIMO = 45.0
LIMITE_1 = 3.0
LIMITE_2 = 10.0
RECARGO_RURAL = 0.15
RECARGO_NACIONAL = 0.45
DESCUENTO_VIP = 0.10
DESCUENTO_FRECUENTE = 0.05
DESCUENTO_CUPON = 0.10
DESCUENTO_EMPRESARIAL = 0.12
RECARGO_FIN_DE_SEMANA = 2000.0
PISO_COBRO = 5000.0
TARIFA_TRAMO_1 = 6000.0
TARIFA_TRAMO_2 = 9000.0
TARIFA_KILO_ADICIONAL = 800.0


class EstrategiaZona(Protocol):
    def aplicar(self, importe: float, peso: float) -> float: ...


@dataclass(frozen=True)
class ZonaEstandar:
    tasa: float

    def aplicar(self, importe: float, peso: float) -> float:
        return importe * (1 + self.tasa)


@dataclass(frozen=True)
class ZonaEmpresarial:
    tasa: float

    def aplicar(self, importe: float, peso: float) -> float:
        return importe if peso > LIMITE_2 else importe * (1 + self.tasa)


ZONAS = {
    "urbana": ZonaEstandar(0.0),
    "rural": ZonaEstandar(RECARGO_RURAL),
    "nacional": ZonaEstandar(RECARGO_NACIONAL),
}
ZONAS_EMPRESARIALES = {
    "urbana": ZonaEmpresarial(0.0),
    "rural": ZonaEmpresarial(RECARGO_RURAL),
    "nacional": ZonaEmpresarial(RECARGO_NACIONAL),
}


def validar(peso: float, zona: str, cliente: str, dia: int, cupon: str | None) -> None:
    if not isinstance(peso, (int, float)) or isinstance(peso, bool) or not 0 < peso <= PESO_MAXIMO:
        raise ValueError("peso inválido")
    if zona not in ZONAS:
        raise ValueError("zona inválida")
    if cliente not in {"normal", "frecuente", "vip", "empresarial"}:
        raise ValueError("cliente inválido")
    if not isinstance(dia, int) or isinstance(dia, bool) or not 1 <= dia <= 7:
        raise ValueError("día inválido")
    if cupon is not None and cupon != "ENVIO10":
        raise ValueError("cupón inválido")


def calcular_tarifa_base(peso: float) -> float:
    if peso <= LIMITE_1:  # D=0 es par: el límite 1 se incluye.
        return TARIFA_TRAMO_1
    if peso <= LIMITE_2:
        return TARIFA_TRAMO_2
    return TARIFA_TRAMO_2 + (peso - LIMITE_2) * TARIFA_KILO_ADICIONAL


def aplicar_descuento_cliente(importe: float, cliente: str) -> float:
    tasas = {
        "normal": 0.0,
        "frecuente": DESCUENTO_FRECUENTE,
        "vip": DESCUENTO_VIP,
        "empresarial": DESCUENTO_EMPRESARIAL,
    }
    return importe * (1 - tasas[cliente])


def redondear_a_centenas(importe: float) -> int:
    return int(Decimal(str(importe)).quantize(Decimal("1E2"), rounding=ROUND_HALF_UP))


def calc(peso: float, zona: str, cliente: str, dia: int, cupon: str | None = None) -> int:
    """Calcula el costo final; sábado y domingo corresponden a los días 6 y 7."""
    validar(peso, zona, cliente, dia, cupon)
    importe = calcular_tarifa_base(peso)

    estrategias = ZONAS_EMPRESARIALES if cliente == "empresarial" else ZONAS
    importe = estrategias[zona].aplicar(importe, peso)
    importe = aplicar_descuento_cliente(importe, cliente)

    if cupon == "ENVIO10":  # B=1 es impar: se aplican ambos descuentos en orden.
        importe *= 1 - DESCUENTO_CUPON
    if dia in (6, 7):  # E=5 es impar: el recargo se suma después de los descuentos.
        importe += RECARGO_FIN_DE_SEMANA

    importe = max(importe, PISO_COBRO)
    return redondear_a_centenas(importe)
