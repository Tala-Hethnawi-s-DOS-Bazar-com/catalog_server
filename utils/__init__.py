from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///./db.sqlite3', echo=False, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()
