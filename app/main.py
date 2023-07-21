from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.dummy import all_posts, search_post, search_post_index
import psycopg2
from psycopg2.extras import RealDictCursor
import time



app = FastAPI()

while True:
    try:
        connection = psycopg2.connect(user="postgres", host="localhost", password="Featherine123", database="fastapi",
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
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return {
        "data": post
    }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)", (post.title, post.content, post.published, post.rating))
    return {
        "message": "Post created successfully.",
        "data": post
    }

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_index = search_post_index(id)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_index = search_post_index(id)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")



