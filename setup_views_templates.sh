#!/bin/bash

# Crear forms.py
cat <<EOT > procesamiento/forms.py
from django import forms

class SubidaForm(forms.Form):
    imagen = forms.ImageField(label="Sube una imagen")
EOT

echo "Creado procesamiento/forms.py"

# Crear urls.py
cat <<EOT > procesamiento/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
EOT

echo "Creado procesamiento/urls.py"

# Crear views.py
cat <<EOT > procesamiento/views.py
import os
from django.shortcuts import render
from .forms import SubidaForm
from .utils.Segmentar_tomates import segmentar_imagen
from .utils.detectar_enfermedades import detectar_enfermedad
from .utils.descripcion import obtener_descripcion
from django.conf import settings

def index(request):
    if request.method == 'POST':
        form = SubidaForm(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.cleaned_data["imagen"]
            subida_path = os.path.join(settings.MEDIA_ROOT, 'subidas', imagen.name)
            with open(subida_path, 'wb+') as destino:
                for chunk in imagen.chunks():
                    destino.write(chunk)

            segmentado_path, estado = segmentar_imagen(subida_path, os.path.join(settings.MEDIA_ROOT, 'segmentados'))
            enf_path, clase = detectar_enfermedad(subida_path, os.path.join(settings.MEDIA_ROOT, 'enfermedades'))
            descripcion = obtener_descripcion(clase)

            contexto = {
                'imagen_segmentada': segmentado_path.replace(settings.BASE_DIR + os.sep, '').replace('\\\\', '/'),
                'estado': estado,
                'imagen_enfermedad': enf_path.replace(settings.BASE_DIR + os.sep, '').replace('\\\\', '/'),
                'clase_enfermedad': clase,
                'descripcion': descripcion
            }

            return render(request, 'procesamiento/resultado.html', contexto)
    else:
        form = SubidaForm()
    return render(request, 'procesamiento/index.html', {'form': form})
EOT

echo "Creado procesamiento/views.py"

# Crear carpeta para templates
mkdir -p procesamiento/templates/procesamiento

# Crear index.html
cat <<EOT > procesamiento/templates/procesamiento/index.html
<!DOCTYPE html>
<html>
<head>
    <title>IA Models - Subida</title>
</head>
<body>
    <h2>Sube una imagen para procesar</h2>
    <form method="post" enctype="multipart/form-data">{% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Procesar</button>
    </form>
</body>
</html>
EOT

echo "Creado procesamiento/templates/procesamiento/index.html"

# Crear resultado.html
cat <<EOT > procesamiento/templates/procesamiento/resultado.html
<!DOCTYPE html>
<html>
<head>
    <title>IA Models - Resultado</title>
</head>
<body>
    <h2>Segmentación</h2>
    <img src="/{{ imagen_segmentada }}" alt="Imagen Segmentada" width="400">
    <p>Estado del fruto: {{ estado }}</p>

    <h2>Enfermedades</h2>
    <img src="/{{ imagen_enfermedad }}" alt="Imagen Enfermedad" width="400">
    <p>Enfermedad detectada: {{ clase_enfermedad }}</p>
    <p>Descripción: {{ descripcion }}</p>

    <br>
    <a href="{% url 'index' %}">Procesar otra imagen</a>
</body>
</html>
EOT

echo "Creado procesamiento/templates/procesamiento/resultado.html"

echo "Archivos Django esenciales creados."
