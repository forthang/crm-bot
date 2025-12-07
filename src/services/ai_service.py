import speech_recognition as sr
from pydub import AudioSegment
import os

async def speech_to_text(file_path: str, language: str = "ru-RU") -> str:
    """
    Бесплатное распознавание речи через Google Speech Recognition.
    
    :param file_path: Путь к файлу .ogg (Telegram Voice)
    :param language: Код языка для Google (ru-RU, en-US, fr-FR)
    """
    recognizer = sr.Recognizer()
    
    # Telegram сохраняет в .ogg, а Google Speech хочет .wav
    wav_path = file_path.replace(".ogg", ".wav")

    try:
        # 1. Конвертация OGG -> WAV (используем pydub + ffmpeg)
        # Это обязательный шаг
        audio = AudioSegment.from_ogg(file_path)
        audio.export(wav_path, format="wav")

        # 2. Распознавание
        with sr.AudioFile(wav_path) as source:
            # Считываем аудиоданные из файла
            audio_data = recognizer.record(source)
            
            # Отправляем запрос на сервера Google
            # Это бесплатно и не требует API ключа (используется дефолтный ключ библиотеки)
            text = recognizer.recognize_google(audio_data, language=language)
            
        return text

    except sr.UnknownValueError:
        return "[Не удалось разобрать речь / Speech not recognized]"
    except sr.RequestError:
        return "[Ошибка соединения с Google / Connection error]"
    except Exception as e:
        print(f"❌ Ошибка обработки аудио: {e}")
        return "[Ошибка аудио / Audio error]"
        
    finally:
        # 3. Удаляем временный wav файл, чтобы не засорять диск
        # (.ogg файл удаляется в хендлере, а .wav мы создали тут, поэтому удаляем тут)
        if os.path.exists(wav_path):
            os.remove(wav_path)