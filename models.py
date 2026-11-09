from __future__ import annotations

from typing import Self, Optional, Type, Iterable, cast, Literal

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet, Model

from . import errors
from .cleaners import Cleaner
from .managers import PolymorphManager
from vvutils.objetos import has_not_none_attr


class MiModel(models.Model):

    # Lista de nombres de campos destinados a aparecer en un ModelForm del modelo.
    # Se deja vacío para que de error si se lo usa sin definirlo en el modelo.
    form_fields: tuple[str]
    cleaner: Type[Cleaner] = Cleaner

    class Meta:
        abstract = True

    @classmethod
    def todes(cls, using: str = 'default') -> QuerySet[Self]:
        return cls.objects.using(using).all()

    @classmethod
    def primere(cls, using: str = 'default') -> Self:
        return cls.objects.using(using).first()

    @classmethod
    def ultime(cls, using: str = 'default') -> Self:
        return cls.objects.using(using).last()

    @classmethod
    def tomar(cls, **kwargs) -> Self:
        using = kwargs.pop('using') if 'using' in kwargs.keys() else 'default'

        return cls.objects.db_manager(using).get(**kwargs)

    @classmethod
    def cantidad(cls, using: str = 'default') -> int:
        return cls.objects.using(using).count()

    @classmethod
    def excepto(cls, *args, **kwargs) -> QuerySet[Self]:
        using = kwargs.pop('using') if 'using' in kwargs.keys() else 'default'
        return cls.objects.using(using).exclude(*args, **kwargs)

    @classmethod
    def filtro(cls, *args, **kwargs) -> QuerySet[Self]:
        using = kwargs.pop('using') if 'using' in kwargs.keys() else 'default'
        return cls.objects.using(using).filter(*args, **kwargs)

    @classmethod
    def crear(cls, **kwargs) -> Self:
        using = kwargs.pop('using', None)
        obj = cls(**kwargs)
        obj.full_clean()
        obj.save(using=using)
        return obj

    @classmethod
    def tomar_o_nada(cls, **kwargs) -> Optional[Self]:
        try:
            return cls.tomar(**kwargs)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_class(cls) -> Type[Self]:
        return cls

    @classmethod
    def get_class_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_lower_class_name(cls) -> str:
        return cls.get_class_name().lower()

    @classmethod
    def get_related_class(cls, campo) -> type[Model] | Literal["self"]:
        return cls._meta.get_field(campo).related_model

    @classmethod
    def get_max_length(cls, campo: str) -> int:
        return cls._meta.get_field(campo).max_length

    def tomar_de_bd(self) -> Optional[Self]:
        return self.get_class().tomar_o_nada(pk=self.pk)

    def clean_save(
            self, exclude=None, validate_unique=True, validate_constraints=True,
            force_insert=False, force_update=False, using=None, update_fields=None,
            omitir=None
    ):
        self.full_clean(exclude, validate_unique, validate_constraints, omitir)
        self.save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def full_clean(
            self, exclude=None, validate_unique=True, validate_constraints=True,
            omitir=None):
        super().full_clean(exclude, validate_unique, validate_constraints)
        self.limpiar(omitir=omitir)

    def limpiar(self, omitir: Iterable[str] | None = None, cleaner: Type[Cleaner] | None = None):
        Cleaner = cleaner or self.cleaner
        Cleaner(obj=self, omitir=omitir).procesar()

    def update_from(self, objeto: Self, commit: bool = True) -> Self:
        for campo in objeto.get_class()._meta.fields:
            valor = campo.value_from_object(objeto)
            if valor is not None:
                try:
                    setattr(self, campo.name, valor)
                except ValueError:
                    # Suponemos que es un campo de tipo foreign
                    setattr(
                        self, campo.name,
                        cast(
                            Self,
                            self._meta.get_field(campo.name).remote_field.model
                        ).tomar(pk=valor)
                    )

        if commit:
            self.save()

        return self

    def has_not_none_attr(self, atributo: str) -> bool:
        return has_not_none_attr(self, atributo)

    def any_field_changed(self) -> bool:
        fields = [f.name for f in self.get_class()._meta.fields]
        for field in fields:
            if getattr(self, field) != getattr(self.tomar_de_bd(), field):
                return True

        return False

    def primer_ancestre(self) -> Type['MiModel']:
        """ Devuelve el primer modelo del que es subclase.
            Si no es subclase, devuelve la clase propia.
        """
        try:
            return cast(Self, self._meta.get_parent_list()[-1])
        except IndexError:
            return self.get_class()

    def es_le_misme_que(self, otro: 'MiModel') -> bool:
        """ Devuelve True si self y otro apuntan al mismo registro más allá
            de la clase con la que se presenten.
        """

        try:
            return (self.primer_ancestre() == otro.primer_ancestre() and
                    self.pk == otro.pk)
        except AttributeError:
            return False

    def mantiene_foreignfield(self, campo: str, otro: Self) -> bool:
        """ Devuelve True si un foreignfield apunta al mismo objeto foráneo
            que el foreignfield de otra instancia.
        """
        valor = getattr(self, campo)
        if valor and not isinstance(valor, models.Model):
            raise AttributeError(
                f'El campo {campo} debe ser de tipo ForeignField'
            )

        try:
            return valor.es_le_misme_que(getattr(otro, campo))
        except AttributeError:
            return False

    def cambia_campo(self, *campos, contraparte: Self | None = None) -> bool:
        otro = contraparte or self.tomar_de_bd()
        for campo in campos:
            if campo not in [x.name for x in self._meta.fields]:
                raise ValueError(f"Campo inexistente: {campo}")
            campo_en_memoria = getattr(self, campo)

            try:
                otro_campo = getattr(otro, campo)
                if campo_en_memoria != otro_campo:
                    return True
            except AttributeError:  # otro is None => self es nuevo
                return True

        return False

    def impedir_cambio(self, campo: str) -> None:
        try:
            if self.cambia_campo(campo) and not self._state.adding:
                raise errors.ErrorCambioEnCampoFijo(
                    message=f"No se puede cambiar valor del campo '{campo}'"
                )
        except (AttributeError, self.DoesNotExist):
            pass


