import datetime
import hashlib
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import mysql.connector
from config import API_TOKEN,configg

config = configg
connection = None

def hash_combined_values(user_id: str, secret_key: str) -> str:
    """Kullanıcı ID'si ve gizli anahtarı birleştirip hashler."""
    combined_string = f"{user_id}:{secret_key}"
    return hashlib.sha256(combined_string.encode()).hexdigest()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        connection = mysql.connector.connect(**config)
        user = update.message.from_user
        telegramid = hash_combined_values(str(user.id),API_TOKEN)
        print(telegramid)
        username = user.username
        cursor=connection.cursor()
        date = datetime.datetime.now()
        query = "SELECT * FROM user WHERE telegramid = %s"
        cursor.execute(query, (telegramid,))
        result = cursor.fetchone()
        print(result)
        if result is None:
            try:
                print("deneme") 
                query = """
                    INSERT INTO user (telegramid, username, points, click_power,last_login,bar)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (telegramid, username, 0,1,date,100)
                cursor.execute(query, values)
                connection.commit()
            except mysql.connector.Error as err:
                print(f"Hata: {err}")
                connection.rollback()
        url = "https://t.me/MyClickerAPi_bot/myclickerapigame"
        keyboard = [[InlineKeyboardButton("Clicker uygulamasını aç", url=url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Merhaba! Aşağıdaki butona tıklayarak oyunu açabilirsiniz:', reply_markup=reply_markup)
    except Exception as e:
        print(f"Hata oluştu: {e}")


    
def get_user_points(user_id: int):
    connection = mysql.connector.connect(**config)
    cursor=connection.cursor()
    telegramid = hash_combined_values(str(user_id),API_TOKEN)
    print(f"Hashlenmiş Telegram ID: {telegramid}")
    query="SELECT last_login,bar FROM user WHERE telegramid = %s"
    cursor.execute(query,(telegramid,))
    result1=cursor.fetchone()
    print(result1)
    last_login, bar = result1
    db_datetime = last_login
    now_time=datetime.datetime.now()
    difference=now_time-db_datetime
    seconds_difference = int(difference.total_seconds())
    query = "SELECT points,click_power FROM user WHERE telegramid = %s"
    cursor.execute(query, (telegramid,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    print(result)
    if result:
        if bar<100 & 100>seconds_difference & seconds_difference>0:
            bar=bar+seconds_difference
            print(bar)
            points,click_power = result
            return {'points': points, 'click_power': click_power,'bar':bar}
        points,click_power = result
        bar=100
        return {'points': points, 'click_power': click_power,'bar':bar}
    return None

def update_user_points(user_id:int,points:int,clickpower:int,bar:int):
    telegramid = hash_combined_values(user_id,API_TOKEN)
    connection = mysql.connector.connect(**config)
    cursor=connection.cursor()
    now_time=datetime.datetime.now()
    query = "UPDATE user SET points = %s,click_power=%s,last_login=%s,bar=%s WHERE telegramid = %s"
    cursor.execute(query, (points,clickpower,now_time,bar,telegramid))
    connection.commit()
    cursor.close()
    connection.close()
    return 

