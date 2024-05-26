from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import os
from io import BytesIO
from setting import SETTINGS
from preprocessing.laplace import laplace_inference
from preprocessing.preprocessor import cut_arrows_inference
from typing import List
from inference.inference import predict
from logger import logger

app = FastAPI()

# image store directory
UPLOAD_DIRECTORY = SETTINGS.upload_path
INFERENCE_TMP_DIRECTORY = SETTINGS.inference_tmp

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
if not os.path.exists(INFERENCE_TMP_DIRECTORY):
    os.makedirs(INFERENCE_TMP_DIRECTORY)

@app.post("/v1/rune-break/image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Get image content
        contents = await file.read()
        image = Image.open(BytesIO(contents))

        # Store raw image to directory
        file_path: str = os.path.join(UPLOAD_DIRECTORY, file.filename)
        image.save(file_path)

        # Do inference
        # 1. Laplace
        lap_file_path = laplace_inference(file.filename, INFERENCE_TMP_DIRECTORY)

        # 2. Cut 4  and get path
        arrows = cut_arrows_inference(lap_file_path)

        # 3. Input image to model
        label_map = {0: 'w', 1: 's', 2: 'a', 3: 'd'}
        result: str = ""
        for arrow in arrows:
            predicted_label = predict(arrow)
            result += label_map[predicted_label]
            logger.info(f"Inference: {arrow} - {label_map[predicted_label]}")

        logger.info(f"Predict: {result}")
        return JSONResponse(content={"answer": result}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=32980)