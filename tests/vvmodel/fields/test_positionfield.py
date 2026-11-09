import pytest

from vvmodel.tests.models import \
    MiTestModelConPositionField, \
    MiTestModelConPositionFieldColectorOrdenado, \
    MiTestModelConDoblePositionField, \
    ModeloErroneo


# Fixtures

@pytest.fixture
def objeto_ordenado():
    return MiTestModelConPositionField.crear(nombre="objeto ordenado", tipo="tipo1")


@pytest.fixture
def otro_objeto_ordenado():
    return MiTestModelConPositionField.crear(nombre="otro objeto ordenado", tipo="tipo1")


@pytest.fixture
def tercer_objeto_ordenado():
    return MiTestModelConPositionField.crear(nombre="tercer objeto ordenado", tipo="tipo1")


@pytest.fixture
def cuarto_objeto_ordenado():
    return MiTestModelConPositionField.crear(nombre="cuarto objeto ordenado", tipo="tipo1")


@pytest.fixture
def quinto_objeto_ordenado():
    return MiTestModelConPositionField.crear(nombre="quinto objeto ordenado", tipo="tipo1")


@pytest.fixture
def objeto_de_otra_coleccion():
    return MiTestModelConPositionField.crear(nombre="objeto de_otra_colecion", tipo="otrotipo")


@pytest.fixture
def otro_objeto_de_otra_coleccion():
    return MiTestModelConPositionField.crear(nombre="otro_objeto de_otra_colecion", tipo="otrotipo")


@pytest.fixture
def objeto_ordenado_colector_ordenado():
    return MiTestModelConPositionFieldColectorOrdenado.crear(
        nombre="objeto ordenado colector ordenado",
        tipo="tipo1"
    )


@pytest.fixture
def otro_objeto_ordenado_colector_ordenado():
    return MiTestModelConPositionFieldColectorOrdenado.crear(
        nombre="otro objeto ordenado colector ordenado",
        tipo="tipo1"
    )


@pytest.fixture
def objeto_ordenado_colector_ordenado_otra_coleccion():
    return MiTestModelConPositionFieldColectorOrdenado.crear(
        nombre="objeto ordenado colector ordenado otra colección",
        tipo="tipo2"
    )


@pytest.fixture
def objeto_ordenado_colector_ordenado_coleccion_anterior():
    return MiTestModelConPositionFieldColectorOrdenado.crear(
        nombre="objeto ordenado colector ordenado colección anterior",
        tipo="tipo0"
    )


# Tests

def test_se_genera_automaticamente():
    obj = MiTestModelConPositionField.crear(nombre="obj", tipo="tipo1")
    assert obj.posicion is not None
def test_primer_objeto_de_una_coleccion_tiene_posicion_cero():
    obj = MiTestModelConPositionField.crear(nombre="obj", tipo="tipo1")
    assert obj.posicion == 0


def test_segundo_objeto_de_una_coleccion_tiene_posicion_1(objeto_ordenado):
    obj = MiTestModelConPositionField.crear(nombre="tercer objeto ordenado", tipo="tipo1")
    assert obj.posicion == 1


def test_nuevo_objeto_de_una_coleccion_tiene_posicion_siguiente_a_la_ultima(objeto_ordenado, otro_objeto_ordenado):
    obj = MiTestModelConPositionField.crear(nombre="tercer objeto ordenado", tipo="tipo1")
    assert obj.posicion == 2


def test_nuevo_objeto_de_otra_coleccion_tiene_posicion_cero(objeto_ordenado, otro_objeto_ordenado):
    obj = MiTestModelConPositionField.crear(nombre="objeto ordenado de otra coleccion", tipo="tipo2")
    assert obj.posicion == 0

def test_si_se_crea_objeto_con_posicion_existente_objetos_de_posicion_mas_alta_suben_de_posicion(
        objeto_ordenado, otro_objeto_ordenado, tercer_objeto_ordenado):
    MiTestModelConPositionField.crear(
        nombre="objeto con posicion existente",
        tipo=objeto_ordenado.tipo,
        posicion=1
    )
    otro_objeto_ordenado.refresh_from_db()
    assert otro_objeto_ordenado.posicion == 2

    tercer_objeto_ordenado.refresh_from_db()
    assert tercer_objeto_ordenado.posicion == 3

def test_si_se_crea_objeto_con_posicion_demasiado_alta_se_ajusta_a_la_ultima_posicion_de_la_coleccion_mas_uno(
        objeto_ordenado, otro_objeto_ordenado):
    obj = MiTestModelConPositionField.crear(
        nombre="objeto con posicion demasiado alta",
        tipo=objeto_ordenado.tipo,
        posicion=10
    )
    assert obj.posicion == otro_objeto_ordenado.posicion + 1

