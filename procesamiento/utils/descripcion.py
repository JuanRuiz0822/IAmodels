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
        lineas = contenido.split('\n')
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
