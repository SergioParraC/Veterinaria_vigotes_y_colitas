from django.shortcuts import render
from . import forms

def home(request):
    data = {
        'titlePage': 'Veterinaria Vida Animal',
        'titulo': 'Veterinaria Vida Animal',
    }
    return render(request, 'home.html', data)


def contacto(request):
    mensaje_contacto = ''

    if request.method == 'POST':
        formulario_contacto = forms.ContactoForm(request.POST)
        if formulario_contacto.is_valid():
            formulario_contacto.save()
            mensaje_contacto = 'Tu mensaje fue enviado correctamente.'
            formulario_contacto = forms.ContactoForm()
    else:
        formulario_contacto = forms.ContactoForm()

    data = {
        'titlePage': 'Contacto',
        'titulo': 'Contacto',
        'formulario_contacto': formulario_contacto,
        'mensaje_contacto': mensaje_contacto,
    }
    return render(request, 'contacto.html', data)
