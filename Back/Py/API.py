from translate import get_translate_google, get_translate_wooo
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Python Flask/FastAPI сервер
app = FastAPI()

# Класс перевода
class TranslateRequest(BaseModel):
    text: str

# Заголовки что бы можно было передавать данные внутри запроса
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники
    allow_methods=["*"],  # Разрешить POST, GET, etc.
    allow_headers=["*"],  # Разрешить JSON заголовки
)

@app.post("/translate/google")
async def translate(request: TranslateRequest):
    result = await get_translate_google(request.text)
    return {"google": result}

@app.post("/translate/wooordhunt")
async def translate(request: TranslateRequest):
    result = await get_translate_wooo(request.text)
    return {"wooordhunt": result}

@app.post("/ping")
async def ping():
    return {}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="78.40.211.69", port=6767)
