import asyncio
import nest_asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from telegram.ext import Application, CommandHandler
from service import start
from service import get_user_points, update_user_points
from fastapi.middleware.cors import CORSMiddleware
from config import API_TOKEN

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm kaynaklara izin vermek için
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP yöntemlerine izin vermek için
    allow_headers=["*"],  # Tüm başlıklara izin vermek için
)
async def start_telegram_bot() -> None:
    application = Application.builder().token(API_TOKEN).build()
    start_handler = CommandHandler('start',start)
    application.add_handler(start_handler)
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

@app.get("/")
def test():
    return "deneme"

@app.get("/pointsAndClickPower/{user_id}")
async def get_points(user_id: int):
    result = get_user_points(user_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/update-points")
def update_points(telegramid:int,points:int,clickpower:int,bar:int):
    update_user_points(telegramid,points,clickpower,bar)
    return {"message": "Points updated successfully"}
   

async def start_fastapi():
    config = uvicorn.Config("main:app", port=8000, reload=True)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(
        start_fastapi(),
        start_telegram_bot(),
    )  

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
    
    