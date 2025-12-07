from openai import AsyncOpenAI
import os
import httpx

from src.config import config

# Define the proxy
proxy_url = "socks5://82.152.233.24:50101:malexoff:DsNfV67K9J"

# Create an httpx client with the proxy
http_client = httpx.AsyncClient(proxies=proxy_url)

# Initialize the OpenAI client with the httpx client
client = AsyncOpenAI(
    api_key=config.OPENAI_API_KEY.get_secret_value(),
    http_client=http_client
)

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