"""Cálculo de envíos EnvíaYa. Política personalizada para el código 0182310057."""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Protocol

PMAX = 45.0
L1 = 3.0
L2 = 10.0
RECARGO_RURAL = 0.15
RECARGO_NACIONAL = 0.45
DESC_VIP = 0.10
DESC_FRECUENTE = 0.05
DESC_CUPON = 0.10
RECARGO_FINDE = 2000.0
PISO = 5000.0
TARIFA_TRAMO_1 = 6000.0
TARIFA_TRAMO_2 = 9000.0
TARIFA_KG_EXTRA = 800.0


class ZoneStrategy(Protocol):
    def apply(self, amount: float, weight: float) -> float: ...


@dataclass(frozen=True)
class StandardZone:
    rate: float

    def apply(self, amount: float, weight: float) -> float:
        return amount * (1 + self.rate)


ZONES = {
    "urbana": StandardZone(0.0),
    "rural": StandardZone(RECARGO_RURAL),
    "nacional": StandardZone(RECARGO_NACIONAL),
}
def validate(weight: float, zone: str, customer: str, day: int, coupon: str | None) -> None:
    if not isinstance(weight, (int, float)) or isinstance(weight, bool) or not 0 < weight <= PMAX:
        raise ValueError("peso inválido")
    if zone not in ZONES:
        raise ValueError("zona inválida")
    if customer not in {"normal", "frecuente", "vip"}:
        raise ValueError("cliente inválido")
    if not isinstance(day, int) or isinstance(day, bool) or not 1 <= day <= 7:
        raise ValueError("día inválido")
    if coupon is not None and coupon != "ENVIO10":
        raise ValueError("cupón inválido")


def base_tariff(weight: float) -> float:
    if weight <= L1:  # D=0, par: L1 incluido
        return TARIFA_TRAMO_1
    if weight <= L2:
        return TARIFA_TRAMO_2
    return TARIFA_TRAMO_2 + (weight - L2) * TARIFA_KG_EXTRA


def apply_customer_discount(amount: float, customer: str) -> float:
    rates = {"normal": 0.0, "frecuente": DESC_FRECUENTE, "vip": DESC_VIP}
    return amount * (1 - rates[customer])


def round_hundreds(amount: float) -> int:
    return int(Decimal(str(amount)).quantize(Decimal("1E2"), rounding=ROUND_HALF_UP))


def calc(weight: float, zone: str, customer: str, day: int, coupon: str | None = None) -> int:
    """Devuelve el costo final; día 6/7 es fin de semana. Solicitud asignada: cambio 1."""
    validate(weight, zone, customer, day, coupon)
    amount = base_tariff(weight)

    amount = ZONES[zone].apply(amount, weight)

    # E=5, impar: el recargo de fin de semana se suma después de descuentos.
    amount = apply_customer_discount(amount, customer)
    if coupon == "ENVIO10":  # B=1, impar: descuentos acumulados, cliente y luego cupón.
        amount *= 1 - DESC_CUPON
    if day in (6, 7):
        amount += RECARGO_FINDE

    amount = max(amount, PISO)
    return round_hundreds(amount)
