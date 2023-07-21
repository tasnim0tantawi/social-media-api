from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.for_reference.dummy import all_posts, search_post, search_post_index
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . secret import db_password, db_name
from . import models
from . database import engine, get_db
from sqlalchemy.orm import Session
# import Depends
from fastapi import Depends




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



# Creating a schema (base model) for posts using pydantic
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# The function root gets called when the user visits the root of the API.
@app.get("/")
def root():
    return {"message": "Hi Tasnim!"}


# Getting all posts, a best practice is to name the route /posts with an s at the end.
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {
        "data": posts
    }

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts  WHERE id = %s", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return {
        "data": post
    }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return {
        "message": "Post created successfully.",
        "data": post
    }

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published=%s WHERE id = %s RETURNING *", (post.title, post.content,post.published, str(id)))
    # updated_post = cursor.fetchone()
    # connection.commit()

    query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    query.update(post.dict())
    db.commit()
    db.refresh(updated_post)
    updated_post = query.first()
    
    return {
        "message": "Post updated successfully.",
        "data": updated_post
    }



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("DELETE FROM posts WHERE id = %s", (str(id),))
    # connection.commit()
    # deleted_post = cursor.fetchone()
    query = db.query(models.Post).filter(models.Post.id == id)
    
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    query.delete(synchronize_session=False)
    db.commit()




