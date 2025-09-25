import os

# Ruta correcta al archivo de descripciones (nombre con acento y espacio)
DESCRIPCION_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "Descripción Enfermedades.txt")
)

# Mapea nombres de clases del modelo a los encabezados usados en el archivo de descripciones
_CLASES_MAP = {
    'TomatoBacterialspot': 'Tomato___Bacterial_spot',
    'TomatoEarlyblight': 'Tomato___Early_blight',
    'TomatoLateblight': 'Tomato___Late_blight',
    'TomatoSeptorialeafspot': 'Tomato___Septoria_leaf_spot',
    'TomatoTomatoYellowLeafCurlVirus': 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'TomatoTomatomosaicvirus': 'Tomato___Tomato_mosaic_virus',
    'Tomatohealthy': 'Tomato___healthy',
}


def _normalizar_nombre(nombre: str) -> str:
    """Convierte el nombre de clase del modelo al encabezado del archivo de descripciones."""
    if not isinstance(nombre, str):
        return ""
    nombre = nombre.strip()
    if nombre in _CLASES_MAP:
        return _CLASES_MAP[nombre]
    # Si ya viene en el formato del archivo
    if nombre.startswith('Tomato___'):
        return nombre
    return nombre


def obtener_descripcion(nombre_enfermedad: str) -> str:
    """
    Obtiene la descripción de una enfermedad desde el archivo de texto "Descripción Enfermedades.txt".
    Acepta nombres provenientes del modelo (p.ej. "TomatoEarlyblight") o ya formateados
    (p.ej. "Tomato___Early_blight").
    """
    try:
        if not os.path.exists(DESCRIPCION_PATH):
            return "Archivo de descripciones no encontrado."

        objetivo = _normalizar_nombre(nombre_enfermedad)
        if not objetivo:
            return "No hay descripción disponible para esta enfermedad."

        with open(DESCRIPCION_PATH, "r", encoding="utf-8") as f:
            contenido = f.read()

        # Parsear el archivo en secciones, cada una inicia con un encabezado que comienza con "Tomato___"
        secciones = []
        actual = []
        for linea in contenido.splitlines():
            # Inicio de una nueva sección cuando aparece un encabezado
            if linea.startswith("Tomato___"):
                if actual:
                    secciones.append("\n".join(actual).strip())
                    actual = []
            actual.append(linea)
        if actual:
            secciones.append("\n".join(actual).strip())

        # Buscar la sección cuyo encabezado comience con el nombre objetivo
        for sec in secciones:
            lineas = [l for l in sec.splitlines() if l.strip() != ""]
            if not lineas:
                continue
            encabezado = lineas[0].strip()
            if encabezado.startswith(objetivo):
                cuerpo = "\n".join(lineas[1:]).strip()
                return cuerpo if cuerpo else "No hay descripción disponible para esta enfermedad."

        return "No hay descripción disponible para esta enfermedad."

    except Exception as e:
        return f"Error al leer descripción: {str(e)}"
