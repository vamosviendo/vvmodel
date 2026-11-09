from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_es_le_misme_que(mocker):
    return mocker.patch('vvmodel.models.MiModel.es_le_misme_que', autospec=True)


def test_compara_contenido_de_foreignfield_con_el_de_otra_instancia(miobjetocomplejo, mock_es_le_misme_que):
    objeto = miobjetocomplejo
    miobjetocomplejo.mantiene_foreignfield('related', objeto)
    mock_es_le_misme_que.assert_called_once_with(miobjetocomplejo.related, objeto.related)


def test_devuelve_true_si_foreignfield_apunta_al_mismo_objeto_que_el_de_otra_instancia(
        miobjetocomplejo, mock_es_le_misme_que):
    mock_otro = MagicMock()
    mock_es_le_misme_que.return_value = True
    assert miobjetocomplejo.mantiene_foreignfield('related', mock_otro)


def test_devuelve_false_si_foreignfield_apunta_un_objeto_distinto_que_el_de_otra_instancia(
        miobjetocomplejo, mock_es_le_misme_que):
    mock_otro = MagicMock()
    mock_es_le_misme_que.return_value = False
    assert not miobjetocomplejo.mantiene_foreignfield('related', mock_otro)


def test_devuelve_false_si_foreignfield_es_none(
        miobjetocomplejo):
    mock_otro = MagicMock()
    miobjetocomplejo.related = None
    assert not miobjetocomplejo.mantiene_foreignfield('related', mock_otro)


def test_tira_error_si_el_campo_no_es_foreignfield(miobjetocomplejo):
    mock_otro = MagicMock()
    with pytest.raises(AttributeError, match='El campo nombre debe ser de tipo ForeignField'):
        miobjetocomplejo.mantiene_foreignfield('nombre', mock_otro)
