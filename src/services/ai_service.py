from openai import AsyncOpenAI
import os
import httpx
import json
from datetime import datetime
import pytz

from src.config import config

# Define the proxy
proxy_url = "socks5://malexoff:DsNfV67K9J@82.152.233.24:50101"
print(f"Using proxy: {proxy_url}")

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

async def get_intent_and_entities(text: str, user_timezone: str) -> dict:
    """
    Uses OpenAI to extract intent and entities from a user's command.
    """
    # Fallback to a default timezone if the provided one is invalid
    try:
        local_tz = pytz.timezone(user_timezone)
    except pytz.UnknownTimeZoneError:
        local_tz = pytz.timezone("UTC")

    now = datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")

    # The system prompt that instructs the model
    system_prompt = f"""
You are an intelligent assistant for a CRM Telegram bot. Your task is to analyze the user's voice commands and extract the intent and relevant entities.

The user's timezone is {user_timezone}.
The current date and time is {now}.

Supported intents:
- "create_client_and_schedule_call": When the user wants to create a new client and schedule a call for them.
- "schedule_call": When the user wants to schedule a call for an *existing* client.
- "create_client": When the user only wants to create a new client.
- "simple_command": For simple keyword-based commands like "show clients", "show schedule", "add client".
- "other": For any other request that doesn't fit the above.

Entities to extract:
- "client_name": The name of the client.
- "call_datetime": The date and time for the call.
- "call_topic": The topic of the call.
- "command": The simple command keyword (e.g., "clients", "schedule", "add").

Analyze the user's request and respond ONLY with a JSON object in the specified structure. Do not add any text before or after the JSON.

JSON Structure:
{{
  "intent": "...",
  "entities": {{
    "client_name": "...",
    "call_datetime": "YYYY-MM-DD HH:MM", // Convert relative time (like "tomorrow at 7pm") to an absolute time in the user's timezone.
    "call_topic": "...",
    "command": "..."
  }}
}}

If an entity is not present in the text, its value in the JSON should be null.
If the intent is not clear, return "intent": "other".
"""
    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ]
        )
        result_json = response.choices[0].message.content
        return json.loads(result_json)
    except Exception as e:
        print(f"❌ Error getting intent from OpenAI: {e}")
        return {"intent": "other", "entities": {{}}}