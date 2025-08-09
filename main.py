import os
from dotenv import load_dotenv
import telebot

load_dotenv()
# Считывание токена из файла .env
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
    exit(1)

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Обработчик команды "/start"
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Привет! Я бот для конвертации голосовых и видео сообщений в текст.  Когда я получу аудио- или видео-сообщение я представлю тебе его в текстовом формате. Также, ты можешь настроить меня, используя ...")

# Обработчик голосовых сообщений
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    bot.reply_to(message, "voice")

# Обработчик видео сообщений (кружки)
@bot.message_handler(content_types=['video_note'])
def handle_video(message):
    bot.reply_to(message, "video_note")

# Запуск бота
bot.infinity_polling()

