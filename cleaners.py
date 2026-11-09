from __future__ import annotations

from typing import TYPE_CHECKING, Type, cast, Iterable

if TYPE_CHECKING:
    from vvmodel.models import MiModel


class Cleaner:
    def __init__(self, obj: MiModel, omitir: Iterable[str] | None = None):
        self.obj = cast(Type[obj], obj)
        self.omitir = omitir or []

    def procesar(self):
        for nombre_metodo in self.__class__.__dict__:
            metodo = getattr(self, nombre_metodo)
            if callable(metodo) \
                    and not nombre_metodo.startswith("_") \
                    and nombre_metodo not in Cleaner.__dict__ \
                    and nombre_metodo not in self.omitir:
                metodo()

    def dumb(self):
        pass
