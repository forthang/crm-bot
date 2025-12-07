from openai import AsyncOpenAI
import os

from src.config import config

client = AsyncOpenAI(api_key=config.OPENAI_API_KEY.get_secret_value())

async def speech_to_text(file_path: str, language: str = "en") -> str:
    """
    Speech recognition using OpenAI Whisper API.
    
    :param file_path: Path to the .ogg file (Telegram Voice)
    :param language: Language code for Whisper (e.g., en, fr)
    """
    try:
        with open(file_path, "rb") as audio_file:
            transcript = await client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                language=language
            )
        return transcript.text
    except Exception as e:
        print(f"❌ Error processing audio with OpenAI: {e}")
        return "[Audio processing error]"
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)