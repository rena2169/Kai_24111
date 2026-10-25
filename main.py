from fastapi import FastAPI, UploadFile, File
from PIL import Image
import tensorflow as tf
import numpy as np
import io

app = FastAPI(title="AI Image Classifier API")

# 1. Загружаем предобученную модель (MobileNetV2) с весами ImageNet
# При первом запуске она скачается из интернета (около 15 МБ)
print("Загрузка модели... (подождите)")
model = tf.keras.applications.MobileNetV2(weights="imagenet")
print("Модель готова!")


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 2. Читаем загруженный файл
    contents = await file.read()

    # 3. Открываем картинку через Pillow и приводим к нужному размеру (224x224)
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image = image.resize((224, 224))

    # 4. Превращаем картинку в массив чисел (тензор) и добавляем размерность "батча"
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)

    # 5. Нормализуем картинку специально для этой модели
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    # 6. Делаем предсказание
    predictions = model.predict(img_array)

    # 7. Декодируем результат в человекочитаемый вид (топ-3 варианта)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]

    # 8. Формируем красивый JSON-ответ
    results = []
    for _, label, probability in decoded:
        results.append({
            "object": label,
            "probability": round(float(probability) * 100, 2)  # Переводим в проценты
        })

    return {"filename": file.filename, "predictions": results}