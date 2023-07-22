from fastapi import FastAPI, status, HTTPException
from typing import Optional, List
from app.for_reference.dummy import all_posts, search_post, search_post_index
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . secret import db_password, db_name
from . import models, schemas
from . database import engine, get_db
from sqlalchemy.orm import Session
# import Depends
from fastapi import Depends
import utils



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


# Getting all posts, a best practice is to name the route /posts with an s at the end.
@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts
    

@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts  WHERE id = %s", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return post
    

@app.post("/posts", status_code=status.HTTP_201_CREATED,  response_model=schemas.PostResponse)
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return  post

@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):
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
    
    return updated_post


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


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user( user:schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash_password(user.password)
    user = models.User(username=user.username, password=hashed_password, email=user.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

