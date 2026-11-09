from datetime import date

import pytest

from vvmodel.tests.cleaners import MiTestCleaner
from vvmodel.tests.models import (
    MiTestRelatedModel as Model,
    MiTestModel as ComplexModel,
    MiTestPolymorphModel, MiTestPolymorphSubmodel, MiTestPolymorphSubSubModel, MiTestPolymorphOtherSubmodel
)


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker(pytest.mark.django_db)


@pytest.fixture
def miobjeto() -> Model:
    return Model.crear(nombre='miobjeto')


@pytest.fixture
def miotroobjeto() -> Model:
    return Model.crear(nombre='miotroobjeto')


@pytest.fixture
def mitercerobjeto() -> Model:
    return Model.crear(nombre='mitercerobjeto')


@pytest.fixture
def misobjetos(miobjeto: Model, miotroobjeto: Model, mitercerobjeto: Model) -> tuple[Model, Model, Model]:
    return (miobjeto, miotroobjeto, mitercerobjeto)


@pytest.fixture
def miobjetocomplejo(miobjeto: Model) -> ComplexModel:
    return ComplexModel.crear(nombre='miobjetocompleto', numero=5.0, related=miobjeto)


@pytest.fixture
def miotroobjetocomplejo(miotroobjeto: Model) -> ComplexModel:
    return ComplexModel.crear(nombre='miotroobjetocompleto', numero=5.0, related=miotroobjeto)


@pytest.fixture
def mitercerobjetocomplejo(miotroobjeto: Model) -> ComplexModel:
    return ComplexModel.crear(nombre='miotroobjetocompleto', numero=6.0, related=miotroobjeto)


@pytest.fixture
def mitercerobjetocomplejo(mitercerobjeto: Model) -> ComplexModel:
    return ComplexModel.crear(nombre='mitercerobjetocompleto', numero=6.0, related=mitercerobjeto)


@pytest.fixture
def misobjetoscomplejos(
        miobjetocomplejo: ComplexModel,
        miotroobjetocomplejo: ComplexModel,
        mitercerobjetocomplejo: ComplexModel,
) -> tuple[ComplexModel, ComplexModel, ComplexModel]:
    return (miobjetocomplejo, miotroobjetocomplejo, mitercerobjetocomplejo)


@pytest.fixture
def miobjetopolimorfico() -> MiTestPolymorphModel:
    return MiTestPolymorphModel.crear(nombre='objeto', numero=1)


@pytest.fixture
def misubobjetopolimorfico() -> MiTestPolymorphSubmodel:
    return MiTestPolymorphSubmodel.crear(nombre='subobjeto', numero=2, detalle='cosas')


@pytest.fixture
def miotrosubobjetopolimorfico() -> MiTestPolymorphOtherSubmodel:
    return MiTestPolymorphOtherSubmodel.crear(
        nombre='subotroobjeto', numero=3, caracteristicas='lista de características')


@pytest.fixture
def misubsubobjetopolimorfico() -> MiTestPolymorphSubSubModel:
    return MiTestPolymorphSubSubModel.crear(nombre='subsubobjeto', numero=3, detalle='cosas')


@pytest.fixture
def miobjetonopersistente(miotroobjeto):
    return ComplexModel(
        nombre='nuevo nombre',
        numero=567,
        fecha=date(2020, 2, 2),
        related=miotroobjeto
    )

@pytest.fixture
def mitestcleaner(miobjeto):
    return MiTestCleaner(obj=miobjeto)
