from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.db_connect import Base

class DialogLog(Base):
    __tablename__ = "d_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    request_type = Column(String)
    user_query = Column(Text)
    ai_response = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())