def test_si_se_crea_objeto_con_posicion_demasiado_alta_en_coleccion_vacia_se_ajusta_a_cero():
    obj = MiTestModelConPositionField.crear(
        nombre="objeto con posicion demasiado alta",
        tipo="tipo1",
        posicion=10
    )
    assert obj.posicion == 0

def test_permite_eliminar_objetos_preexistentes(objeto_ordenado):
    campo_posicion = MiTestModelConPositionField._meta.get_field("posicion")

    if hasattr(campo_posicion, "clase"):
        delattr(campo_posicion, "clase")

    try:
        objeto_ordenado.delete()
    except AttributeError:
        raise AssertionError("Método pre_delete no encuentra el atributo 'clase' en PositionField")

def test_si_se_elimina_objeto_objetos_posteriores_de_la_coleccion_bajan_de_posicion(
        objeto_ordenado, otro_objeto_ordenado, tercer_objeto_ordenado):
    assert tercer_objeto_ordenado.posicion == 2

    otro_objeto_ordenado.delete()
    tercer_objeto_ordenado.refresh_from_db()

    assert tercer_objeto_ordenado.posicion == 1

def test_si_se_elimina_queryset_de_una_coleccion_objetos_que_no_son_del_queryset_bajan_de_posicion(
        objeto_ordenado, otro_objeto_ordenado, tercer_objeto_ordenado, cuarto_objeto_ordenado):
    objeto_ordenado.nombre += " xxx"
    objeto_ordenado.clean_save()
    otro_objeto_ordenado.nombre += " xxx"
    otro_objeto_ordenado.clean_save()

    MiTestModelConPositionField.objects.filter(nombre__contains="xxx").delete()

    tercer_objeto_ordenado.refresh_from_db()
    assert tercer_objeto_ordenado.posicion == 0
    cuarto_objeto_ordenado.refresh_from_db()
    assert cuarto_objeto_ordenado.posicion == 1

def test_si_se_elimina_queryset_no_continuo_de_una_coleccion_objetos_que_no_son_del_queryset_bajan_de_posicion(
        objeto_ordenado, otro_objeto_ordenado, tercer_objeto_ordenado, cuarto_objeto_ordenado):
    objeto_ordenado.nombre += " xxx"
    objeto_ordenado.clean_save()
    tercer_objeto_ordenado.nombre += " xxx"
    tercer_objeto_ordenado.clean_save()

    MiTestModelConPositionField.objects.filter(nombre__contains="xxx").delete()

    otro_objeto_ordenado.refresh_from_db()
    assert otro_objeto_ordenado.posicion == 0
    cuarto_objeto_ordenado.refresh_from_db()
    assert cuarto_objeto_ordenado.posicion == 1

def test_si_se_elimina_queryset_que_abarca_mas_de_una_coleccion_se_reasignan_posiciones_en_todas_las_colecciones_involucradas(
        objeto_ordenado, otro_objeto_ordenado, tercer_objeto_ordenado, objeto_de_otra_coleccion, otro_objeto_de_otra_coleccion):
    objeto_ordenado.nombre += "xxx"
    objeto_ordenado.clean_save()
    objeto_de_otra_coleccion.nombre += "xxx"
    objeto_de_otra_coleccion.clean_save()

    MiTestModelConPositionField.objects.filter(nombre__contains="xxx").delete()
    otro_objeto_ordenado.refresh_from_db()
    assert otro_objeto_ordenado.posicion == 0
    tercer_objeto_ordenado.refresh_from_db()
    assert tercer_objeto_ordenado.posicion == 1
    otro_objeto_de_otra_coleccion.refresh_from_db()
    assert otro_objeto_de_otra_coleccion.posicion == 0

def test_si_se_elimina_objeto_de_otra_coleccion_objetos_de_esta_coleccion_no_cambian(
        objeto_de_otra_coleccion, objeto_ordenado, otro_objeto_ordenado):
    pos1 = objeto_ordenado.posicion
    pos2 = otro_objeto_ordenado.posicion

    objeto_de_otra_coleccion.delete()

    objeto_ordenado.refresh_from_db()
    assert objeto_ordenado.posicion == pos1

    otro_objeto_ordenado.refresh_from_db()
    assert otro_objeto_ordenado.posicion == pos2

