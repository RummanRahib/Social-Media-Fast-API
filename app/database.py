from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# structure --> 'postgresql://<username>:<password>@<ip_address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# to run raw sql directly using postgres libray instead of Sqlalchemy

# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'Social Media Fast API', user = 'postgres', password = 'postgresql', cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful.')
#         break
#     except Exception as error:
#         print('Connecting to DB failed')
#         print('Error: ', error)
#         sleep(2)
