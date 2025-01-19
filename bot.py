import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
from googletrans import Translator
from config import TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Создаем папку для сохранения изображений
if not os.path.exists("img"):
    os.makedirs("img")

# Инициализация переводчика
translator = Translator()


# Хэндлер для команды /start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Я бот. Отправь мне фото, текст или используй команду /help.")


# Хэндлер для команды /help
@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    # Указываем путь к голосовому файлу
    voice_file_path = "voice.ogg"

    # Проверяем, существует ли голосовой файл
    if os.path.exists(voice_file_path):
        with open(voice_file_path, "rb") as voice:
            await bot.send_voice(chat_id=message.chat.id, voice=voice)
    else:
        await message.reply("Файл с голосовым сообщением не найден.")


# Хэндлер для обработки фотографий
@dp.message_handler(content_types=[ContentType.PHOTO])
async def handle_photo(message: types.Message):
    # Получаем файл фотографии
    photo = message.photo[-1]  # Берем фотографию максимального размера
    photo_file = await bot.get_file(photo.file_id)

    # Скачиваем фотографию в папку img
    photo_path = f"img/{photo.file_id}.jpg"
    await bot.download_file(photo_file.file_path, photo_path)

    await message.reply("Фото сохранено!")


# Хэндлер для обработки текстовых сообщений
@dp.message_handler(content_types=[ContentType.TEXT])
async def handle_text(message: types.Message):
    # Перевод текста на английский язык
    translated_text = translator.translate(message.text, src="auto", dest="en").text

    # Отправляем перевод пользователю
    await message.reply(f"Перевод на английский:\n{translated_text}")


# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)