def test_si_se_cambia_posicion_a_una_anterior_objetos_entre_posicion_anterior_y_nueva_elevan_su_posicion(
        objeto_ordenado, otro_objeto_ordenado, tercer_objeto_ordenado, cuarto_objeto_ordenado, quinto_objeto_ordenado):
    cuarto_objeto_ordenado.posicion = 1
    cuarto_objeto_ordenado.clean_save()

    objeto_ordenado.refresh_from_db()
    assert objeto_ordenado.posicion == 0

    otro_objeto_ordenado.refresh_from_db()
    assert otro_objeto_ordenado.posicion == 2

    tercer_objeto_ordenado.refresh_from_db()
    assert tercer_objeto_ordenado.posicion == 3

    quinto_objeto_ordenado.refresh_from_db()
    assert quinto_objeto_ordenado.posicion == 4

def test_si_se_cambia_posicion_a_una_posterior_objetos_entre_posicion_anterior_y_nueva_bajan_su_posicion(
        objeto_ordenado, otro_objeto_ordenado, tercer_objeto_ordenado, cuarto_objeto_ordenado, quinto_objeto_ordenado):
    otro_objeto_ordenado.posicion = 3
    otro_objeto_ordenado.clean_save()

    objeto_ordenado.refresh_from_db()
    assert objeto_ordenado.posicion == 0

    tercer_objeto_ordenado.refresh_from_db()
    assert tercer_objeto_ordenado.posicion == 1

    cuarto_objeto_ordenado.refresh_from_db()
    assert cuarto_objeto_ordenado.posicion == 2

    quinto_objeto_ordenado.refresh_from_db()
    assert quinto_objeto_ordenado.posicion == 4

def test_si_cambia_posicion_a_una_demasiado_alta_se_ajusta_a_la_ultima_mas_uno(
        objeto_ordenado, otro_objeto_ordenado, tercer_objeto_ordenado):
    otro_objeto_ordenado.posicion = 5
    otro_objeto_ordenado.clean_save()
    assert otro_objeto_ordenado.posicion == 2

def test_si_cambia_posicion_en_coleccion_con_un_solo_objeto_se_ajusta_a_cero(objeto_ordenado):
    objeto_ordenado.posicion = 5
    objeto_ordenado.clean_save()
    assert objeto_ordenado.posicion == 0

def test_si_objeto_cambia_de_coleccion_pasa_a_la_ultima_posicion_de_la_nueva_coleccion(
        objeto_ordenado, otro_objeto_ordenado, tercer_objeto_ordenado, objeto_de_otra_coleccion):
    tercer_objeto_ordenado.tipo = objeto_de_otra_coleccion.tipo
    tercer_objeto_ordenado.clean_save()

    assert tercer_objeto_ordenado.posicion == 1

def test_si_objeto_cambia_de_coleccion_objetos_posteriores_de_la_coleccion_original_bajan_una_posicion(
        objeto_ordenado, otro_objeto_ordenado, tercer_objeto_ordenado, objeto_de_otra_coleccion):
    objeto_ordenado.tipo = objeto_de_otra_coleccion.tipo
    objeto_ordenado.clean_save()

    otro_objeto_ordenado.refresh_from_db()
    assert otro_objeto_ordenado.posicion == 0

    tercer_objeto_ordenado.refresh_from_db()
    assert tercer_objeto_ordenado.posicion == 1

def test_si_objeto_cambia_de_coleccion_a_una_sin_objetos_posicion_pasa_a_cero(objeto_ordenado, otro_objeto_ordenado):
    objeto_ordenado.tipo = "tipo nuevo"
    objeto_ordenado.clean_save()

    assert objeto_ordenado.posicion == 0

def test_con_colector_ordenado_si_objeto_cambia_a_una_coleccion_posterior_pasa_a_la_posicion_cero_de_la_nueva_coleccion(
        objeto_ordenado_colector_ordenado,
        otro_objeto_ordenado_colector_ordenado,
        objeto_ordenado_colector_ordenado_otra_coleccion):
    otro_objeto_ordenado_colector_ordenado.tipo = objeto_ordenado_colector_ordenado_otra_coleccion.tipo
    otro_objeto_ordenado_colector_ordenado.clean_save()

    assert otro_objeto_ordenado_colector_ordenado.posicion == 0

