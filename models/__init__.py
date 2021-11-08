from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from utils import engine

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    price = Column(Float, default=0.0, nullable=False)
    topic_id = Column(Integer, ForeignKey('topic.id'))
    topic = relationship('Topic', backref='books')


class Topic(Base):
    __tablename__ = 'topic'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


Base.metadata.create_all(engine)
