from django import forms
from . import models


class ContactoForm(forms.ModelForm):
    class Meta:
        model = models.Contacto
        fields = ['nombre', 'numero_contacto', 'email', 'mensaje']
        labels = {
            'nombre': 'Nombre',
            'numero_contacto': 'Numero de contacto',
            'email': 'Correo electronico',
            'mensaje': 'Mensaje',
        }
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 4}),
        }
