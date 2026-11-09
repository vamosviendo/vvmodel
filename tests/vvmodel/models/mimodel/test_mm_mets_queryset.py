from django.db.models import QuerySet

from vvmodel.tests.models import (
    MiTestRelatedModel as Model,
    MiTestModel as ComplexModel,
)


def test_todes_devuelve_todos_los_objetos(misobjetos):
    assert list(Model.todes()) == list(Model.objects.all())


def test_primere_devuelve_primer_objeto(misobjetos):
    assert Model.primere() == misobjetos[0]


def test_ultime_devuelve_ultimo_objeto(misobjetos):
    assert Model.ultime() == misobjetos[-1]


def test_tomar_devuelve_objeto_indicado(miobjeto, miotroobjeto):
    assert Model.tomar(nombre='miotroobjeto') == miotroobjeto


def test_cantidad_devuelve_cantidad_de_objetos(misobjetos):
    assert Model.cantidad() == len(misobjetos)


def test_excepto_devuelve_todos_los_objetos_excepto_el_indicado(misobjetos):
    assert list(Model.excepto(pk=misobjetos[1].pk)) == [misobjetos[0], misobjetos[2]]


def test_filtro_devuelve_todos_los_objetos_que_coincidan(misobjetoscomplejos):
    assert tuple(ComplexModel.filtro(numero=5.0)) == misobjetoscomplejos[0:2]