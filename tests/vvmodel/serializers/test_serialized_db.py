import pytest
from django.core.exceptions import ValidationError

from vvmodel.serializers import SerializedDb, SerializedObject


class TestUpdateOrAppendElements:

    def test_todos_sus_elementos_son_instancias_de_serializedobject(self):
        with pytest.raises(TypeError):
            serialized_db = SerializedDb([1, 2, 3])
        serialized_db = SerializedDb([SerializedObject(), SerializedObject()])  # No debe dar error

    def test_no_admite_que_se_asignen_elementos_que_no_sean_instancias_de_serializedobject(self):
        serialized_db = SerializedDb([SerializedObject()])
        with pytest.raises(TypeError):
            serialized_db[0] = 2
        serialized_db[0] = SerializedObject()   # No debe dar error

    def test_no_admite_que_se_agreguen_elementos_que_no_sean_instancias_de_serializedobject(self):
        serialized_db = SerializedDb()
        with pytest.raises(TypeError):
            serialized_db.append(2)
        serialized_db.append(SerializedObject())    # No debe dar error

    def test_no_admite_que_se_inserten_elementos_que_no_sean_instancias_de_serializedobject(self):
        serialized_db = SerializedDb([SerializedObject(), SerializedObject()])
        with pytest.raises(TypeError):
            serialized_db.insert(1, "a")
        serialized_db.insert(1, SerializedObject())     # No debe dar error

    def test_no_admite_extender_con_listas_que_contengan_elementos_que_no_sean_serializedobject(self):
        serialized_db = SerializedDb([SerializedObject()])
        lista = [SerializedObject(), 2, SerializedObject()]
        with pytest.raises(TypeError):
            serialized_db.extend(lista)
        serialized_db.extend([x for x in lista if isinstance(x, SerializedObject)])     # No debe dar error


class TestFilterByModel:

    def test_devuelve_serializeddb_con_todos_los_elementos_de_un_modelo_dado(
            self, serialized_db):
        serialized_model = serialized_db.filter_by_model("tests.mitestrelatedmodel")
        assert isinstance(serialized_model, SerializedDb)
        assert len(serialized_model) > 0
        for obj in serialized_model:
            assert obj["model"] == "tests.mitestrelatedmodel"

    def test_da_valueerror_si_recibe_app_no_registrada(self, serialized_db):
        with pytest.raises(
                ValueError,
                match='App "appinexistente" inexistente'
        ):
            serialized_db.filter_by_model("appinexistente.mitestrelatedmodel")

    def test_da_valueerror_si_recibe_modelo_inexistente_en_app(self, serialized_db):
        with pytest.raises(
                ValueError,
                match='Modelo "modeloinexistente" inexistente en app "tests"'
        ):
            serialized_db.filter_by_model("tests.modeloinexistente")


class TestFiltrar:
    def test_devuelve_una_instancia_de_SerializedDb(self, serialized_db):
        assert isinstance(serialized_db.filtrar(numero=5.0), SerializedDb)

    def test_incluye_en_el_resultado_todos_los_elementos_en_los_que_all_kwargs_present_es_verdadero(
            self, serialized_db, mocker):
        mock_all_kwargs_present = mocker.patch(
            "vvmodel.serializers.SerializedObject.all_kwargs_present",
            autospec=True
        )
        mock_all_kwargs_present.side_effect = [True, True, False, True, False, False, True, False, False, True, False]
        print(len(serialized_db))
        assert serialized_db.filtrar(cualquier="cosa") == [
            serialized_db[0],
            serialized_db[1],
            serialized_db[3],
            serialized_db[6],
            serialized_db[9],
        ]

    def test_incluye_en_la_SerializedDb_devuelta_todos_los_elementos_en_los_que_el_valor_del_campo_coincide_con_el_argumento(
            self, serialized_db):
        assert serialized_db.filtrar(numero=5.0) == [
            x for x in serialized_db if x.fields.get("numero") == 5.0
        ]

    def test_si_se_buscan_campos_con_valor_none_no_incluye_elementos_que_no_tengan_ese_campo(self, serialized_db):
        for dic in serialized_db[1:]:
            dic.fields.update({"algo": None})
        assert serialized_db[0] not in serialized_db.filtrar(algo=None)

    def test_si_el_argumento_es_model_devuelve_todos_los_elementos_de_ese_modelo(self, serialized_db):
        assert \
            serialized_db.filtrar(model="tests.mitestmodel") == \
            [x for x in serialized_db if x.model == "tests.mitestmodel"]


