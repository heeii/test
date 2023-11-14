import cv2
import mediapipe as mp
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)


def predictions(nparr):
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    znach = ''
    upx = upy = bpx = bpy = razmx1 = razmx2 = razmy1 = razmy2 = 0

    hands = mp.solutions.hands.Hands(static_image_mode=False,
                                     max_num_hands=1,
                                     min_tracking_confidence=0.5,
                                     min_detection_confidence=0.5)
    mpDrow = mp.solutions.drawing_utils
    result = hands.process(image)
    h, w, _ = image.shape
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
        mpDrow.draw_landmarks(image, result.multi_hand_landmarks[0],
                              mp.solutions.hands.HAND_CONNECTIONS)
        razm_o = (((razmx1 - razmx2) ** 2 + (razmy1 - razmy2) ** 2) ** 0.5) * config['mn']
        leng = ((upx - bpx) ** 2 + (upy - bpy) ** 2) ** 0.5
        if leng < razm_o:
            znach = '"Все ОК"'
        else:
            znach = '"Все не ОК"'
    else:
        znach = '"Тут же пусто"'

    image_with_prediction = image.copy()
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(image_with_prediction, znach, (0, 40), font,
                1, color=(255, 0, 0), thickness=2)
    return image_with_prediction
