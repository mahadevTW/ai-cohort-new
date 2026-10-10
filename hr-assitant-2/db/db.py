#  all functions interacting to db table are part of this file
# all db tables are represented from file models.py
# insert_message, and list messages 

from sqlalchemy import create_engine
from db.models import DB_FILE, Message, Conversation
engine = create_engine(DB_FILE)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

def insert_message(role: str, content: str, conversation_id: int, tokens: int = None):
    message = Message(role=role, content=content, conversation_id=conversation_id, tokens=tokens)
    session.add(message)
    session.commit()
    session.close()
    return message

def list_messages(conversation_id:int):
    # select * from messages where conversation_id={}
    messages = session.query(Message).filter(Message.conversation_id == conversation_id).all()
    session.close()
    return messages

def list_messages_after_summary(conversation_id:int, last_message_id:int):
    # select * from messages where conversation_id={} && id > last_message_id
    messages = session.query(Message).filter(Message.conversation_id == conversation_id, Message.id > last_message_id).all()
    session.close()
    return messages


def create_conversation(title: str):
    conversation = Conversation(title=title)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    c =  {"id": conversation.id, "title": conversation.title}
    session.close()
    return c

def increment_conversation_tokens(conversation_id: int, tokens: int):
    conversation = session.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation:
        if conversation.tokens is None:
            conversation.tokens = 0
        conversation.tokens = conversation.tokens + tokens
        session.commit()
        session.refresh(conversation)
        session.close()
    session.close()

# upsert the conversation summary
def insert_or_update_conversation_summary(conversation_id: int, summary: str, last_message_id: int):
    # check if for given conversation_id a summary already exists, if yes update it otherwise insert a new one
    from db.models import Conversation_summary
    conversation_summary = session.query(Conversation_summary).filter(Conversation_summary.conversation_id == conversation_id).first()
    if conversation_summary:
        conversation_summary.summary = summary
        conversation_summary.last_message_id = last_message_id
    else:
        conversation_summary = Conversation_summary(conversation_id=conversation_id, summary=summary, last_message_id=last_message_id)
        session.add(conversation_summary)
    session.commit()
    session.refresh(conversation_summary)
    session.close()
    return conversation_summary

def get_summary(conversation_id: int):
    from db.models import Conversation_summary
    summary = session.query(Conversation_summary).filter(Conversation_summary.conversation_id == conversation_id).first()
    session.close()
    return summary