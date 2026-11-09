from django.core.exceptions import ValidationError

# Managers

ERROR_QUERYSET_DELETE = 'Por razones de seguridad no se permite ' \
                        'QuerySet.delete().' \
                        'Use instance.delete() en su lugar.'


class ErrorCambioEnCampoFijo(ValidationError):
    """ Se intentó cambiar el valor de un campo fijo"""
    def __init__(self, message='Se intentó cambiar el valor de un campo fijo'):
        super().__init__(message)
