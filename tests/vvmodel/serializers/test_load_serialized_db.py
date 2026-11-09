from io import TextIOWrapper

from vvmodel.serializers import load_serialized_file, load_serialized_filename, SerializedDb


def test_devuelve_una_instancia_de_SerializedDb(serialized_file):
    assert isinstance(load_serialized_file(serialized_file), SerializedDb)


def test_instancia_devuelta_contiene_objetos_de_la_base_de_datos(elementos, serialized_file):
    serialized_db = load_serialized_file(serialized_file)
    identidades = [(x['model'], x['pk']) for x in serialized_db]
    for elemento in elementos:
        assert (elemento._meta.label_lower, elemento.pk) in identidades


def test_incluye_en_cada_objeto_una_referencia_a_la_SerializedDb_contenedora(elementos, serialized_file):
    serialized_db = load_serialized_file(serialized_file)
    for elemento in serialized_db:
        assert elemento.container == serialized_db


def test_load_serialized_filename_carga_archivo_serializado_a_partir_de_nombre_de_archivo(serialized_file, mocker):
    mock_load_serialized_file = mocker.patch("vvmodel.serializers.load_serialized_file")
    load_serialized_filename("db.json")
    mock_load_serialized_file.assert_called_once()
    arg = mock_load_serialized_file.call_args.args[0]
    assert isinstance(arg, TextIOWrapper)
    assert arg.name == "db.json"
    assert arg.mode == "r"
