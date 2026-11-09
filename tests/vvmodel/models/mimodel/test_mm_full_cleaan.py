def test_llama_a_metodo_limpiar(miobjeto, mocker):
    mock_limpiar = mocker.patch("vvmodel.models.MiModel.limpiar")
    miobjeto.full_clean()
    mock_limpiar.assert_called_once()


def test_permite_omitir_comprobaciones(miobjeto, mocker):
    mock_limpiar = mocker.patch("vvmodel.models.MiModel.limpiar")
    miobjeto.full_clean(omitir=["metodo_uno"])
    mock_limpiar.assert_called_with(omitir=["metodo_uno"])
