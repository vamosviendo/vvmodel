from vvmodel.tests.models import MiTestPolymorphModel, MiTestPolymorphSubmodel


def test_devuelve_true_para_el_mismo_objeto_tomado_como_clases_distintas(misubobjetopolimorfico):
    obj = MiTestPolymorphModel.tomar(numero=misubobjetopolimorfico.numero)
    obj_sub = MiTestPolymorphSubmodel.tomar(numero=misubobjetopolimorfico.numero)

    assert obj.es_le_misme_que(obj_sub)
    assert obj_sub.es_le_misme_que(obj)


def test_devuelve_false_para_objetos_distintos_tomados_como_clases_distintas(
        miobjetopolimorfico, misubobjetopolimorfico):
    assert not miobjetopolimorfico.es_le_misme_que(misubobjetopolimorfico)
    assert not misubobjetopolimorfico.es_le_misme_que(miobjetopolimorfico)


def test_devuelve_false_para_objetos_distintos_tomados_como_la_misma_clase(
        miobjetopolimorfico, misubobjetopolimorfico):
    obj1 = MiTestPolymorphModel.tomar(numero=miobjetopolimorfico.numero)
    obj2 = MiTestPolymorphModel.tomar(numero=misubobjetopolimorfico.numero)

    assert not obj1.es_le_misme_que(obj2)
    assert not obj2.es_le_misme_que(obj1)


def test_devuelve_false_si_uno_de_los_objetos_no_esta_en_la_base_de_datos(
        miobjetopolimorfico):
    obj = MiTestPolymorphModel(
        nombre=miobjetopolimorfico.nombre,
        numero=miobjetopolimorfico.numero,
    )

    assert not miobjetopolimorfico.es_le_misme_que(obj)
