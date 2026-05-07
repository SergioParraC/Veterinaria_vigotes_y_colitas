from django import forms
from .models import Perfil, Usuario, Cuenta_Usuario
import re


class PerfilForm(forms.ModelForm):
    nombre = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre del perfil'}),
        help_text='Ingresa el nombre del perfil o rol (máximo 100 caracteres). Ejemplo: Administrador, Veterinario.'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
        help_text='Correo electrónico asociado al perfil. Debe ser único.'
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '300 000 0000'}),
        help_text='Número de teléfono opcional. Solo dígitos.'
    )
    direccion = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Dirección del perfil', 'rows': 2}),
        help_text='Dirección física opcional del perfil.'
    )

    class Meta:
        model = Perfil
        fields = ['nombre', 'email', 'telefono', 'direccion']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or not nombre.strip():
            raise forms.ValidationError('El nombre es obligatorio.')
        return nombre.strip()

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        if telefono:
            digitos = re.sub(r'\D', '', telefono)
            if not digitos.isdigit():
                raise forms.ValidationError('El teléfono solo puede contener dígitos.')
            if len(digitos) != 10:
                raise forms.ValidationError('El teléfono debe tener exactamente 10 dígitos.')
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or not email.strip():
            raise forms.ValidationError('El correo electrónico es obligatorio.')
        if Perfil.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Ya existe un perfil con este correo electrónico.')
        return email.strip()


class UsuarioForm(forms.ModelForm):
    nombre = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre'}),
        help_text='Primer nombre del usuario (máximo 100 caracteres).'
    )
    apellido = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Apellido'}),
        help_text='Apellido del usuario (máximo 100 caracteres).'
    )
    tipo_documento = forms.ChoiceField(
        required=True,
        choices=[('CC', 'Cédula de Ciudadanía'), ('TI', 'Tarjeta de Identidad'), ('CE', 'Cédula de Extranjería'), ('Otro', 'Otro')],
        widget=forms.Select(),
        help_text='Tipo de documento de identidad del usuario.'
    )
    numero_documento = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Número de documento'}),
        help_text='Número único de identificación del usuario.'
    )
    correo = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
        help_text='Correo electrónico único del usuario. Se usará para comunicaciones.'
    )
    telefono = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '300 000 0000'}),
        help_text='Teléfono de contacto del usuario. Exactamente 10 dígitos.'
    )
    direccion = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Dirección'}),
        help_text='Dirección de residencia del usuario.'
    )
    rol = forms.ModelChoiceField(
        queryset=Perfil.objects.all(),
        required=False,
        empty_label='Sin rol',
        widget=forms.Select(),
        help_text='Rol o perfil asignado al usuario (opcional).'
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'tipo_documento', 'numero_documento', 'correo', 'telefono', 'direccion', 'rol']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or not nombre.strip():
            raise forms.ValidationError('El nombre es obligatorio.')
        return nombre.strip()

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        if not apellido or not apellido.strip():
            raise forms.ValidationError('El apellido es obligatorio.')
        return apellido.strip()

    def clean_numero_documento(self):
        doc = self.cleaned_data.get('numero_documento')
        if not doc or not doc.strip():
            raise forms.ValidationError('El número de documento es obligatorio.')
        if Usuario.objects.filter(numero_documento=doc).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Ya existe un usuario con este número de documento.')
        return doc.strip()

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if not correo or not correo.strip():
            raise forms.ValidationError('El correo electrónico es obligatorio.')
        if Usuario.objects.filter(correo=correo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Ya existe un usuario con este correo electrónico.')
        return correo.strip()

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono or not telefono.strip():
            raise forms.ValidationError('El teléfono es obligatorio.')
        digitos = re.sub(r'\D', '', telefono)
        if not digitos.isdigit():
            raise forms.ValidationError('El teléfono solo puede contener dígitos.')
        if len(digitos) != 10:
            raise forms.ValidationError('El teléfono debe tener exactamente 10 dígitos.')
        return digitos

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if not direccion or not direccion.strip():
            raise forms.ValidationError('La dirección es obligatoria.')
        return direccion.strip()


class CuentaUsuarioForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        required=True,
        empty_label='Seleccione un usuario',
        widget=forms.Select(),
        help_text='Usuario al que se le asignará esta cuenta.'
    )
    nombre_usuario = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
        help_text='Nombre único para iniciar sesión (mínimo 4 caracteres, máximo 150).'
    )
    contrasena = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        help_text='Contraseña de acceso. Mínimo 6 caracteres. Al editar, dejar vacío para no cambiarla.'
    )
    estado = forms.BooleanField(
        required=False,
        initial=True,
        help_text='Si está activo, el usuario podrá iniciar sesión.'
    )

    class Meta:
        model = Cuenta_Usuario
        fields = ['usuario', 'nombre_usuario', 'contrasena', 'estado']

    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario')
        if not usuario:
            raise forms.ValidationError('Debes seleccionar un usuario.')
        if Cuenta_Usuario.objects.filter(usuario=usuario).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este usuario ya tiene una cuenta asignada.')
        return usuario

    def clean_nombre_usuario(self):
        nombre_usuario = self.cleaned_data.get('nombre_usuario')
        if not nombre_usuario or not nombre_usuario.strip():
            raise forms.ValidationError('El nombre de usuario es obligatorio.')
        if len(nombre_usuario.strip()) < 4:
            raise forms.ValidationError('El nombre de usuario debe tener al menos 4 caracteres.')
        if Cuenta_Usuario.objects.filter(nombre_usuario=nombre_usuario).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Ya existe una cuenta con este nombre de usuario.')
        return nombre_usuario.strip()

    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        if not self.instance.pk:
            if not contrasena:
                raise forms.ValidationError('La contraseña es obligatoria al crear una cuenta.')
            if len(contrasena) < 6:
                raise forms.ValidationError('La contraseña debe tener al menos 6 caracteres.')
        elif contrasena and len(contrasena) < 6:
            raise forms.ValidationError('La contraseña debe tener al menos 6 caracteres.')
        return contrasena
