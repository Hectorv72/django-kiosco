from django.forms import ModelForm
from django import forms
from .models import *
#from . import models

class FormArticulos(ModelForm):
    class Meta:
        model = Articulos
        fields = ['nombre_art','precio','rubro','stock']
        labels = { "nombre_art": "Articulo"}
"""
class FormForo(ModelForm):
	class Meta:
		model = Foros
		fields = ['nom_foro','descripcion','archivo']
"""