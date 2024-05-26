from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import os
from io import BytesIO
from setting import SETTINGS

app = FastAPI()

# 指定圖片保存路徑
UPLOAD_DIRECTORY = SETTINGS.upload_path

# 如果保存路徑不存在，則創建它
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.post("/v1/rune-break/image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # 讀取文件內容
        contents = await file.read()

        # 將文件內容轉換為 PIL Image 對象
        image = Image.open(BytesIO(contents))

        # 保存圖片到本地文件系統
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        image.save(file_path)

        return JSONResponse(content={"answer": "wsad"}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=32980)