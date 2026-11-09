import pytest

from vvmodel.tests.models import MiTestPolymorphModel, MiTestPolymorphSubmodel


@pytest.fixture
def id(misubobjetopolimorfico):
    return misubobjetopolimorfico.pk


def test_tomar_devuelve_objeto_polimorfico(id):
    assert MiTestPolymorphModel.tomar(id=id).get_class() == MiTestPolymorphSubmodel


def test_con_polymorphic_false_devuelve_objeto_no_polimorfico(id):
    assert MiTestPolymorphModel.tomar(id=id, polymorphic=False).get_class() == MiTestPolymorphModel


def test_como_subclase_devuelve_objeto_como_instancia_del_submodelo(id):
    obj = MiTestPolymorphModel.tomar(id=id, polymorphic=False)
    assert obj.como_subclase().get_class() == MiTestPolymorphSubmodel


def test_save_guarda_app_en_campo_content_type():
    obj = MiTestPolymorphModel(nombre='objeto polimórfico no persistente', numero=3)
    obj.save()
    assert obj.content_type.app_label == 'tests'


def test_save_guarda_modelo_en_campo_content_type():
    obj = MiTestPolymorphModel(nombre='objeto polimórfico', numero=3)
    objsub = MiTestPolymorphSubmodel(nombre='subobjeto polimórfico', numero=4)

    obj.save()
    assert obj.content_type.model == 'mitestpolymorphmodel'

    objsub.save()
    assert objsub.content_type.model == 'mitestpolymorphsubmodel'


def test_actualizar_subclase_devuelve_el_mismo_objeto_actualizado_como_subclase(misubobjetopolimorfico):
    obj = MiTestPolymorphModel.tomar(id=misubobjetopolimorfico.pk, polymorphic=False)
    assert obj.actualizar_subclase().get_class() == MiTestPolymorphSubmodel
