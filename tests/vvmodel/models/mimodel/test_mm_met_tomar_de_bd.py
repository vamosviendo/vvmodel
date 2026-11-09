from vvmodel.tests.models import MiTestRelatedModel as Model


def test_devuelve_la_version_persistente_de_un_objeto(miobjeto):
    obj_guardado = Model.tomar(nombre = miobjeto.nombre)
    miobjeto.nombre = 'objeto modificado no persistente'
    assert miobjeto.tomar_de_bd() == obj_guardado


def test_si_no_hay_version_persistente_de_un_objeto_devuelve_none():
    objeto = Model(nombre = 'objeto no persistente')
    assert objeto.tomar_de_bd() is None
