from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import contextlib

#database 
DATABASE_LOCATION = 'sqlite:///./shop.db'

#creating sqlalchemy engine

engine = create_engine(DATABASE_LOCATION, echo=False)


#creating session class
Local_session = sessionmaker(bind=engine)


def create_tables():
    """creates all tables if they haven't been created yet"""
    print("creating tables...")
    Base.metadata.create_all(engine)
    print("Tables are created or they already exist")

@contextlib.contextmanager
def get_db():
    """generator to receive and close db"""

    db = Local_session()
    try:
        yield db #returns session
    finally:
        db.close