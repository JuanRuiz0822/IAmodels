#Detectar enfermedades en hojas de plantas de tomate.
# =================================================================
# 1. CONFIGURACIÓN
# =================================================================

# --- ¡MODIFICA ESTAS DOS LÍNEAS! ---
#MODEL_PATH = '/content/drive/MyDrive/Grupo 2 Fitopatologia/tomatoModel'
MODEL_PATH = '/content/drive/MyDrive/Grupo 2 Fitopatologia/CNN-7_Model64.h5'
IMAGE_PATH = '/content/drive/MyDrive/Grupo 2 Fitopatologia/test/Tomato___Tomato_Yellow_Leaf_Curl_Virus/0a3d19ca-a126-4ea3-83e3-0abb0e9b02e3___YLCV_GCREC 2449_FlipTB.JPG'

# --- PARÁMETROS DEL MODELO (NO MODIFICAR SI NO ES NECESARIO) ---
# Dimensiones de la imagen con las que se entrenó el modelo
IMG_DIMENSIONS = (64, 64)

# El diccionario de clases correcto que proporcionaste
CLASS_INDICES = {
    'Tomato___Bacterial_spot': 0,
    'Tomato___Early_blight': 1,
    'Tomato___Late_blight': 2,
    'Tomato___Septoria_leaf_spot': 3,
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 4,
    'Tomato___Tomato_mosaic_virus': 5,
    'Tomato___healthy': 6
}

# =================================================================
# 2. EJECUCIÓN DEL SCRIPT
# =================================================================

try:
    # --- Cargar el modelo entrenado ---
    print(f"  Cargando modelo desde: {MODEL_PATH}")
    model = load_model(MODEL_PATH)
    print(" ¡Modelo cargado exitosamente!")

    # --- Cargar y mostrar la imagen ---
    print(f"\n  Cargando imagen desde: {IMAGE_PATH}")
    if not os.path.exists(IMAGE_PATH):
        raise FileNotFoundError(f"No se encontró la imagen en la ruta especificada.")
    display(IPImage(filename=IMAGE_PATH, width=300))

    # --- Preprocesar la imagen ---
    img = image.load_img(IMAGE_PATH, target_size=IMG_DIMENSIONS)
    img_array = image.img_to_array(img)
    img_array /= 255.0  # Normalización
    img_batch = np.expand_dims(img_array, axis=0) # Añadir dimensión de lote

    # --- Realizar la clasificación ---
    print("\n🧠  Clasificando la imagen...")
    predictions = model.predict(img_batch)

    # --- Interpretar y mostrar el resultado ---
    predicted_index = np.argmax(predictions[0])
    confidence = np.max(predictions[0]) * 100

    # Mapear el índice a la etiqueta de clase
    class_labels = {v: k for k, v in CLASS_INDICES.items()}
    predicted_class_name = class_labels[predicted_index]

    print("\n--- 🎯 RESULTADO DE LA CLASIFICACIÓN ---")
    print(f"**Clase Predicha:** {predicted_class_name.replace('___', ' ')}")
    print(f"**Confianza:** {confidence:.2f}%")


except Exception as e:
    print(f"\n--- ❌ OCURRIÓ UN ERROR ---")
    print(e)
