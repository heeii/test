from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
import numpy as np
import json
import predict
from uvicorn import run

app = FastAPI()

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Настройки CORS для разрешения запросов из любых источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config['allow_origins']],
    allow_credentials=config['allow_credentials'],
    allow_methods=[config['allow_methods']],
    allow_headers=[config['allow_headers']]
)


@app.post("/api/v1/predict")
async def predict(file: UploadFile):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image_with_prediction=predict.predictions(nparr)

        output_path = file.filename

        # Вернуть изображение с разметкой как вложенный файл в ответе
        return FileResponse(str(output_path),
                            headers={"Content-Disposition": f"attachment; filename={file.filename}"})

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    run(app, host=config['host'], port=config['api_port'])

