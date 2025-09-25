Coloque aquí los modelos entrenados para ejecución local:

- best1.onnx  (modelo de segmentación YOLO)
- tomatoModel.h5  (modelo de clasificación de enfermedades)

Rutas esperadas por el sistema:
- Segmentación: procesamiento/utils/modelos/best1.onnx
- Enfermedades: procesamiento/utils/modelos/tomatoModel.h5

Si estos archivos no existen, al procesar una imagen se mostrará un error indicando la ruta faltante.
