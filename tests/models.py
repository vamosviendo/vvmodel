from datetime import date

from django.db import models

from vvmodel.fields import PositionField
from vvmodel.models import MiModel, PolymorphModel
from vvmodel.tests.cleaners import MiTestCleaner


class MiTestRelatedModel(MiModel):
    nombre = models.CharField(max_length=50, unique=True)

    cleaner = MiTestCleaner


class MiTestModel(MiModel):
    nombre = models.CharField(max_length=50, unique=True)
    numero = models.FloatField()
    fecha = models.DateField(default=date.today)
    related = models.ForeignKey(MiTestRelatedModel, on_delete=models.CASCADE, null=True)


class MiTestPolymorphModel(PolymorphModel):
    nombre = models.CharField(max_length=50, unique=True)
    numero = models.FloatField()


class MiTestPolymorphSubmodel(MiTestPolymorphModel):
    detalle = models.TextField()


class MiTestPolymorphOtherSubmodel(MiTestPolymorphModel):
    caracteristicas = models.TextField()


class MiTestPolymorphSubSubModel(MiTestPolymorphSubmodel):
    pass


class MiTestModelConPositionField(MiModel):
    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20)
    posicion = PositionField(campo_colector="tipo")

    def __str__(self):
        return f"{self.nombre} - {self.tipo} - {self.posicion}"


class MiTestModelConPositionFieldColectorOrdenado(MiModel):
    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20)
    posicion = PositionField(campo_colector="tipo", colector_ordenado=True)

    def __str__(self):
        return f"{self.nombre} - {self.tipo} - {self.posicion}"


class MiTestModelConDoblePositionField(MiTestModelConPositionField):
    colector = models.CharField(max_length=20)
    segunda_posicion = PositionField(campo_colector="colector")


class ModeloErroneo(MiTestModelConPositionFieldColectorOrdenado):
    segunda_posicion = PositionField(campo_colector="tipo")
