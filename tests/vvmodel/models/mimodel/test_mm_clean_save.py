from vvmodel.tests.models import MiTestRelatedModel


def test_hace_un_full_clean_al_guardar_un_objeto_nuevo(mocker):
    mock_full_clean = mocker.patch('vvmodel.models.MiModel.full_clean', autospec=True)
    obj = MiTestRelatedModel(nombre="Modelo a guardar")
    obj.clean_save()
    mock_full_clean.assert_called_once_with(obj, None, True, True, None)


def test_guarda_un_objeto_nuevo(mocker):
    mock_save = mocker.patch('vvmodel.models.MiModel.save', autospec=True)
    obj = MiTestRelatedModel(nombre="Modelo a guardar")
    obj.clean_save()
    mock_save.assert_called_once_with(obj, force_insert=False, force_update=False, using=None, update_fields=None)


def test_integrativo_guarda_objeto_nuevo():
    cantidad = MiTestRelatedModel.cantidad()
    obj = MiTestRelatedModel(nombre="Modelo a guardar")
    obj.clean_save()
    assert MiTestRelatedModel.cantidad() == cantidad + 1


def test_acepta_y_pasa_parametros_de_full_clean(mocker):
    mock_full_clean = mocker.patch('vvmodel.models.MiModel.full_clean', autospec=True)
    obj = MiTestRelatedModel(nombre="Modelo a guardar")
    obj.clean_save(exclude=["list"], validate_unique=False, validate_constraints=False)
    mock_full_clean.assert_called_once_with(
        obj, ["list"], False, False, None
    )


def test_acepta_y_pasa_parametros_de_save(mocker):
    mock_save = mocker.patch('vvmodel.models.MiModel.save', autospec=True)
    obj = MiTestRelatedModel(nombre="Modelo a guardar")
    obj.clean_save(force_insert=True, force_update=True, using="db.sqlite3", update_fields=["field"])
    mock_save.assert_called_once_with(obj, force_insert=True, force_update=True, using="db.sqlite3", update_fields=["field"])


def test_puede_omitir_comprobaciones(miobjeto, mocker):
    mock_full_clean = mocker.patch("vvmodel.models.MiModel.full_clean")
    miobjeto.clean_save(omitir=["metodo_uno"])
    ANY = mocker.ANY
    mock_full_clean.assert_called_with(ANY, ANY, ANY, ["metodo_uno"])
