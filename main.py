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
    # await start_telegram_bot()
    return "ok"

# @app.get("/pointsAndClickPower/{user_id}")
# async def get_points(user_id: int):
#     result = get_user_points(user_id)
#     if result:
#         return result
#     raise HTTPException(status_code=404, detail="User not found")

# @app.get("/update-points")
# def update_points(telegramid: int, points: int, clickpower: int, bar: int):
#     update_user_points(telegramid, points, clickpower, bar)
#     return {"message": "Points updated successfully"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)