from vvmodel.tests.models import MiTestRelatedModel, MiTestModel


class TestGetClass:

    def test_devuelve_la_clase_del_objeto(self, miobjeto, miobjetocomplejo):
        assert miobjeto.get_class() == MiTestRelatedModel
        assert miobjetocomplejo.get_class() == MiTestModel


class TestGetClassName:

    def test_devuelve_una_cadena_con_el_nombre_de_la_clase_del_objeto(self, miobjeto, miobjetocomplejo):
        assert miobjeto.get_class_name() == 'MiTestRelatedModel'
        assert miobjetocomplejo.get_class_name() == 'MiTestModel'


class TestGetRelatedClass:

    def test_devuelve_clase_del_modelo_relacionado_con_un_campo_foreign(self):
        assert MiTestModel.get_related_class('related') == MiTestRelatedModel

    def test_devuelve_none_si_el_campo_no_es_foreign(self):
        assert MiTestModel.get_related_class('nombre') is None


class TestGetLowerClassName:

    def test_devuelve_una_cadena_con_el_nombre_de_la_clase_en_minusculas(self, miobjeto):
        assert miobjeto.get_lower_class_name() == miobjeto.get_class_name().lower()
