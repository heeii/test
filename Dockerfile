# Используйте базовый образ Python
FROM python:3.10

# Установите необходимые зависимости
RUN pip install fastapi uvicorn opencv-python-headless mediapipe

# Копируйте ваш исходный код в контейнер
COPY . .
WORKDIR /app

# Определите порт, на котором ваше приложение будет работать
EXPOSE 8000

# Запустите ваше приложение при запуске контейнера
CMD ["uvicorn", "main:app"]