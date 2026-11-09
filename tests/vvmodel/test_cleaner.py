def test_ejecuta_todos_los_metodos_de_la_clase(mitestcleaner, mocker):
    mock_m1 = mocker.patch("vvmodel.tests.cleaners.MiTestCleaner.metodo_uno")
    mock_m2 = mocker.patch("vvmodel.tests.cleaners.MiTestCleaner.metodo_dos")
    mitestcleaner.procesar()
    for mock in mock_m1, mock_m2:
        mock.assert_called_once()


def test_ejecuta_los_metodos_en_el_orden_en_el_que_aparecen_en_la_clase(mitestcleaner, mocker):
    registro_llamadas = []

    mock_m1 = mocker.patch("vvmodel.tests.cleaners.MiTestCleaner.metodo_uno")
    mock_m2 = mocker.patch("vvmodel.tests.cleaners.MiTestCleaner.metodo_dos")

    mock_m1.side_effect = lambda: registro_llamadas.append("metodo_uno")
    mock_m2.side_effect = lambda: registro_llamadas.append("metodo_dos")

    mitestcleaner.procesar()

    assert registro_llamadas == ["metodo_uno", "metodo_dos"]


def test_no_ejecuta_metodos_protegidos(mitestcleaner, mocker):
    mock_metodo = mocker.patch("vvmodel.tests.cleaners.MiTestCleaner._metodo_protegido")
    mitestcleaner.procesar()
    mock_metodo.assert_not_called()


def test_no_ejecuta_metodos_de_la_clase_Cleaner(mitestcleaner, mocker):
    mock_dumb = mocker.patch("vvmodel.tests.cleaners.MiTestCleaner.dumb")
    mitestcleaner.procesar()
    mock_dumb.assert_not_called()


def test_no_ejecuta_metodos_recibidos_en_lista_omitir(miobjeto, mocker):
    mock_m1 = mocker.patch("vvmodel.tests.cleaners.MiTestCleaner.metodo_uno")
    cleaner = miobjeto.cleaner(obj=miobjeto, omitir=["metodo_uno"])
    cleaner.procesar()
    mock_m1.assert_not_called()
