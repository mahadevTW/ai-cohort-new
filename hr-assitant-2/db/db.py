#  all functions interacting to db table are part of this file
# all db tables are represented from file models.py
# insert_message, and list messages 

from sqlalchemy import create_engine
from db.models import DB_FILE, Message, Conversation
engine = create_engine(DB_FILE)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

def insert_message(role: str, content: str):
    message = Message(role=role, content=content)
    session.add(message)
    session.commit()
    session.close()
    return message

def list_messages():
    messages = session.query(Message).all()
    session.close()
    return messages

def create_conversation(title: str):
    conversation = Conversation(title=title)
    session.add(conversation)
    session.commit()
    session.close()
    return conversation