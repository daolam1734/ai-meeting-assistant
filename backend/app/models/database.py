from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, create_base
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    transcript = Column(Text)
    summary = Column(Text)
    
    tasks = relationship("Task", back_populates="meeting")
    decisions = relationship("Decision", back_populates="meeting")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    assignee = Column(String, nullable=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    
    meeting = relationship("Meeting", back_populates="tasks")

class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    
    meeting = relationship("Meeting", back_populates="decisions")
