import os
import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

API_TOKEN = os.getenv("TELEGRAM_BOT")
BACKEND_URL = "http://localhost:8000/api/v1"
API_KEY = os.getenv("API_KEY")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_data = {}

def get_headers():
    return {"X-API-KEY": API_KEY}

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я ИИ-консультант. Отправь мне текст, голосовое сообщение или картинку.")

@dp.message(Command("clear"))
async def cmd_clear(message: Message):
    user_id = str(message.from_user.id)
    try:
        requests.delete(f"{BACKEND_URL}/history/{user_id}", headers=get_headers())
        await message.answer("Память очищена")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@dp.message(F.text)
async def handle_text(message: Message):
    user_id = str(message.from_user.id)
    await message.bot.send_chat_action(message.chat.id, "typing")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat/text",
            headers=get_headers(),
            data={"user_id": user_id, "text": message.text}
        )
        data = response.json()
        await message.answer(data.get("response", "Ошибка обработки"))
    except Exception as e:
        await message.answer(f"Ошибка соединения: {e}")

@dp.message(F.voice)
async def handle_voice(message: Message):
    user_id = str(message.from_user.id)
    await message.bot.send_chat_action(message.chat.id, "typing")

    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    
    file_on_disk = f"voice_{user_id}.mp3"
    await bot.download_file(file_path, file_on_disk)

    try:
        with open(file_on_disk, "rb") as audio:
            files = {"audio": (file_on_disk, audio, "audio/mpeg")}
            data = {"user_id": user_id}
            
            response = requests.post(
                f"{BACKEND_URL}/chat/audio",
                headers=get_headers(),
                data=data,
                files=files
            )
            res_data = response.json()
            await message.reply(f"🎤 Вы сказали: {res_data.get('transcription')}\n\n🤖 Ответ: {res_data.get('response')}")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
    finally:
        if os.path.exists(file_on_disk):
            os.remove(file_on_disk)

@dp.message(F.photo)
async def handle_photo(message: Message):
    user_id = str(message.from_user.id)
    caption = message.caption or "Опиши это изображение в контексте базы знаний"
    
    await message.bot.send_chat_action(message.chat.id, "typing")
    
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_name = f"photo_{user_id}.jpg"
    await bot.download_file(file.file_path, file_name)

    try:
        with open(file_name, "rb") as img:
            files = {"image": (file_name, img, "image/jpeg")}
            data = {"user_id": user_id, "text": caption}
            
            response = requests.post(
                f"{BACKEND_URL}/chat/text",
                headers=get_headers(),
                data=data,
                files=files
            )
            res_data = response.json()
            await message.answer(res_data.get("response"))
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())