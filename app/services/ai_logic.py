import base64
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from app.services.qdrant_db import get_vectors
from app.config import settings

store = {}

def get_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    
    if len(store[session_id].messages) > 10:
        store[session_id].messages = store[session_id].messages[-10:]
        
    return store[session_id]

def clear_history(session_id):
    if session_id in store:
        store[session_id].clear()
        return True
    return False

async def generate_response(user_id, text, image_bytes=None):
    vector_store = get_vectors()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    docs = await retriever.ainvoke(text)
    context_text = "\n\n".join([d.page_content for d in docs])

    llm = ChatOpenAI(
	model="gpt-4o-mini", 
	temperature=0.3,
	api_key=settings.OPENAI_API_KEY
)

    promptik = (
        "Ты умный консультант. Отвечай на вопросы пользователя, используя \
        только предоставленный контекст. Если контекст не предоставлен - ответь, что не знаешь, не придумывай ответ."
        f"\n\nКонтекст:\n{context_text}"
    )

    history = get_history(user_id)
    messages = [SystemMessage(content=promptik)] + history.messages

    user_content = [{"type": "text", "text": text}]
    
    if image_bytes:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        user_content.append({
            "type": "image_url",
            "image_url": f"data:image/jpeg;base64,{base64_image}"
        })

    messages.append(HumanMessage(content=user_content))

    response = await llm.ainvoke(messages)
    
    history.add_user_message(text + " [Image Uploaded]" if image_bytes else text)
    history.add_ai_message(response.content)

    return response.content
