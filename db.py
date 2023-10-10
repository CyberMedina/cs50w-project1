import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, text
from dotenv import load_dotenv
load_dotenv()



# Set up database
engine= create_engine(os.getenv("DATABASE_URL"), pool_size=20, max_overflow=30)
db = scoped_session(sessionmaker(bind=engine))