def test_con_colector_ordenado_si_objeto_cambia_a_una_coleccion_posterior_objetos_de_la_coleccion_suben_de_posicion(
        objeto_ordenado_colector_ordenado,
        otro_objeto_ordenado_colector_ordenado,
        objeto_ordenado_colector_ordenado_otra_coleccion):
    otro_objeto_ordenado_colector_ordenado.tipo = objeto_ordenado_colector_ordenado_otra_coleccion.tipo
    otro_objeto_ordenado_colector_ordenado.clean_save()

    objeto_ordenado_colector_ordenado_otra_coleccion.refresh_from_db()
    assert objeto_ordenado_colector_ordenado_otra_coleccion.posicion == 1

def test_con_colector_ordenado_si_objeto_cambia_a_una_coleccion_posterior_objetos_posteriores_de_la_coleccion_original_bajan_una_posicion(
        objeto_ordenado_colector_ordenado,
        otro_objeto_ordenado_colector_ordenado,
        objeto_ordenado_colector_ordenado_otra_coleccion):
    objeto_ordenado_colector_ordenado.tipo = objeto_ordenado_colector_ordenado_otra_coleccion.tipo
    objeto_ordenado_colector_ordenado.clean_save()

    otro_objeto_ordenado_colector_ordenado.refresh_from_db()
    assert otro_objeto_ordenado_colector_ordenado.posicion == 0

def test_con_colector_ordenado_si_objeto_cambia_a_una_coleccion_anterior_pasa_a_la_ultima_posicion_de_la_nueva_coleccion(
        objeto_ordenado_colector_ordenado,
        otro_objeto_ordenado_colector_ordenado,
        objeto_ordenado_colector_ordenado_coleccion_anterior):
    objeto_ordenado_colector_ordenado.tipo = objeto_ordenado_colector_ordenado_coleccion_anterior.tipo
    objeto_ordenado_colector_ordenado.clean_save()

    assert objeto_ordenado_colector_ordenado.posicion == 1

def test_con_colector_ordenado_si_objeto_cambia_de_coleccion_a_una_posterior_sin_objetos_posicion_pasa_a_cero(
        objeto_ordenado_colector_ordenado, otro_objeto_ordenado_colector_ordenado):
    objeto_ordenado_colector_ordenado.tipo = "tipo3"
    objeto_ordenado_colector_ordenado.clean_save()

    assert objeto_ordenado_colector_ordenado.posicion == 0

def test_con_colector_ordenado_si_objeto_cambia_de_coleccion_a_una_anterior_sin_objetos_posicion_pasa_a_cero(
        objeto_ordenado_colector_ordenado, otro_objeto_ordenado_colector_ordenado):
    otro_objeto_ordenado_colector_ordenado.tipo = "tipo0"
    otro_objeto_ordenado_colector_ordenado.clean_save()

    assert objeto_ordenado_colector_ordenado.posicion == 0

def test_si_cambia_coleccion_y_posicion_se_descarta_cambio_en_posicion(
        objeto_ordenado_colector_ordenado,
        otro_objeto_ordenado_colector_ordenado,
        objeto_ordenado_colector_ordenado_otra_coleccion):
    objeto_ordenado_colector_ordenado.tipo = objeto_ordenado_colector_ordenado_otra_coleccion.tipo
    objeto_ordenado_colector_ordenado.posicion = 2
    objeto_ordenado_colector_ordenado.clean_save()

    assert objeto_ordenado_colector_ordenado.posicion == 0

    objeto_ordenado_colector_ordenado_otra_coleccion.refresh_from_db()
    assert objeto_ordenado_colector_ordenado_otra_coleccion.posicion == 1


def test_admite_mas_de_un_positionfield():
    obj = MiTestModelConDoblePositionField.crear(nombre="objxxx", tipo="tipo1", colector="colecc1")
    obj2 = MiTestModelConDoblePositionField.crear(nombre="obj2xxx", tipo="tipo1", colector="colecc1")
    obj3 = MiTestModelConDoblePositionField.crear(nombre="obj3", tipo="tipo1", colector="colecc2")
    obj4 = MiTestModelConDoblePositionField.crear(nombre="obj4", tipo="tipo2", colector="colecc2")
    assert obj.posicion == 0
    assert obj.segunda_posicion == 0
    assert obj2.posicion == 1
    assert obj2.segunda_posicion == 1
    assert obj3.posicion == 2
    assert obj3.segunda_posicion == 0
    assert obj4.posicion == 0
    assert obj4.segunda_posicion == 1

    MiTestModelConDoblePositionField.objects.filter(nombre__contains="xxx").delete()

    obj3.refresh_from_db()
    assert obj3.posicion == 0
    assert obj3.segunda_posicion == 0

    obj3.delete()

    obj4.refresh_from_db()
    assert obj4.posicion == 0
    assert obj4.segunda_posicion == 0
