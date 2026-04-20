from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    survey_name = Column(String(255), nullable=False)
    page_name = Column(String(255), nullable=False)
    survey_monkey_id = Column(String(100))
    survey_link = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("Question", back_populates="survey", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.id", ondelete="CASCADE"), nullable=False)
    question_title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    survey = relationship("Survey", back_populates="questions")
    choices = relationship("Choice", back_populates="question", cascade="all, delete-orphan")


class Choice(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    choice_text = Column(String(255), nullable=False)

    question = relationship("Question", back_populates="choices")