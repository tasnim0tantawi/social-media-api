from fastapi import FastAPI
from app.for_reference.dummy import all_posts, search_post, search_post_index
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . secret import db_password, db_name
from . import models, schemas
from . database import engine, get_db
from . routers import post, user



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        connection = psycopg2.connect(user="postgres", host="localhost", password=db_password, database=db_name,
                                    cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database connection established")
        break

    except Exception as error:
        print("Error while connecting to PostgreSQL", error)
        time.sleep(5)



# The function root gets called when the user visits the root of the API.
@app.get("/")
def root():
    return {"message": "Hi Tasnim!"}

app.include_router(post.router)
app.include_router(user.router)



