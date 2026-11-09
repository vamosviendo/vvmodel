import pytest

from datetime import date

from vvmodel.tests.models import MiTestModel


def test_actualiza_objeto_existente_a_partir_de_objeto_del_mismo_tipo(
        miobjetocomplejo, miobjetonopersistente, miotroobjeto):
    miobjetocomplejo.update_from(miobjetonopersistente)
    miobjetocomplejo.refresh_from_db()

    assert miobjetocomplejo.nombre == 'nuevo nombre'
    assert miobjetocomplejo.numero == 567
    assert miobjetocomplejo.fecha == date(2020, 2, 2)
    assert miobjetocomplejo.related == miotroobjeto


def test_con_commit_false_no_guarda_objeto_actualizado(miobjetocomplejo, miobjetonopersistente):
    nombre = miobjetocomplejo.nombre
    numero = miobjetocomplejo.numero
    fecha = miobjetocomplejo.fecha
    related = miobjetocomplejo.related

    miobjetocomplejo.update_from(miobjetonopersistente, commit=False)
    miobjetocomplejo.refresh_from_db()

    assert miobjetocomplejo.nombre == nombre
    assert miobjetocomplejo.numero == numero
    assert miobjetocomplejo.fecha == fecha
    assert miobjetocomplejo.related == related


def test_con_commit_false_actualiza_objeto_aunque_no_lo_guarde(miobjetocomplejo, miobjetonopersistente):
    miobjetocomplejo.update_from(miobjetonopersistente, commit=False)

    assert miobjetocomplejo.nombre == miobjetonopersistente.nombre
    assert miobjetocomplejo.numero == miobjetonopersistente.numero
    assert miobjetocomplejo.fecha == miobjetonopersistente.fecha
    assert miobjetocomplejo.related == miobjetonopersistente.related


def test_si_se_usa_con_un_objeto_incompleto_actualiza_solo_los_campos_del_objeto(miobjetocomplejo):
    otroobjetocomplejo = MiTestModel(nombre='objeto incompleto')
    numero = miobjetocomplejo.numero
    related = miobjetocomplejo.related

    miobjetocomplejo.update_from(otroobjetocomplejo)
    miobjetocomplejo.refresh_from_db()

    assert miobjetocomplejo.nombre == 'objeto incompleto'
    assert miobjetocomplejo.numero == numero
    assert miobjetocomplejo.related == related


def test_devuelve_objeto_actualizado(miobjetocomplejo, miobjetonopersistente):
    objeto_actualizado = miobjetocomplejo.update_from(miobjetonopersistente, commit=False)

    assert objeto_actualizado.nombre == miobjetonopersistente.nombre
    assert objeto_actualizado.numero == miobjetonopersistente.numero
    assert objeto_actualizado.fecha == miobjetonopersistente.fecha
    assert objeto_actualizado.related == miobjetonopersistente.related
