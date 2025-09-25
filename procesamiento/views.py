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
                'imagen_segmentada': segmentado_path.replace(settings.BASE_DIR + os.sep, '').replace('\\', '/'),
                'estado': estado,
                'imagen_enfermedad': enf_path.replace(settings.BASE_DIR + os.sep, '').replace('\\', '/'),
                'clase_enfermedad': clase,
                'descripcion': descripcion
            }

            return render(request, 'procesamiento/resultado.html', contexto)
    else:
        form = SubidaForm()
    return render(request, 'procesamiento/index.html', {'form': form})
