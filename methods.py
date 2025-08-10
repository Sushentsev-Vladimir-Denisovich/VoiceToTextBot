from moviepy import VideoFileClip
import os
import constants

# Преобразование голоса в текст (универсально для аудио и видео сообщений)
def convert_voice_to_text_and_reply(whisper, whisper_model, bot, message):
    if message.content_type == "voice":
        # Обработка голосового сообщения
        downloaded_file = download_file(bot, message.voice.file_id)
        # Сохранение файла во временный файл
        with open(constants.TEMP_AUDIO_FILE_NAME, "wb") as new_file:
            new_file.write(downloaded_file)
    elif message.content_type == "video_note":
        # Обработка видеосообщения
        downloaded_file = downloaded_file = download_file(bot, message.video_note.file_id)
        with open(constants.TEMP_VIDEO_FILE_NAME, "wb") as new_file:
            new_file.write(downloaded_file)

        # Извлечение аудио из видео
        try:
            video = VideoFileClip(constants.TEMP_VIDEO_FILE_NAME)
            audio = video.audio
            audio.write_audiofile(constants.TEMP_AUDIO_FILE_NAME)
            video.close()
            os.remove(constants.TEMP_VIDEO_FILE_NAME)  # Удаляем временный видеофайл
        except Exception as e:
            bot.reply_to(message, f"Ошибка при извлечении аудио из видео:\n{e}")
            return
    else:
        bot.reply_to(message, f"Ошибка при извлечении аудио из видео:\n{e}")
        return
    try:
        audio = whisper.load_audio(constants.TEMP_AUDIO_FILE_NAME)
        result = whisper_model.transcribe(audio)
        text = result["text"]

        # Удаление начального и конечного пробелов
        text = text.strip()
        
        # Разбиваем текст на части размером не более 4096 символов
        chunks = [text[i:i + 4096] for i in range(0, len(text), 4096)]

        # Получение автора сообщения и шаблона текста для ответа
        author = get_author(message)
        if author:
            message_text = f"Сообщение от <u>{author}</u>:\n"
        else:
            message_text = message_text = "Распознанный текст:\n"
        
        # Формирование сообщения с HTML-форматированием
        for chunk in chunks:
            message_text += f"<pre>{chunk}</pre>\n"

        bot.reply_to(message, message_text, parse_mode="HTML") # Указываем parse_mode

    except Exception as e:
        bot.reply_to(message, f"Ошибка при обработке голосового сообщения:\n\n{e}")
    finally:
        # Удаление временного файла
        os.remove(constants.TEMP_AUDIO_FILE_NAME)

# Скачивание файла
def download_file(bot, file_id):
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    # Скачивание файла
    return bot.download_file(file_path)

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
