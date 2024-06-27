from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates
import aiofiles
import os

app = FastAPI()

# 정적 파일을 서빙하기 위해 static 디렉토리를 마운트합니다.
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# 업로드된 파일을 저장할 디렉토리를 설정합니다.
UPLOAD_DIR = os.path.join("static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def upload_video(request: Request, file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    async with aiofiles.open(file_location, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    return templates.TemplateResponse("result.html", {"request": request, "file_url": f"/static/uploads/{file.filename}"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
