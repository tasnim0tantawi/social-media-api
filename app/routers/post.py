from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from typing import List


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    responses={404: {"description": "Not found"}},
)
app = FastAPI()

# Getting all posts, a best practice is to name the route /posts with an s at the end.
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts
    

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts  WHERE id = %s", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return post
    

@router.post("/", status_code=status.HTTP_201_CREATED,  response_model=schemas.PostResponse)
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return  post

@router.put("/{id}", response_model=schemas.PostResponse)
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("DELETE FROM posts WHERE id = %s", (str(id),))
    # connection.commit()
    # deleted_post = cursor.fetchone()
    query = db.query(models.Post).filter(models.Post.id == id)
    
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    query.delete(synchronize_session=False)
    db.commit()
