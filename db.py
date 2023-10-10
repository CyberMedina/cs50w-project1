import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, text
from dotenv import load_dotenv
load_dotenv()



# Set up database
engine= create_engine(os.getenv("DATABASE_URL"), pool_pre_ping=True,
        connect_args={
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        }
)
db = scoped_session(sessionmaker(bind=engine))
