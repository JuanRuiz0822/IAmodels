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
            accion = request.POST.get("accion", "segmentacion")

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
                media_base = settings.MEDIA_URL.strip('/') or 'media'
                contexto = {'success': True}

                if accion == "segmentacion":
                    # Ejecutar solo segmentación
                    segmentado_path, estado = segmentar_imagen(
                        subida_path, os.path.join(settings.MEDIA_ROOT, 'segmentados')
                    )
                    seg_rel = os.path.relpath(segmentado_path, settings.MEDIA_ROOT).replace('\\', '/')
                    contexto.update({
                        'imagen_segmentada': f"{media_base}/{seg_rel.lstrip('/')}",
                        'estado': estado,
                        'mostrar_segmentacion': True,
                        'mostrar_enfermedad': False,
                    })
                elif accion == "enfermedad":
                    # Ejecutar solo detección de enfermedad
                    enf_path, clase = detectar_enfermedad(
                        subida_path, os.path.join(settings.MEDIA_ROOT, 'enfermedades')
                    )
                    descripcion = obtener_descripcion(clase)
                    enf_rel = os.path.relpath(enf_path, settings.MEDIA_ROOT).replace('\\', '/')
                    contexto.update({
                        'imagen_enfermedad': f"{media_base}/{enf_rel.lstrip('/')}",
                        'clase_enfermedad': clase,
                        'descripcion': descripcion,
                        'mostrar_segmentacion': False,
                        'mostrar_enfermedad': True,
                    })
                else:
                    # Si no se envía acción válida, ejecutar ambos por compatibilidad
                    segmentado_path, estado = segmentar_imagen(
                        subida_path, os.path.join(settings.MEDIA_ROOT, 'segmentados')
                    )
                    enf_path, clase = detectar_enfermedad(
                        subida_path, os.path.join(settings.MEDIA_ROOT, 'enfermedades')
                    )
                    descripcion = obtener_descripcion(clase)
                    seg_rel = os.path.relpath(segmentado_path, settings.MEDIA_ROOT).replace('\\', '/')
                    enf_rel = os.path.relpath(enf_path, settings.MEDIA_ROOT).replace('\\', '/')
                    contexto.update({
                        'imagen_segmentada': f"{media_base}/{seg_rel.lstrip('/')}",
                        'estado': estado,
                        'imagen_enfermedad': f"{media_base}/{enf_rel.lstrip('/')}",
                        'clase_enfermedad': clase,
                        'descripcion': descripcion,
                        'mostrar_segmentacion': True,
                        'mostrar_enfermedad': True,
                    })

            except Exception as e:
                contexto = {
                    'error': f"Error procesando imagen: {str(e)}",
                    'success': False
                }

            return render(request, 'procesamiento/resultado.html', contexto)
    else:
        form = SubidaForm()
    return render(request, 'procesamiento/index.html', {'form': form})
