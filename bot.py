import os
import sys
from dotenv import load_dotenv
import telebot
import whisper
import constants
import methods

load_dotenv()
# Считывание токена из файла .env
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    print(constants.TOKEN_NOT_SET)
    sys.exit(1)

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

#Загрузка модели Whisper
whisper_model = whisper.load_model("small") # Можно указать другую модель: "small", "medium", "large", "large-v2"

# Обработчик команды "/start"
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, constants.START_MESSAGE)

# Обработчик голосовых сообщений
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    methods.convert_voice_to_text_and_reply(whisper, whisper_model, bot, message)

# Обработчик видео сообщений (кружки)
@bot.message_handler(content_types=['video_note'])
def handle_video(message):
    methods.convert_voice_to_text_and_reply(whisper, whisper_model, bot, message)

# Запуск бота
bot.infinity_polling()

