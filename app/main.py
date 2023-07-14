from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.dummy import all_posts, search_post, search_post_index


posts = all_posts

app = FastAPI()

# Creating a schema (base model) for posts using pydantic
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# The function root gets called when the user visits the root of the API.
@app.get("/")
def root():
    return {"message": "Hi Tasnim!"}


# Getting all posts, a best practice is to name the route /posts with an s at the end.
@app.get("/posts")
def get_posts():
    return {
        "data": posts
    }

@app.get("/posts/{id}")
def get_post(id: int):
    post = search_post(id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return {
        "data": post
    }

@app.post("/posts")
def create_post(post: Post):
    posts.append(post.model_dump())
    return {
        "message": "Post created successfully.",
        "data": posts
    }

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_index = search_post_index(id)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    posts[post_index] = post
    return {
        "message": "Post updated successfully.",
        "data": posts
    }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_index = search_post_index(id)
    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    posts.pop(post_index)



