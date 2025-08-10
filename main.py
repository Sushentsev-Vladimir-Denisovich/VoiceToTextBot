import os
from dotenv import load_dotenv
import telebot
import whisper
import constants

load_dotenv()
# Считывание токена из файла .env
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    print(constants.TOKEN_NOT_SET)
    exit(1)

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

#Загрузка модели Whisper
model = whisper.load_model("small") # Можно указать другую модель: "small", "medium", "large", "large-v2"

# Обработчик команды "/start"
@bot.message_handler(commands=['start'])
def handle_start(message):
    print("start")
    bot.reply_to(message, constants.START_MESSAGE)

# Обработчик голосовых сообщений
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    print("voice")
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    # Скачивание файла
    downloaded_file = bot.download_file(file_path)

    # Сохранение файла во временный файл
    with open(constants.TEMP_AUDIO_FILE_NAME, "wb") as new_file:
        new_file.write(downloaded_file)

    try:
        audio = whisper.load_audio(constants.TEMP_AUDIO_FILE_NAME)
        result = model.transcribe(audio)
        text = result["text"]

        # Удаление начального и конечного пробелов
        text = text.strip()
        
        # Разбиваем текст на части размером не более 4096 символов
        chunks = [text[i:i + 4096] for i in range(0, len(text), 4096)]

        # Получение автора сообщения и шаблона текста для ответа
        author = get_author(message)
        if author:
            message_text = f"Сообщение от {author}:\n"
        else:
            message_text = message_text = "Распознанный текст:\n"
        
        # Формирование сообщения с HTML-форматированием
        for chunk in chunks:
            message_text += f"<pre>{chunk}</pre>\n"

        bot.reply_to(message, message_text, parse_mode="HTML") # Указываем parse_mode

        #bot.reply_to(message, f"Распознанный текст:\n'''{text}'''\n", parse_mode='Markdown')

    except Exception as e:
        bot.reply_to(message, f"Ошибка при обработке голосового сообщения:\n\n{e}")
    finally:
        # Удаление временного файла
        os.remove(constants.TEMP_AUDIO_FILE_NAME)

# Обработчик видео сообщений (кружки)
@bot.message_handler(content_types=['video_note'])
def handle_video(message):
    bot.reply_to(message, "video_note")

# Получение автора сообщения (какой-либо сущности, позволяющей отличать отправившего сообщение от других)
def get_author(message):
    user = message.from_user

    # Проверяем наличие имени
    author = user.first_name
    if author:
        return author
    
    # Проверяем наличие юзернейма
    author = user.username
    if author:
        return f"@{author}"
    
    return author

# Запуск бота
bot.infinity_polling()

