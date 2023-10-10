import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, text
from dotenv import load_dotenv
load_dotenv()



# Set up database
engine= create_engine(os.getenv("DATABASE_URL"),  pool_size=10,
                                      max_overflow=2,
                                      pool_recycle=300,
                                      pool_pre_ping=True,
                                      pool_use_lifo=True)
db = scoped_session(sessionmaker(bind=engine))
