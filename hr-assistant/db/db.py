
from sqlalchemy import engine, create_engine
from db.models import DB_PATH
from db.models import Conversation, ChatMessage, ConversationSummary
from sqlalchemy.orm import sessionmaker

engine = create_engine(DB_PATH)
Session = sessionmaker(bind=engine)
session = Session()

def create_conversation(title):
    conversation = Conversation(title=title)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation

def list_conversations():
    return session.query(Conversation).all()

def create_chat_message(conversation_id:str, text:str, role:str, tokens_spent:int):
    chat_message = ChatMessage(conversation_id=conversation_id, text=text, role=role, tokens_spent=tokens_spent)
    session.add(chat_message)
    session.commit()
    session.refresh(chat_message)
    return chat_message

def list_messages_in_conversation(conversation_id:str):
    mesaages = session.query(ChatMessage).\
        filter(ChatMessage.conversation_id == conversation_id).all()
    return [{"role": m.role, "content": m.text,"id": m.id} for m in mesaages]

def update_token_usage(conversation_id: str, tokens: int):
    conversation = session.query(Conversation).get(conversation_id)
    conversation.tokens_spent = (conversation.tokens_spent or 0) + tokens
    session.commit()

def update_conversation_summary(conversation_id: str, summary_text: str, last_message_id: int):
    summary = session.query(ConversationSummary).filter(ConversationSummary.conversation_id == conversation_id).first()
    if not summary:
        summary = ConversationSummary(conversation_id=conversation_id, summary_text=summary_text, last_message_id=last_message_id)
        session.add(summary)
    else:
        summary.summary_text = summary_text
        summary.last_message_id = last_message_id
    session.commit()
    return summary

def get_conversation_summary(conversation_id: str):
    return session.query(ConversationSummary).filter(ConversationSummary.conversation_id == conversation_id).first()

def read_messages_after_last_compaction(conversation_id: str):
    # read the last_message_id from the conversation summary table
    # if conversation_summary exists, get the last_message_id otherwise set it to None
    #  and read all in case last_message_id is None
    conversation_summary = get_conversation_summary(conversation_id=conversation_id)
    if conversation_summary:
        last_message_id = conversation_summary.last_message_id
    else:
        last_message_id = None

    if last_message_id is None:
        messages = session.query(ChatMessage).filter(ChatMessage.conversation_id == conversation_id).all()
    else:
        messages = session.query(ChatMessage).filter(ChatMessage.conversation_id == conversation_id, ChatMessage.id > last_message_id).all()
    return [{"role": m.role, "content": m.text,"id": m.id} for m in messages]
