# use sqlalchemy to create 2 tables, ChatMessage other is Conversation
from datetime import date

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
#  sqlite file path
DB_PATH = "sqlite:///hr_assistant.db"

Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    created_at = Column(String, default=date.today)
    tokens_spent = Column(Integer)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String)
    text = Column(String)
    created_at = Column(String, default=date.today)
    tokens_spent = Column(Integer)

class ConversationSummary(Base):
    __tablename__ = "conversation_summaries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    summary_text = Column(String)
    last_message_id = Column(Integer, ForeignKey("chat_messages.id"))
    created_at = Column(String, default=date.today)

# on start, create the database tables
from sqlalchemy import create_engine
engine = create_engine(DB_PATH)
Base.metadata.create_all(engine)