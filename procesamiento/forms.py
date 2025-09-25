from django import forms

class SubidaForm(forms.Form):
    imagen = forms.ImageField(label="Sube una imagen")
