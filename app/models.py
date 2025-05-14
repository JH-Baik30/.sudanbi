# app/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    english = Column(String)
    pronunciation = Column(String)
    part_of_speech = Column(String)
    meaning = Column(String)
    example_sentence = Column(String)
    example_translation = Column(String)
