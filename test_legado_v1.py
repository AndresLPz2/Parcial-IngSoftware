"""Pruebas de contrato que exhiben defectos de la versión v1.0.0."""
import inspect

import pytest

from envios_legado_v1 import calc


@pytest.mark.xfail(reason="DEF-01: el legado usa 50 en lugar del peso máximo 45")
def test_probar_PLEG_01_rechazo_de_peso_sobre_el_maximo():
    with pytest.raises(ValueError):
        calc(46, "urbana", "normal", 1)


@pytest.mark.xfail(reason="DEF-02: el legado no valida la zona ni el día")
@pytest.mark.parametrize("zona,dia", [
    pytest.param("desconocida", 1, id="PLEG-02-zona"),
    pytest.param("urbana", 0, id="PLEG-03-dia"),
])
def test_probar_PLEG_02_03_rechazo_de_zona_o_dia_invalidos(zona, dia):
    with pytest.raises(ValueError):
        calc(4, zona, "normal", dia)


@pytest.mark.xfail(reason="DEF-03: la condición día>6 omite el sábado")
def test_probar_PLEG_04_recargo_del_sabado():
    assert calc(4, "urbana", "normal", 6) == 11000


@pytest.mark.xfail(reason="DEF-04: el descuento también reduce el recargo de fin de semana")
def test_probar_PLEG_05_recargo_despues_del_descuento_vip():
    assert calc(4, "urbana", "vip", 7) == 10100


@pytest.mark.xfail(reason="DEF-05: el cupón desconocido se ignora aunque F sea impar")
def test_probar_PLEG_06_rechazo_de_cupon_desconocido():
    with pytest.raises(ValueError):
        calc(4, "urbana", "normal", 1, "OTRO")


@pytest.mark.xfail(reason="DEF-06: el legado trunca en lugar de redondear mitades hacia arriba")
def test_probar_PLEG_07_redondeo_de_empate_hacia_arriba():
    assert calc(4, "rural", "normal", 1) == 10400


@pytest.mark.xfail(reason="DEF-07: el legado no valida el tipo de cliente")
def test_probar_PLEG_08_rechazo_de_cliente_desconocido():
    with pytest.raises(ValueError):
        calc(4, "urbana", "ocasional", 1)


@pytest.mark.xfail(reason="DEF-08: la interfaz heredada incluye el parámetro flag")
def test_probar_PLEG_09_interfaz_sin_parametro_flag():
    assert "flag" not in inspect.signature(calc).parameters
