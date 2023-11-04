import os

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from pathlib import Path
import cv2
import numpy as np
import mediapipe as mp
import json
app = FastAPI()
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
# Настройки CORS для разрешения запросов из любых источников (для тестовых целей)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config['allow_origins']],
    allow_credentials=config['allow_credentials'],
    allow_methods=[config['allow_methods']],
    allow_headers=[config['allow_headers']],
    #allow_origins=["*"],
    #allow_credentials=True,
   # allow_methods=["*"],
    #allow_headers=["*"],
)

# Маршрут для получения предсказаний
@app.post("/api/v1/predict")
async def predict(file: UploadFile):
    try:
        # Считать изображение
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        znach=''
        upx = upy = bpx = bpy = razmx1 = razmx2 = razmy1 = razmy2 = 0
        # Обработка изображения (ваш код)
        img = image
        # img = cv2.imread(img)
        hands = mp.solutions.hands.Hands(static_image_mode=False,
                                                         max_num_hands=1,
                                                         min_tracking_confidence=0.5,
                                                         min_detection_confidence=0.5)
        mpDrow = mp.solutions.drawing_utils
        result = hands.process(img)
        h, w, _ = img.shape
        if result.multi_hand_landmarks:
            for id, lm in enumerate(result.multi_hand_landmarks[0].landmark):

                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 8:
                    upx = cx
                    upy = cy
                if id == 4:
                    bpx = cx
                    bpy = cy
                if id == 6:
                    razmx1 = cx
                    razmy1 = cy
                if id == 7:
                    razmx2 = cx
                    razmy2 = cy
            mpDrow.draw_landmarks(img, result.multi_hand_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS,)
            razm_o = (((razmx1 - razmx2) ** 2 + (razmy1 - razmy2) ** 2) ** 0.5) * config['mn']
            leng = ((upx - bpx) ** 2 + (upy - bpy) ** 2) ** 0.5
            if leng < razm_o:
                znach='"Все ОК"'
            else:
                znach='"Все не ОК"'
        else:
            znach='"Тут же пусто"'
        image=img


        # В данном примере просто добавляем надпись "Предсказание" на изображение
        image_with_prediction = image.copy()
        #cv2.putText(image_with_prediction, znach, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_COMPLEX
        # вставка текста синего цвета
        cv2.putText(image_with_prediction, znach, (0, 40), font, 1, color=(255, 0, 0), thickness=2)
        # Сохранить изображение с разметкой во временный файл
        output_path = file.filename
        cv2.imwrite(str(output_path), image_with_prediction)
        # cv2.imshow(image_with_prediction)
        # Вернуть изображение с разметкой как вложенный файл в ответе
        return FileResponse(str(output_path), headers={"Content-Disposition": f"attachment; filename={file.filename}"})
        os.remove('i.jpg')
    except Exception as e:
        return {"error": str(e)}
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config[8000], port=config['api_port'])
    os.remove('i.jpg')
