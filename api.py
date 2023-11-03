import requests
import argparse
from io import BytesIO
import cv2
import json
def main():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    parser = argparse.ArgumentParser(description="Получить предсказания для изображения")
    parser.add_argument("--input", help="Путь к входному изображению")
    parser.add_argument("--output", help="Путь для сохранения изображения с предсказанием")

    args = parser.parse_args()

    input_image_path = args.input
    output_image_path = args.output

    if input_image_path and output_image_path:
        # Отправка изображения на API
        with open(input_image_path, "rb") as image_file:
            files = {"file": ("i.jpg", image_file)}
            response = requests.post(config['app_address'], files=files)

            if response.status_code == 200:
                # Прочитайте изображение с предсказанием
                image_with_prediction = BytesIO(response.content)

                # Сохраните изображение с предсказанием
                with open(output_image_path, "wb") as output_image:
                    output_image.write(image_with_prediction.read())
                # cv2.imshow(output_image)
                print(f"Предсказание успешно сохранено в {output_image_path}")
            else:
                print(f"Ошибка при получении предсказания: {response.text}")
    else:
        print("Укажите пути к входному и выходному изображениям")

if __name__ == "__main__":
    main()