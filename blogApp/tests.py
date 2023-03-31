from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# creo la excepción para que no se acepten numeros en los tags
def validar_texto(value):
    lista=[]
    lista_numeros=['0','1','2','3','4','5','6','7','8','9']
    for i in value:
        lista.append(i)
        if i in lista_numeros:
            raise ValidationError(
                _('%(value)s should not have numbers'),
                params={'value': value},
            )
