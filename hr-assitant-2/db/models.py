# layer of models representing the messages and conversations
# we will sqlalchemy as framework to create the models for messages and conversations
# Messages [id, conversation_id, role, content, created_at]
# Conversations [id, title, created_at]

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date

DB_FILE = "sqlite:///hr_assistant-2.db"

Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    tokens = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=date.today) 

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    tokens = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=date.today)

class Conversation_summary(Base):
    __tablename__ = "conversation_summaries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    summary = Column(String, nullable=False)
    last_message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    created_at = Column(DateTime, default=date.today)

def autocreate_tables():
    # create engine for sqlite database DB_FILE
    from sqlalchemy import create_engine
    engine = create_engine(DB_FILE)
    Base.metadata.create_all(engine)