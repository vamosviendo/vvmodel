from vvmodel.tests.models import MiTestModel as Model


def test_devuelve_longitud_maxima_de_charfield():
    assert Model.get_max_length('nombre') == 50
