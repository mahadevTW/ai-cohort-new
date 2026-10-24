# all utility functions related to database operations can be added here
from sqlalchemy.orm import sessionmaker
from db.models import Message, engine
from datetime import datetime

Session = sessionmaker(bind=engine)

def insert_message(role, content):
    session = Session()
    message = Message(role=role, content=content, timestamp=datetime.now())
    session.add(message)
    session.commit()
    session.close()
    return message

def get_all_messages():
    session = Session()
    messages = session.query(Message).all()
    session.close()
    return messages