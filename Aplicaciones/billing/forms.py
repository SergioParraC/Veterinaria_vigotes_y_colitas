from django import forms
from Aplicaciones.pets.models import Dueño, Mascota

'''Muestra los clientes para crear la factura'''
class CrearFacturaClienteForm(forms.Form):
    cliente = forms.ModelChoiceField(
        label="Cliente",
        queryset=Dueño.objects.all(),
        empty_label="Selecciona un cliente"
    )

'''Muestra las mascotas del cliente seleccionado'''
class CrearFacturaMascotaForm(forms.Form):
    mascota = forms.ModelChoiceField(
        label="Mascota",
        queryset=Mascota.objects.none(),
        empty_label="Selecciona la mascota",
        required=False
    )

    # Método donde se filtran las masctoas por cliente
    def __init__(self, *args, **kwargs):
        # Obtiene el id_cliente pasado desde la vista para filtrar las mascotas
        cliente_id = kwargs.pop('cliente_id', None)
        super().__init__(*args, **kwargs)
        # Si se proporcionó un cliente_id, filtra las mascotas por ese cliente
        if cliente_id:
            self.fields['mascota'].queryset = Mascota.objects.filter(dueño_id=cliente_id)

    # NOTA: Es posible crear una factura sin seleccionar la mascota