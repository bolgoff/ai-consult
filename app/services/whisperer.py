<<<<<<< HEAD
import os
from groq import AsyncGroq
from app.config import settings

async def transcribe_audio(file_path: str) -> str:
    client = AsyncGroq(api_key=settings.GROQ_API_KEY)
    with open(file_path, "rb") as audio_file:
        audio_result = await client.audio.transcriptions.create(
	file=(os.path.basename(file_path), file.read()),
	model="whisper-1",
	response_format="json",
	language='ru',
	temperature=0.0 
        )
    return audio_result.text
=======
import openai
from app.config import settings

async def transcribe_audio(file_path: str) -> str:
    client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    with open(file_path, "rb") as audio_file:
        audio_result = await client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    return audio_result.text
>>>>>>> 93a86bcb04ca010b2ae1e08f121dda4fc06575ca