class PolymorphModel(MiModel):
    """ Agrega polimorfismo a MiModel."""

    class Meta:
        abstract = True

    content_type = models.ForeignKey(
        ContentType,
        null=True,
        editable=False,
        on_delete=models.CASCADE,
    )

    objects = PolymorphManager()

    @classmethod
    def tomar(cls, polymorphic: bool = True, **kwargs) -> Self:
        using = kwargs.pop('using') if 'using' in kwargs.keys() else 'default'

        if polymorphic:
            return super().tomar(using=using, **kwargs)
        return cls.objects.db_manager(using).get_no_poly(**kwargs)

    def como_subclase(self, db: str = 'default') -> 'PolymorphModel':
        """ Devuelve objeto polimórfico, basándose en el campo content_type.
            Arg db: corrige un error (¿bug?) que se produce cuando se intenta
            eliminar todos los registros de la clase madre (ver punto 2 en
            comentario inicial de vvmodel.managers).
        """
        content_type = self.content_type
        model = cast(Self, content_type.model_class())
        return model.tomar(pk=self.pk, polymorphic=False, using=db)

    def actualizar_subclase(self) -> 'PolymorphModel':
        """ Devuelve instancia con info de clase actualizada"""
        return self.primer_ancestre().tomar(pk=self.pk)

    def save(self, *args, using: str = 'default', **kwargs) -> None:

        if not self.content_type:
            ct = ContentType.objects.db_manager(using).get(
                app_label=self._meta.app_label,
                model=self.get_lower_class_name()
            )
            self.content_type = ct

        super().save(*args, **kwargs)
