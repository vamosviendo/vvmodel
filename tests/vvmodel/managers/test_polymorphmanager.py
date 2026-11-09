import pytest

from vvmodel.managers import PolymorphManager, PolymorphQuerySet
from vvmodel.tests.models import MiTestPolymorphModel


@pytest.fixture
def poly_manager() -> PolymorphManager:
    pm = PolymorphManager()
    pm.model = MiTestPolymorphModel
    return pm


def test_get_queryset_devuelve_queryset_polimorfica(poly_manager):
    assert type(poly_manager.get_queryset()) is PolymorphQuerySet


def test_queryset_polimorfico_devuelve_item_con_la_clase_correcta(poly_manager):
    for o in poly_manager.get_queryset().__iter__():
        assert type(o) == o.content_type().model_class()
