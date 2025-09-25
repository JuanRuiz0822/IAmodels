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
                    'imagen_segmentada': segmentado_path.replace(settings.BASE_DIR, '').replace('\\', '/'),
                    'estado': estado,
                    'imagen_enfermedad': enf_path.replace(settings.BASE_DIR, '').replace('\\', '/'),
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
