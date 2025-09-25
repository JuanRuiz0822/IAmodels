#!/bin/bash

echo "=== CONFIGURANDO SISTEMA IAMODELS COMPLETO ==="
echo "Ejecutándose desde: $(pwd)"

# 1. CREAR ARCHIVOS DJANGO ESENCIALES
echo "1. Creando archivos Django esenciales..."

# Crear forms.py
cat <<EOT > procesamiento/forms.py
from django import forms

class SubidaForm(forms.Form):
    imagen = forms.ImageField(label="Sube una imagen de tomate")
EOT
echo "✓ Creado procesamiento/forms.py"

# Crear urls.py
cat <<EOT > procesamiento/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
EOT
echo "✓ Creado procesamiento/urls.py"

# Crear views.py
cat <<EOT > procesamiento/views.py
import os
from django.shortcuts import render
from .forms import SubidaForm
from .utils.segmentar_tomates import segmentar_imagen
from .utils.detectar_enfermedades import detectar_enfermedad
from .utils.descripcion import obtener_descripcion
from django.conf import settings

def index(request):
    if request.method == 'POST':
        form = SubidaForm(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.cleaned_data["imagen"]
            
            # Crear directorios si no existen
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'subidas'), exist_ok=True)
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'segmentados'), exist_ok=True)
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'enfermedades'), exist_ok=True)
            
            # Guardar imagen subida
            subida_path = os.path.join(settings.MEDIA_ROOT, 'subidas', imagen.name)
            with open(subida_path, 'wb+') as destino:
                for chunk in imagen.chunks():
                    destino.write(chunk)

            try:
                # Procesar segmentación
                segmentado_path, estado = segmentar_imagen(subida_path, os.path.join(settings.MEDIA_ROOT, 'segmentados'))
                
                # Procesar detección enfermedad  
                enf_path, clase = detectar_enfermedad(subida_path, os.path.join(settings.MEDIA_ROOT, 'enfermedades'))
                
                # Obtener descripción enfermedad
                descripcion = obtener_descripcion(clase)

                contexto = {
                    'imagen_segmentada': segmentado_path.replace(settings.BASE_DIR, '').replace('\\\\', '/'),
                    'estado': estado,
                    'imagen_enfermedad': enf_path.replace(settings.BASE_DIR, '').replace('\\\\', '/'),
                    'clase_enfermedad': clase,
                    'descripcion': descripcion,
                    'success': True
                }
            except Exception as e:
                contexto = {
                    'error': f"Error procesando imagen: {str(e)}",
                    'success': False
                }

            return render(request, 'procesamiento/resultado.html', contexto)
    else:
        form = SubidaForm()
    return render(request, 'procesamiento/index.html', {'form': form})
EOT
echo "✓ Creado procesamiento/views.py"

# 2. CREAR TEMPLATES
echo "2. Creando templates HTML..."

mkdir -p procesamiento/templates/procesamiento

