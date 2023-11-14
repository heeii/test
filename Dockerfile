FROM python:3.10
RUN pip install --upgrade pip


RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install opencv-python-headless
RUN pip install mediapipe
RUN pip install python-multipart


WORKDIR /app
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
