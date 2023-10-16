from django import forms
from .models import Comentario, Pelicula

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']

class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ['titulo', 'director']
        
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if Pelicula.objects.filter(titulo__iexact=titulo).exists():
            raise forms.ValidationError("Una película con este título ya existe.")
        return titulo
    