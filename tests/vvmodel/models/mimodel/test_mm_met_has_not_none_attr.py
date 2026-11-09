from vvmodel.tests.models import MiTestModel as Model


def test_devuelve_false_si_no_existe_el_atributo_en_el_objeto(miobjeto):
    assert not miobjeto.has_not_none_attr('cuadrado')


def test_devuelve_true_si_el_atributo_existe_y_no_es_none(miobjeto):
    assert miobjeto.has_not_none_attr('nombre')


def test_devuelve_false_si_el_atributo_existe_y_es_none(miobjeto):
    miobjeto.cuadrado = None
    assert not miobjeto.has_not_none_attr('cuadrado')
