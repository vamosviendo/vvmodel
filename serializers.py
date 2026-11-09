from __future__ import annotations

import json
from collections import UserDict, UserList
from typing import Any, TextIO, Self, Union

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

serializedobjectvalue: type = Union[str, int, dict[str, Any]]


def _validate_app(app: str) -> str:
    if app in apps.all_models.keys():
        return app
    raise ValueError(f'App "{app}" inexistente')


def _validate_app_model(app: str, model: str) -> str:
    if model in apps.all_models[app].keys():
        return model
    raise ValueError(f'Modelo "{model}" inexistente en app "{app}"')

def _validate_app_and_model(model: str) -> str:
    app, app_model = model.split(".")
    _validate_app(app)
    _validate_app_model(app, app_model)
    return model


class SerializedObject(UserDict):

    @classmethod
    def model_string(cls):
        """ En subclases de SerializedObject, debe ser implementada para que
            devuelva la cadena "app.model" correspondiente al modelo
            representado
        """
        raise NotImplementedError('Método "model_string" no implementado')

    def __init__(self, dicc: dict | SerializedObject = None, /, container: SerializedDb = None, **kwargs):
        super().__init__(dicc, **kwargs)
        self.container = container
        if container is None:
            if isinstance(dicc, SerializedObject):
                self.container = dicc.container

    def __setitem__(self, key: str, value: serializedobjectvalue):
        key, value = self._validate(key, value)
        super().__setitem__(key, value)

    def __lt__(self, other):
        return (self.model, self.pk) < (other.model, other.pk)

    @property
    def model(self) -> str:
        return self['model']

    @model.setter
    def model(self, value: str):
        self['model'] = value

    @property
    def pk(self) -> int:
        return self['pk']

    @pk.setter
    def pk(self, value: int):
        self['pk'] = value

    @property
    def fields(self) -> dict[str, Any]:
        return self['fields']

    @fields.setter
    def fields(self, value: dict[str, Any]):
        self['fields'] = value

    @classmethod
    def primere(cls, container: SerializedDb, **kwargs) -> Self | None:
        result = container.primere(cls.model_string(), **kwargs)
        return cls(result) or None

    @classmethod
    def todes(cls, container: SerializedDb) -> SerializedDb:
        nuevo_container = container.filter_by_model(cls.model_string())

        try:
            keys = nuevo_container[0].fields.keys()
        except IndexError:
            keys = []

        if "content_type" in keys:
            try:
                content_types = set(".".join(x.fields["content_type"]) for x in nuevo_container)
            except TypeError:
                content_types = set()
                for x in nuevo_container:
                    content_type = ContentType.objects.get(pk=x.fields["content_type"])
                    content_types.add(f"{content_type.app_label}.{content_type.model}")

            for ct in content_types - {cls.model_string()}:
                nuevo_container += container.filter_by_model(ct)

        return SerializedDb([cls(x, nuevo_container) for x in nuevo_container])

    def all_kwargs_present(self, **kwargs) -> bool:
        """ Devuelve True si todos los argumentos pasados con nombre corresponden
            a pk, modelo o campos del objeto serializado.
        """
        result = True
        for key, value in kwargs.items():
            result = (self.pk == value) if key == "pk" \
                else (self.model == value) if key == "model" \
                else (key in self.fields.keys()) and (self.fields[key] == value)
            if result is False:
                break
        return result

    def _validate(self, key: str, value: serializedobjectvalue) -> tuple[str, serializedobjectvalue]:
        if key == "model":
            return key, self._validate_model(value)
        if key == "pk":
            return key, self._validate_pk(value)
        if key == "fields":
            return key, self._validate_fields(value)
        raise KeyError(
            f'Clave "{key}" no se encuentra entre las claves admitidas para SerializedObject')

    @staticmethod
    def _validate_model(model: str) -> str:
        if type(model) is str:
            try:
                app, app_model = model.split('.')
            except ValueError:
                raise ValueError(f'Valor "{model}" no responde a estructura correcta "<app>.<model>"')
            return f"{_validate_app(app)}.{_validate_app_model(app, app_model)}"

        raise TypeError(f'Tipo de valor "{model}" de clave "model" erróneo. Debe ser str')

    @staticmethod
    def _validate_pk(pk: int) -> int:
        if type(pk) is int:
            return pk
        raise TypeError(f'Tipo de valor "{pk}" de clave "pk" erróneo. Debe ser int')

    @staticmethod
    def _validate_fields(fields: dict[str, Any]):
        if isinstance(fields, dict):
            return fields
        raise TypeError(f'Tipo de valor "{fields}" de clave "fields" erróneo. Debe ser dict')


class SerializedDb(UserList):

    def __init__(self, initlist: list[SerializedObject] = None):
        initlist = map(self._validate, initlist) if initlist else None
        super().__init__(initlist)

    def __setitem__(self, index: int, item: SerializedObject):
        self.data[index] = self._validate(item)

    def append(self, item: SerializedObject):
        self.data.append(self._validate(item))

    def insert(self, index: int, item: SerializedObject):
        self.data.insert(index, self._validate(item))

    def extend(self, other: list[SerializedObject]):
        if isinstance(other, type(self)):
            self.data.extend(other)
        else:
            self.data.extend(self._validate(item) for item in other)

    def filtrar(self, **kwargs) -> SerializedDb:
        return SerializedDb([x for x in self if x.all_kwargs_present(**kwargs)])

    def filter_by_model(self, model: str) -> SerializedDb:
        return self.filtrar(model=_validate_app_and_model(model))

    def primere(self, model: str, **kwargs) -> SerializedObject | None:
        try:
            return self.tomar(model=model, **kwargs)
        except StopIteration:
            return None

    def tomar(self, **kwargs) -> SerializedObject:
        return next(x for x in self if x.all_kwargs_present(**self._validate_kwargs(kwargs)))

    @staticmethod
    def _validate(item: SerializedObject) -> SerializedObject:
        if isinstance(item, SerializedObject):
            return item
        raise TypeError

    def _validate_kwargs(self, kwargs):
        """ Si se pasa "pk", debe pasarse "model" a menos que todos los
            elementos de la serie compartan el mismo modelo.
        """
        if "pk" in kwargs.keys() and "model" not in kwargs.keys():
            models = [x.model for x in self]
            if not all(model == models[0] for model in models):
                raise ValidationError(
                    'Si se pasa argumento "pk", debe estar presente el '
                    'argumento "model" o bien todos los valores de "model" '
                    'en la serie deben ser iguales'
                )
        return kwargs


def load_serialized_filename(archivo: str) -> SerializedDb:
    with open(archivo, 'r') as db:
        return load_serialized_file(db)


def load_serialized_file(archivo: TextIO) -> SerializedDb:
    serialized_db = SerializedDb()
    for obj in json.load(archivo):
        serialized_db.append(SerializedObject(obj, container=serialized_db))
    return serialized_db
