from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from pydantic.types import Optional
from app.dummy import all_posts, search_post, search_post_index


posts = all_posts

app = FastAPI()

# Creating a schema (base model) for posts using pydantic
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Hi Tasnim!"}

@app.get("/posts")
def get_posts():
    return {
        "data": posts
    }

@app.post("/posts/")
def create_post():
    pass


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int):
    pass


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id):
    pass


