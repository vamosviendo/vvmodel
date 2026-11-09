import datetime

import pytest

from vvmodel.tests.models import MiTestModel


def test_devuelve_true_si_hay_cambio_en_alguno_de_los_campos_dados(miobjetocomplejo):
    miobjetocomplejo.numero = miobjetocomplejo.numero + 2
    assert miobjetocomplejo.cambia_campo("numero", "nombre") is True


def test_devuelve_false_si_no_hay_cambio_en_ninguno_de_los_campos_dados(miobjetocomplejo):
    miobjetocomplejo.numero = miobjetocomplejo.numero + 2
    assert miobjetocomplejo.cambia_campo("nombre", "fecha") is False


def test_acepta_un_objeto_contra_el_cual_comparar(miobjetocomplejo):
    obj2 = MiTestModel(
        nombre="Otro nombre",
        numero=miobjetocomplejo.numero,
        fecha=miobjetocomplejo.fecha,
        related=miobjetocomplejo.related)
    assert miobjetocomplejo.cambia_campo("nombre", contraparte=obj2) is True
    assert miobjetocomplejo.cambia_campo("numero", "fecha", "related", contraparte=obj2) is False


def test_da_error_si_recibe_campo_inexistente(miobjetocomplejo):
    with pytest.raises(ValueError):
        miobjetocomplejo.cambia_campo("importe")


def test_devuelve_true_si_el_movimiento_es_nuevo(miobjeto):
    obj = MiTestModel(
        nombre="Objeto nuevo",
        numero=15,
        fecha=datetime.date(2025,11,12),
        related=miobjeto
    )
    for campo in [x.name for x in obj._meta.fields]:
        assert obj.cambia_campo(campo) is True
