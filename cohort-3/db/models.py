# SQL definition of the message table
# using sqlAlchemy framework

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role= Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    token_usage = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

# at start if this table does not exist, create it
engine = create_engine("sqlite:///messages.db")
Base.metadata.create_all(engine)
print("Database tables are created")