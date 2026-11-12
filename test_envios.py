import pytest

from envios import calc


@pytest.mark.parametrize("weight,zone,customer,day,coupon,expected", [
    (1, "urbana", "normal", 1, None, 6000),       # tramo 1
    (3, "urbana", "normal", 1, None, 6000),       # L1 incluido (D par)
    (3.001, "urbana", "normal", 1, None, 9000),   # sobre L1
    (10, "urbana", "normal", 1, None, 9000),      # L2
    (10.01, "urbana", "normal", 1, None, 9000),   # proporcional: 9008 -> 9000
    (45, "urbana", "normal", 1, None, 37000),     # PMAX
    (4, "rural", "normal", 1, None, 10400),       # rural 15%, empate hacia arriba
    (4, "nacional", "normal", 1, None, 13100),    # nacional 45%
    (4, "urbana", "frecuente", 1, None, 8600),   # 5%
    (4, "urbana", "vip", 1, None, 8100),         # 10%
    (4, "urbana", "vip", 1, "ENVIO10", 7300),   # acumulados B impar
    (1, "urbana", "vip", 1, "ENVIO10", 5000),   # piso tras descuentos
    (4, "urbana", "normal", 6, None, 11000),      # sábado, E impar: +2000 final
    (4, "urbana", "vip", 7, None, 10100),        # domingo, descuento luego finde
    (4, "urbana", "normal", 5, None, 9000),       # viernes
    (11, "rural", "empresarial", 2, None, 8600), # >L2: zona exenta; 8624->8600
    (10, "rural", "empresarial", 2, None, 9100), # =L2: zona no exenta
    (4, "rural", "empresarial", 2, "ENVIO10", 8200),
    (0, "urbana", "normal", 1, None, ValueError),
    (45.001, "urbana", "normal", 1, None, ValueError),
    (1, "isla", "normal", 1, None, ValueError),
    (1, "urbana", "ocasional", 1, None, ValueError),
    (1, "urbana", "normal", 0, None, ValueError),
    (1, "urbana", "vip", 1, "OTRO", ValueError), # F impar: desconocido es error
    (1, "urbana", "vip", 1, None, 5400),
])
def test_calc_cases(weight, zone, customer, day, coupon, expected):
    if expected is ValueError:
        with pytest.raises(ValueError):
            calc(weight, zone, customer, day, coupon)
    else:
        assert calc(weight, zone, customer, day, coupon) == expected


@pytest.mark.parametrize("day", [1, 2, 3, 4, 5, 6, 7])
def test_all_valid_days(day):
    assert isinstance(calc(4, "urbana", "normal", day), int)
