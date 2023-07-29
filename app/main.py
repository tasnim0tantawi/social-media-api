from fastapi import FastAPI
from app.for_reference.dummy import all_posts, search_post, search_post_index
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . secret import db_password, db_name
from . import models, schemas
from . database import engine, get_db
from . routers import post, user, authentication



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# The function root gets called when the user visits the root of the API.
@app.get("/")
def root():
    return {"message": "Hi Tasnim!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)



