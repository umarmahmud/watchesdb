import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

user = os.getenv("USER")
server = os.getenv("SERVER")
host = os.getenv("HOST")
database = os.getenv("DATABASE")


db_url = f'postgresql+psycopg2://{user}:{server}@{host}/{database}'
engine = create_engine(db_url, echo=True)
Session = sessionmaker(bind=engine)


def get_db():
    with Session() as session:
        yield session