import pytest

from vvmodel import errors


def test_tira_error_si_detecta_un_cambio_en_el_campo_dado(miobjetocomplejo):
    miobjetocomplejo.nombre = 'otro nombre'
    with pytest.raises(
            errors.ErrorCambioEnCampoFijo,
            match="No se puede cambiar valor del campo 'nombre'"
    ):
        miobjetocomplejo.impedir_cambio('nombre')


def test_no_hace_nada_si_no_existe_version_persistente_del_objeto(miobjetonopersistente):
    miobjetonopersistente.impedir_cambio('nombre')  # No da error
