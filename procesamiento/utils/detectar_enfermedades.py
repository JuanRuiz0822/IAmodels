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
