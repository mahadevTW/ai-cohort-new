# all utility functions related to database operations can be added here
from sqlalchemy.orm import sessionmaker
from db.models import Message, engine
from datetime import datetime

Session = sessionmaker(bind=engine, expire_on_commit=False)

def insert_message(role, content, token_usage, conversation_id=None):
    session = Session()
    message = Message(role=role, content=content, token_usage=token_usage, conversation_id=conversation_id, timestamp=datetime.now())
    session.add(message)
    session.commit()
    session.close()
    return message

def get_all_messages(conversation_id):
    session = Session()
    messages = session.query(Message).filter_by(conversation_id=conversation_id).all()
    session.close()
    return messages

def create_conversation(title):
    session = Session()
    from db.models import Conversation
    conversation = Conversation(title=title, token_usage=0, timestamp=datetime.now())
    session.add(conversation)
    session.commit()
    session.close()
    return conversation

def list_conversations():
    session = Session()
    from db.models import Conversation
    conversations = session.query(Conversation).all()
    session.close()
    return conversations