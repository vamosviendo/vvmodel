from typing import cast
from django.core.exceptions import ValidationError
from django.db.models import PositiveIntegerField, signals, QuerySet


class PositionField(PositiveIntegerField):
    def __init__(self, *args, campo_colector: str, colector_ordenado: bool = False, **kwargs):
        kwargs["null"] = True
        kwargs["blank"] = True
        self.campo_colector = campo_colector
        self.colector_ordenado = colector_ordenado
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        kwargs.pop('null', None)
        kwargs.pop('blank', None)
        kwargs["campo_colector"] = self.campo_colector
        kwargs["colector_ordenado"] = self.colector_ordenado

        return name, path, args, kwargs

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        signals.pre_delete.connect(
            self.pre_delete,
            sender=cls,
            weak=False,
        )

    def pre_delete(self, sender, instance, **kwargs):
        self.clase = type(instance)
        origin = kwargs.get("origin")

        # Si NO es un QuerySet, desplazar posiciones
        if not isinstance(origin, QuerySet):
            self._desplazar_otras_posiciones_de_la_coleccion(
                objeto=instance,
                coleccion=getattr(instance, self.campo_colector),
                desplazamiento=1,
                incremento=-1
            )
            return

        # Si es un QuerySet, no hacer nada hasta que se eliminen todas las instancias
        cantidad_eliminada = origin.count()

        if not hasattr(sender, '_deleting_pks'):
            sender._deleting_pks = set()
        if not hasattr(sender, '_colecciones'):
            sender._colecciones = set()

        sender._deleting_pks.add(instance.pk)
        sender._colecciones.add(getattr(instance, self.campo_colector))

        # Esperar a que se eliminen todos los elementos del queryset para reasignar posiciones
        if len(sender._deleting_pks) == cantidad_eliminada:
            for coleccion in sender._colecciones:

                objetos_restantes = sender.objects.filter(
                    **{self.campo_colector: coleccion}
                ).exclude(pk__in=sender._deleting_pks).order_by(self.attname)

                # Reasignar posiciones consecutivas desde 0
                for index, obj in enumerate(objetos_restantes):
                    sender.objects.filter(pk=obj.pk).update(**{self.attname: index})

            if hasattr(sender, '_deleting_pks'):
                del sender._deleting_pks
            if hasattr(sender, '_colecciones'):
                del sender._colecciones

    def pre_save(self, model_instance, add):
        self.clase = type(model_instance)
        self.objeto = cast(self.clase, model_instance)
        self.coleccion = getattr(self.objeto, self.campo_colector)
        self.items_coleccion = self.clase.objects.filter(**{self.campo_colector: self.coleccion})
        self.ultimo_objeto_anterior = self.items_coleccion.last()

        if self.objeto._state.adding:
            # Pre_save se ejecuta dos veces. Una con add=False y otra con add=True.
            # Aplicar side effects solo una vez. Funciona igual con "if add", excepto
            # que hace que falle la verificación paranoica antes de asignar el valor
            # al objeto, así que optamos por "if not add"
            valor = self._asignar_posicion_nueva(not add)
        else:
            valor = self._modificar_posicion_existente()

        self._verificar_que_no_se_repite_posicion(valor)

        setattr(self.objeto, self.attname, valor)

        return getattr(self.objeto, self.attname)

    def _asignar_posicion_nueva(self, produce_efectos):
        valor = getattr(self.objeto, self.attname)
        if valor is None:
            try:
                return getattr(self.ultimo_objeto_anterior, self.attname) + 1
            except AttributeError:  # ultimo_objeto_anterior is None. No hay objetos en la colección.
                return 0
        try:
            ultima_posicion = getattr(self.ultimo_objeto_anterior, self.attname)
            if valor > ultima_posicion + 1:
                return ultima_posicion + 1

            if produce_efectos:
                self._desplazar_otras_posiciones_de_la_coleccion()
        except AttributeError:  # ultimo_objeto_anterior is None. No hay objetos en la colección.
            return 0

        return valor

    def _modificar_posicion_existente(self):
        valor = getattr(self.objeto, self.attname)
        original = self.clase.objects.get(pk=self.objeto.pk)
        valor_original = getattr(original, self.attname)
        coleccion_original = getattr(original, self.campo_colector)

        if self.coleccion != coleccion_original:
            setattr(self.objeto, self.attname, valor_original)
            self._desplazar_otras_posiciones_de_la_coleccion(
                coleccion=coleccion_original,
                desplazamiento=1,
                incremento=-1
            )

            if self.colector_ordenado and self.coleccion > coleccion_original:
                self._desplazar_otras_posiciones_de_la_coleccion(desplazamiento=-1)
                return 0

            try:
                return getattr(self.ultimo_objeto_anterior, self.attname) + 1
            except AttributeError:  # ultimo_objeto_anterior is None. No hay objetos en la colección.
                return 0

        if valor < valor_original:
            self._desplazar_otras_posiciones_de_la_coleccion(hasta=valor_original)
        elif valor > valor_original:
            ultima_posicion = getattr(self.ultimo_objeto_anterior, self.attname)
            if valor > ultima_posicion:
                valor = ultima_posicion
            self._desplazar_otras_posiciones_de_la_coleccion(
                objeto=original,
                hasta=valor + 1,
                incremento=-1
            )

        return valor

    def _desplazar_otras_posiciones_de_la_coleccion(
            self,
            objeto=None,
            coleccion=None,
            desplazamiento=0,
            hasta=None,
            incremento=1
    ):
        objeto = objeto or self.objeto
        coleccion = coleccion or self.coleccion
        filtro = {
            self.campo_colector: coleccion,
            f"{self.attname}__gte": getattr(objeto, self.attname) + desplazamiento
        }
        if hasta:
            filtro[f"{self.attname}__lt"] = hasta
        objetos_a_desplazar = self.clase.objects.filter(**filtro).exclude(pk=objeto.pk)

        for obj in objetos_a_desplazar:
            posicion = getattr(obj, self.attname)
            self.clase.objects.filter(pk=obj.pk).update(**{self.attname: posicion + incremento})

    def _verificar_que_no_se_repite_posicion(self, valor):
        # Verificación paranoica para estar seguro de que no hay posiciones repetidas
        # en una colección
        posiciones_existentes = [
            getattr(obj, self.attname) for obj in self.items_coleccion.exclude(pk=self.objeto.pk)
        ]
        if valor in posiciones_existentes:
            raise ValidationError(f"Posición {valor} repetida en colección {self.coleccion}")
