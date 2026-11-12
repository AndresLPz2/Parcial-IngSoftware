"""Pruebas de contrato que exhiben defectos de la etiqueta v1.0.0."""
import inspect

import pytest

from envios_legacy_v1 import calc


@pytest.mark.xfail(reason="DEF-01: legado usa 50 en vez de PMAX=45")
def test_TLEG_01_rechaza_peso_mayor_a_pmax():
    with pytest.raises(ValueError):
        calc(46, "urbana", "normal", 1)


@pytest.mark.xfail(reason="DEF-02: legado omite validaciones de zona y día")
@pytest.mark.parametrize("zone,day", [
    pytest.param("desconocida", 1, id="TLEG-02-zona"),
    pytest.param("urbana", 0, id="TLEG-03-dia"),
])
def test_TLEG_02_03_rechaza_zona_o_dia_invalidos(zone, day):
    with pytest.raises(ValueError):
        calc(4, zone, "normal", day)


@pytest.mark.xfail(reason="DEF-03: d>6 omite el sábado")
def test_TLEG_04_sabado_cobra_recargo():
    assert calc(4, "urbana", "normal", 6) == 11000


@pytest.mark.xfail(reason="DEF-04: el recargo de fin de semana se descuenta")
def test_TLEG_05_aplica_recargo_despues_del_descuento_vip():
    assert calc(4, "urbana", "vip", 7) == 10100


@pytest.mark.xfail(reason="DEF-05: cupón desconocido se ignora, F es impar")
def test_TLEG_06_rechaza_cupon_desconocido():
    with pytest.raises(ValueError):
        calc(4, "urbana", "normal", 1, "OTRO")


@pytest.mark.xfail(reason="DEF-06: legado trunca en lugar de redondear half-up")
def test_TLEG_07_redondea_empate_de_cincuenta_hacia_arriba():
    assert calc(4, "rural", "normal", 1) == 10400


@pytest.mark.xfail(reason="DEF-07: legado no valida el tipo de cliente")
def test_TLEG_08_rechaza_cliente_desconocido():
    with pytest.raises(ValueError):
        calc(4, "urbana", "ocasional", 1)


@pytest.mark.xfail(reason="DEF-08: la interfaz heredada incluye flag")
def test_TLEG_09_api_no_expone_flag():
    assert "flag" not in inspect.signature(calc).parameters
