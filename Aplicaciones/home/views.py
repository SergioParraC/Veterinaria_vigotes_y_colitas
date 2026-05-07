from django.shortcuts import render

def home(request):
    data = {
        'titlePage': 'Veterinaria Vida Animal',
        'titulo': 'Veterinaria Vida Animal'
    }
    return render(request, 'home.html', data)