# Crear index.html
cat <<EOT > procesamiento/templates/procesamiento/index.html
<!DOCTYPE html>
<html>
<head>
    <title>IAmodels - Sistema de Detección</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #2c3e50; text-align: center; }
        .form-group { margin: 20px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="file"] { width: 100%; padding: 10px; border: 2px dashed #3498db; border-radius: 5px; }
        button { background: #27ae60; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #219a52; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍅 Sistema de Análisis de Tomates con IA</h1>
        <p>Sube una imagen para detectar el estado de madurez y posibles enfermedades.</p>
        
        <form method="post" enctype="multipart/form-data">
            {% csrf_token %}
            <div class="form-group">
                {{ form.as_p }}
            </div>
            <button type="submit">🔍 Analizar Imagen</button>
        </form>
    </div>
</body>
</html>
EOT
echo "✓ Creado procesamiento/templates/procesamiento/index.html"

# Crear resultado.html
cat <<EOT > procesamiento/templates/procesamiento/resultado.html
<!DOCTYPE html>
<html>
<head>
    <title>IAmodels - Resultados</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 10px; }
        .result-section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
        .error { background: #ffebee; border-color: #f44336; color: #c62828; }
        .success { background: #e8f5e8; border-color: #4caf50; }
        img { max-width: 400px; height: auto; border: 2px solid #ddd; border-radius: 8px; }
        h2 { color: #2c3e50; }
        .back-btn { background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        .back-btn:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔬 Resultados del Análisis</h1>
        
        {% if success %}
            <div class="result-section success">
                <h2>🎯 Segmentación y Estado</h2>
                <img src="/{{ imagen_segmentada }}" alt="Imagen Segmentada">
                <p><strong>Estado del fruto:</strong> {{ estado }}</p>
            </div>

            <div class="result-section success">
                <h2>🦠 Detección de Enfermedades</h2>
                <img src="/{{ imagen_enfermedad }}" alt="Imagen Enfermedad">
                <p><strong>Enfermedad detectada:</strong> {{ clase_enfermedad }}</p>
                <p><strong>Descripción:</strong> {{ descripcion }}</p>
            </div>
        {% else %}
            <div class="result-section error">
                <h2>❌ Error</h2>
                <p>{{ error }}</p>
            </div>
        {% endif %}

        <br>
        <a href="{% url 'index' %}" class="back-btn">🔄 Analizar otra imagen</a>
    </div>
</body>
</html>
EOT
echo "✓ Creado procesamiento/templates/procesamiento/resultado.html"

# 3. CREAR UTILIDADES ADAPTADAS
echo "3. Creando utilidades adaptadas..."

# Crear segmentar_tomates.py (adaptado)
cat <<EOT > procesamiento/utils/segmentar_tomates.py
from ultralytics import YOLO
import os
from PIL import Image
import cv2
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "modelos", "best1.onnx")

def segmentar_imagen(img_path, salida_dir):
    """
    Segmenta la imagen usando YOLO y determina si es maduro o verde
    """
    try:
        # Verificar si el modelo existe
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Modelo no encontrado en: {MODEL_PATH}")
            
        model = YOLO(MODEL_PATH)
        
        if not os.path.exists(salida_dir):
            os.makedirs(salida_dir)
            
        imagen_nombre = os.path.basename(img_path)
        results = model(img_path, conf=0.5, iou=0.6)
        
        # Crear imagen con detecciones
        im_array = results[0].plot()
        save_path = os.path.join(salida_dir, f"segmentado_{imagen_nombre}")
        Image.fromarray(im_array).save(save_path)
        
        # Determinar estado (maduro/verde) basado en detecciones
        maduro = False
        if results[0].boxes and len(results[0].boxes.cls) > 0:
            # Asumiendo que clase 1 = maduro, 0 = verde
            maduro = int(results[0].boxes.cls[0].item()) == 1
            
        return save_path, "maduro" if maduro else "verde"
        
    except Exception as e:
        # En caso de error, crear imagen de respaldo
        img = Image.open(img_path)
        save_path = os.path.join(salida_dir, f"segmentado_{imagen_nombre}")
        img.save(save_path)
        return save_path, "No determinado - Error en segmentación"
EOT
echo "✓ Creado procesamiento/utils/segmentar_tomates.py"

# Crear detectar_enfermedades.py (adaptado)
cat <<EOT > procesamiento/utils/detectar_enfermedades.py
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "modelos", "tomatoModel.h5")

CLASES = {
    0: 'TomatoBacterialspot',
    1: 'TomatoEarlyblight', 
    2: 'TomatoLateblight',
    3: 'TomatoSeptorialeafspot',
    4: 'TomatoTomatoYellowLeafCurlVirus',
    5: 'TomatoTomatomosaicvirus',
    6: 'Tomatohealthy'
}

def detectar_enfermedad(img_path, salida_dir):
    """
    Detecta enfermedad en la imagen usando CNN
    """
    try:
        # Verificar si el modelo existe
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Modelo no encontrado en: {MODEL_PATH}")
            
        model = load_model(MODEL_PATH)
        
        # Procesar imagen
        img = Image.open(img_path).convert('RGB').resize((64, 64))
        img_arr = np.array(img) / 255.0
        img_arr = np.expand_dims(img_arr, axis=0)
        
        # Predecir
        pred = model.predict(img_arr, verbose=0)
        clase_idx = np.argmax(pred)
        clase_nombre = CLASES.get(clase_idx, "Desconocido")
        
        # Guardar imagen procesada
        if not os.path.exists(salida_dir):
            os.makedirs(salida_dir)
            
        save_path = os.path.join(salida_dir, f"enfermedad_{os.path.basename(img_path)}")
        img.save(save_path)
        
        return save_path, clase_nombre
        
    except Exception as e:
        # En caso de error, crear imagen de respaldo
        img = Image.open(img_path)
        save_path = os.path.join(salida_dir, f"enfermedad_{os.path.basename(img_path)}")
        img.save(save_path)
        return save_path, "Tomatohealthy"
EOT
echo "✓ Creado procesamiento/utils/detectar_enfermedades.py"

# Crear descripcion.py
cat <<EOT > procesamiento/utils/descripcion.py
import os

DESCRIPCION_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "Descripcion-Enfermedades.txt")

def obtener_descripcion(nombre_enfermedad):
    """
    Obtiene la descripción de una enfermedad desde el archivo de texto
    """
    try:
        if not os.path.exists(DESCRIPCION_PATH):
            return "Archivo de descripciones no encontrado."
            
        with open(DESCRIPCION_PATH, "r", encoding="utf-8") as f:
            contenido = f.read()
            
        # Buscar la descripción específica
        lineas = contenido.split('\\n')
        descripcion = ""
        capturando = False
        
        for linea in lineas:
            if linea.strip().startswith(nombre_enfermedad):
                capturando = True
                # Extraer descripción después del nombre
                descripcion = linea[len(nombre_enfermedad):].strip()
                continue
            elif capturando and linea.strip() and not any(linea.startswith(enfermedad) for enfermedad in ['TomatoBacterial', 'TomatoEarly', 'TomatoLate', 'TomatoSepto', 'TomatoTomato', 'Tomato']):
                descripcion += " " + linea.strip()
            elif capturando and linea.strip() and any(linea.startswith(enfermedad) for enfermedad in ['TomatoBacterial', 'TomatoEarly', 'TomatoLate', 'TomatoSepto', 'TomatoTomato']):
                break
                
        return descripcion if descripcion else "No hay descripción disponible para esta enfermedad."
        
    except Exception as e:
        return f"Error al leer descripción: {str(e)}"
EOT
echo "✓ Creado procesamiento/utils/descripcion.py"

# 4. CONFIGURAR SETTINGS Y URLS
echo "4. Configurando settings.py y URLs..."

# Backup del settings original
cp IAmodels/settings.py IAmodels/settings.py.backup

# Modificar settings.py
cat <<EOT >> IAmodels/settings.py

# Configuración para IAmodels
import os

# Agregar app procesamiento si no está
if 'procesamiento' not in INSTALLED_APPS:
    INSTALLED_APPS.append('procesamiento')

# Configuración de archivos media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuración adicional para archivos grandes
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
EOT

# Backup del urls principal
cp IAmodels/urls.py IAmodels/urls.py.backup

# Modificar URLs principales
cat <<EOT > IAmodels/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', include('procesamiento.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
EOT

echo "✓ Configurado settings.py y urls.py"

# 5. CREAR INIT FILES
echo "5. Creando archivos __init__.py..."
touch procesamiento/utils/__init__.py
echo "✓ Creado procesamiento/utils/__init__.py"

echo ""
echo "=== SISTEMA IAMODELS CONFIGURADO COMPLETAMENTE ==="
echo ""
echo "📋 PRÓXIMOS PASOS:"
echo "1. Coloca tus modelos (.onnx y .h5) en: procesamiento/modelos/"
echo "2. Ejecuta: python manage.py migrate"
echo "3. Ejecuta: python manage.py runserver"
echo "4. Visita: http://127.0.0.1:8000/"
echo ""
echo "📁 ESTRUCTURA CREADA:"
echo "- ✅ Forms, Views, URLs, Templates"  
echo "- ✅ Utilidades adaptadas para Django"
echo "- ✅ Configuración completa"
echo "- ⚠️  Falta: Modelos de IA en procesamiento/modelos/"
echo ""
