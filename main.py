import os
from dotenv import load_dotenv
import telebot

# Замените на ваш токен
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
    exit(1)

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Обработчик команд (пример)
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Привет! Я бот для конвертации голосовых и видео сообщений в текст.  Когда я получу аудио- или видео-сообщение я представлю тебе его в текстовом формате. Также, ты можешь настроить меня, используя ...")

# Запуск бота
bot.infinity_polling()

