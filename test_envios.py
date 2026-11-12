import pytest

from envios import calc


@pytest.mark.parametrize("peso,zona,cliente,dia,cupon,esperado", [
    (1, "urbana", "normal", 1, None, 6000),       # Tramo 1.
    (3, "urbana", "normal", 1, None, 6000),       # Límite 1 incluido (D par).
    (3.001, "urbana", "normal", 1, None, 9000),   # Justo sobre el límite 1.
    (10, "urbana", "normal", 1, None, 9000),      # Límite 2.
    (10.01, "urbana", "normal", 1, None, 9000),   # 9008 se redondea a 9000.
    (45, "urbana", "normal", 1, None, 37000),     # Peso máximo permitido.
    (4, "rural", "normal", 1, None, 10400),       # 15%; empate hacia arriba.
    (4, "nacional", "normal", 1, None, 13100),    # Recargo nacional 45%.
    (4, "urbana", "frecuente", 1, None, 8600),   # Descuento frecuente 5%.
    (4, "urbana", "vip", 1, None, 8100),         # Descuento VIP 10%.
    (4, "urbana", "vip", 1, "ENVIO10", 7300),   # Descuentos acumulados (B impar).
    (1, "urbana", "vip", 1, "ENVIO10", 5000),   # Piso después de descuentos.
    (4, "urbana", "normal", 6, None, 11000),      # Sábado: suma $2.000 al final.
    (4, "urbana", "vip", 7, None, 10100),        # Domingo: descuento y luego recargo.
    (4, "urbana", "normal", 5, None, 9000),       # Viernes sin recargo.
    (11, "rural", "empresarial", 2, None, 8600), # Sobre L2: zona exenta.
    (10, "rural", "empresarial", 2, None, 9100), # En L2: zona no exenta.
    (4, "rural", "empresarial", 2, "ENVIO10", 8200),
    (0, "urbana", "normal", 1, None, ValueError),
    (45.001, "urbana", "normal", 1, None, ValueError),
    (1, "isla", "normal", 1, None, ValueError),
    (1, "urbana", "ocasional", 1, None, ValueError),
    (1, "urbana", "normal", 0, None, ValueError),
    (1, "urbana", "vip", 1, "OTRO", ValueError), # F impar: cupón desconocido es error.
    (1, "urbana", "vip", 1, None, 5400),
])
def test_probar_casos_de_calculo(peso, zona, cliente, dia, cupon, esperado):
    if esperado is ValueError:
        with pytest.raises(ValueError):
            calc(peso, zona, cliente, dia, cupon)
    else:
        assert calc(peso, zona, cliente, dia, cupon) == esperado


@pytest.mark.parametrize("dia", [1, 2, 3, 4, 5, 6, 7])
def test_probar_todos_los_dias_validos(dia):
    assert isinstance(calc(4, "urbana", "normal", dia), int)
