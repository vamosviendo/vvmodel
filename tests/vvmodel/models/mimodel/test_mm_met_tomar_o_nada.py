from vvmodel.tests.models import MiTestRelatedModel as Model


def test_devuelve_objeto_si_existe(miobjeto):
    assert Model.tomar_o_nada(nombre=miobjeto.nombre) == miobjeto


def test_devuelve_none_si_objeto_no_existe():
    assert Model.tomar_o_nada(nombre='objeto inexistente') is None
