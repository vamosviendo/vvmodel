from __future__ import annotations

import pytest

from vvmodel.tests.models import MiTestModel, MiTestRelatedModel


@pytest.fixture
def params(miobjeto) -> dict[str, str | float | MiTestRelatedModel]:
    return {
        'nombre': 'objeto',
        'numero': 3.0,
        'related': miobjeto,
    }


def test_crea_objeto(params):
    MiTestModel.crear(**params)
    assert MiTestModel.cantidad() == 1


def test_devuelve_objeto(params, miobjeto):
    obj = MiTestModel.crear(**params)
    assert obj.nombre == 'objeto'
    assert obj.numero == 3.0
    assert obj.related == miobjeto


def test_verifica_objeto(params, mocker):
    mock_full_clean = mocker.patch('vvmodel.tests.models.MiTestModel.full_clean', autospec=True)
    obj = MiTestModel.crear(**params)
    mock_full_clean.assert_called_once_with(obj)


def test_guarda_objeto(params, mocker):
    mock_save = mocker.patch('vvmodel.tests.models.MiTestModel.save', autospec=True)
    obj = MiTestModel.crear(**params)
    mock_save.assert_called_once_with(obj, using=None)
