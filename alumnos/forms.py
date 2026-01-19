from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroAlumnoForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        # El orden aquí es como aparecerá en la página de registro
        fields = UserCreationForm.Meta.fields + (
            'nombre_completo', 
            'apellido_completo', 
            'email', 
            'curso',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Forzamos que estos campos sean obligatorios
        self.fields['nombre_completo'].required = True
        self.fields['apellido_completo'].required = True
        self.fields['email'].required = True