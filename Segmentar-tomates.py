#Segmentar tomates maduros y verdes
# --- 1. Cargar el modelo YOLO ---
model_path = '/content/drive/MyDrive/Semilleros_2025/Modelos-finales23-09-2025/best(1).onnx'
try:
    model = YOLO(model_path)
    print("Modelo cargado exitosamente.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")

# --- 2. Procesar una sola imagen de prueba ---
# Define la ruta específica a la imagen que deseas procesar
img_path = '/content/drive/MyDrive/Semilleros_2025/Modelos-finales23-09-2025/test/images/unriped_tomato_58.jpeg'
save_dir = '/content/drive/MyDrive/Semilleros_2025/Modelos-finales23-09-2025/working'
os.makedirs(save_dir, exist_ok=True)

# Obtiene el nombre del archivo de la ruta para el guardado
single_image_name = os.path.basename(img_path)

print(f"Procesando la imagen: {single_image_name}")

try:
    # Realiza la detección de objetos usando el modelo
    results = model(img_path, conf=0.5, iou=0.6)

    # Obtiene el resultado de la primera y única imagen en la lista de resultados
    r = results[0]

    # Dibuja las predicciones en la imagen
    im_array = r.plot()

    # Define la ruta para guardar la imagen procesada
    save_path = os.path.join(save_dir, f'predicted_{single_image_name}')

    # Guarda la imagen con las predicciones
    cv2.imwrite(save_path, im_array)

    # Muestra la imagen guardadabest(1).onnx
    display(Image.open(save_path))
    print(f"Imagen procesada guardada en: {save_path}")

except FileNotFoundError:
    print(f"Error: La imagen '{img_path}' no se encuentra. Verifica que la ruta y el nombre del archivo sean correctos.")