class TestTomar:
    def test_devuelve_el_primer_elemento_en_el_que_el_valor_del_campo_coincide_con_el_argumento(
            self, serialized_db):
        assert \
            serialized_db.tomar(nombre="miotroobjeto") == \
            next(x for x in serialized_db if x.fields["nombre"] == "miotroobjeto")

    def test_da_error_si_no_encuentra_el_elemento_solicitado(self, serialized_db):
        with pytest.raises(StopIteration):
            serialized_db.tomar(nombre="objetoinexistente")

    def test_si_el_argumento_es_model_busca_el_modelo_y_no_un_campo(self, serialized_db):
        assert \
            serialized_db.tomar(model="tests.mitestmodel") == \
            next(x for x in serialized_db if x.model == "tests.mitestmodel")

    def test_si_hay_argumento_pk_debe_haber_argumento_model(self, serialized_db):
        with pytest.raises(
                ValidationError,
                match='Si se pasa argumento "pk", debe estar presente el argumento "model" '
                    'o bien todos los valores de "model" en la serie deben ser iguales'
        ):
            serialized_db.tomar(pk=2)

    def test_si_hay_argumento_pk_puede_no_haber_argumento_model_si_todos_los_elementos_de_la_serie_tienen_el_mismo_valor_model(
            self, serialized_db):
        serialized_mitestmodel = serialized_db.filter_by_model("tests.mitestmodel")
        assert serialized_mitestmodel.tomar(pk=1) == next(
            x for x in serialized_db if x.model == "tests.mitestmodel" and x.pk == 1
        )

    def test_si_el_argumento_es_pk_busca_la_clave_primaria_y_no_un_campo(self, serialized_db):
        assert \
            serialized_db.tomar(model="tests.mitestmodel", pk=2) == \
            next(x for x in serialized_db if x.model == "tests.mitestmodel" and x.pk == 2)

    def test_si_recibe_pk_que_coincide_junto_con_campo_que_no_coincide_da_error(self, serialized_db):
        with pytest.raises(StopIteration):
            serialized_db.tomar(model="tests.mitestmodel", pk=2, nombre="objeto inexistente")

    def test_si_recibe_campo_que_coincide_junto_con_pk_que_no_coincide_devuelve_None(self, serialized_db):
        with pytest.raises(StopIteration):
            serialized_db.tomar(model="tests.mitestmodel", pk=5, nombre="mitestmodel")


class TestPrimere:

    @pytest.fixture
    def mock_tomar(self, mocker):
        return mocker.patch("vvmodel.serializers.SerializedDb.tomar", autospec=True)

    def test_devuelve_el_primer_elemento_del_modelo_dado_en_el_que_el_valor_del_campo_coincide_con_el_argumento(
            self, serialized_db):
        assert \
            serialized_db.primere("tests.mitestrelatedmodel", nombre="miotroobjeto") == \
            next(
                x for x in serialized_db.filter_by_model(
                    "tests.mitestrelatedmodel"
                ) if x.fields["nombre"] == "miotroobjeto"
            )

    def test_toma_objeto_con_los_valores_dados_de_la_base_de_datos_serializada(self, serialized_db, mock_tomar):
        serialized_db.primere("tests.mitestrelatedmodel", nombre="miotroobjeto")
        mock_tomar.assert_called_once_with(serialized_db, model="tests.mitestrelatedmodel", nombre="miotroobjeto")

    def test_puede_manejar_mas_de_un_argumento(self, serialized_db, mock_tomar):
        serialized_db.primere(
            "tests.mitestmodel", numero=5.0, nombre="miotroobjetocompleto")
        mock_tomar.assert_called_once_with(
            serialized_db, model="tests.mitestmodel", numero=5.0, nombre="miotroobjetocompleto")

    def test_devuelve_none_si_no_se_encuentra_el_elemento_solicitado(self, serialized_db):
        db_sin_model = SerializedDb([x for x in serialized_db if x.model != "tests.mitestrelatedmodel"])
        assert db_sin_model.primere("tests.mitestrelatedmodel") is None
