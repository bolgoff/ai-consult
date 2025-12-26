import os
import aiofiles
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, Header, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from app.config import settings
from app.db_connect import connection, Base, get_db
from app.db_postgres import DialogLog
from app.services.ai_logic import generate_response, clear_history
from app.services.whisperer import transcribe_audio

@asynccontextmanager
<<<<<<< HEAD
async def lifespan(app: FastAPI):
=======
async def lifespan():
>>>>>>> 93a86bcb04ca010b2ae1e08f121dda4fc06575ca
    async with connection.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

async def verify_key(x_api_key=Header()):
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Неверный ключ API")

async def log_interaction(db, user_id, req_type, query, response):
    log = DialogLog(user_id=user_id, request_type=req_type, user_query=query, ai_response=response)
    db.add(log)
    await db.commit()

@app.post("/api/v1/chat/text", dependencies=[Depends(verify_key)])
async def chat_text(
<<<<<<< HEAD
    background_tasks: BackgroundTasks,
    user_id: str = Form(...),
    text: str = Form(None),
    image: UploadFile = File(None),
    db: AsyncSession = Depends(get_db)
=======
    background_tasks,
    user_id=Form(...),
    text=Form(None),
    image=File(None),
    db=Depends(get_db)
>>>>>>> 93a86bcb04ca010b2ae1e08f121dda4fc06575ca
):
    if not text and not image:
        raise HTTPException(status_code=400, detail="Нужен текст и/или картинка")
    
    image_bytes = None
    if image:
        image_bytes = await image.read()
        if not text: 
            text = "Что изображено на картинке в контексте документа?"

    response_text = await generate_response(user_id, text, image_bytes)

    async def save_log():
        async with AsyncSession(connection) as session:
             await log_interaction(session, user_id, "text/image", text, response_text)
    
    background_tasks.add_task(save_log)

    return {"response": response_text}

# Эндпойнт с аудио и картинкой
@app.post("/api/v1/chat/audio", dependencies=[Depends(verify_key)])
async def chat_audio(
<<<<<<< HEAD
    background_tasks: BackgroundTasks,
    user_id: str = Form(...),
    audio=File(...),
    image: UploadFile = File(None),
    db: AsyncSession = Depends(get_db)
=======
    background_tasks,
    user_id=Form(...),
    audio=File(...),
    image=File(None),
    db=Depends(get_db)
>>>>>>> 93a86bcb04ca010b2ae1e08f121dda4fc06575ca
):
    temp_filename = f"temp_{user_id}_{audio.filename}"
    async with aiofiles.open(temp_filename, 'wb') as out_file:
        content = await audio.read()
        await out_file.write(content)

    try:
        transcribed_text = await transcribe_audio(temp_filename)
    finally:
        os.remove(temp_filename)

    image_bytes = None
    if image:
        image_bytes = await image.read()

    response_text = await generate_response(user_id, transcribed_text, image_bytes)

    async def save_log():
        async with AsyncSession(connection) as session:
             await log_interaction(session, user_id, "audio", transcribed_text, response_text)
    
    background_tasks.add_task(save_log)

    return {"transcription": transcribed_text, "response": response_text}

@app.delete("/api/v1/history/{user_id}", dependencies=[Depends(verify_key)])
async def delete_history(user_id: str):
    success = clear_history(user_id)
<<<<<<< HEAD
    return {"status": "cleared" if success else "user not found"}
=======
    return {"status": "cleared" if success else "user not found"}
>>>>>>> 93a86bcb04ca010b2ae1e08f121dda4fc06575ca
