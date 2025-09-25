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
    imagen_nombre = os.path.basename(img_path)
    try:
        # Verificar si el modelo existe
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Modelo no encontrado en: {MODEL_PATH}")
            
        model = YOLO(MODEL_PATH)
        
        if not os.path.exists(salida_dir):
            os.makedirs(salida_dir)
            
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
        os.makedirs(salida_dir, exist_ok=True)
        img = Image.open(img_path).convert('RGB')
        save_path = os.path.join(salida_dir, f"segmentado_{imagen_nombre}")
        img.save(save_path)
        return save_path, "No determinado - Error en segmentación"
