import os
import uvicorn
from fastapi import FastAPI, HTTPException
from service import get_user_points, update_user_points,start_telegram_bot
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm kaynaklara izin vermek için
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP yöntemlerine izin vermek için
    allow_headers=["*"],  # Tüm başlıklara izin vermek için
)


@app.get("/")
async def test():
    return "ok"




if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)