from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.for_reference.dummy import all_posts, search_post, search_post_index
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . secret import db_password, db_name



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
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {
        "data": posts
    }

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts  WHERE id = %s", (str(id),))
    post = cursor.fetchone()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return {
        "data": post
    }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *", (post.title, post.content))
    post = cursor.fetchone()
    connection.commit()

    return {
        "message": "Post created successfully.",
        "data": post
    }

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published=%s WHERE id = %s RETURNING *", (post.title, post.content,post.published, str(id)))
    updated_post = cursor.fetchone()
    connection.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    
    return {
        "message": "Post updated successfully.",
        "data": updated_post
    }




@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s", (str(id),))
    connection.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")



