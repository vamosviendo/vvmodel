from vvmodel.tests.cleaners import MiTestCleaner, OtroTestCleaner


def test_crea_un_cleaner_de_la_clase_asociada_al_modelo(miobjeto, mocker):
    spy_cleaner = mocker.spy(MiTestCleaner, '__init__')

    miobjeto.limpiar()

    assert spy_cleaner.called is True
    assert spy_cleaner.call_count == 1


def test_pasa_el_objeto_self_al_cleaner_creado(miobjeto, mocker):
    cleaner_spy = mocker.spy(MiTestCleaner, '__init__')
    miobjeto.limpiar()
    cleaner_spy.assert_called_with(mocker.ANY, obj=miobjeto, omitir=None)


def test_procesa_cleaner_creado(miobjeto, mocker):
    mock_procesar = mocker.patch.object(MiTestCleaner, 'procesar')
    miobjeto.limpiar()
    mock_procesar.assert_called_once()


def test_puede_usar_cleaner_distinto_del_asociado_al_modelo(miobjeto, mocker):
    spy_cleaner = mocker.spy(MiTestCleaner, '__init__')
    spy_otro_cleaner = mocker.spy(OtroTestCleaner, '__init__')

    miobjeto.limpiar(cleaner=OtroTestCleaner)

    assert spy_cleaner.called is False
    assert spy_otro_cleaner.called is True


def test_pueden_omitirse_metodos_del_cleaner_asociado(miobjeto, mocker):
    mock_metodo = mocker.patch("vvmodel.tests.cleaners.MiTestCleaner.metodo_dos")
    miobjeto.limpiar(omitir=["metodo_dos"])
    mock_metodo.assert_not_called()
