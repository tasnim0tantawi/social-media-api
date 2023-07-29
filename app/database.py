from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .secret import db_password, db_name

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{db_password}@localhost/{db_name}"

# while True:
#     try:
#         connection = psycopg2.connect(user="postgres", host="localhost", password=db_password, database=db_name,
#                                     cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("Database connection established")
#         break

#     except Exception as error:
#         print("Error while connecting to PostgreSQL", error)
#         time.sleep(5)



engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()