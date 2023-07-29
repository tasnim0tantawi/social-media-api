from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from typing import List
from .. import oauth2


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

    posts = db.query(models.Post).filter(models.Post.visibility == "public").all()
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found.")
    
    return posts

@router.get("/my_posts", response_model=List[schemas.PostResponse])
def get_my_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found.")
    
    return posts    

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts  WHERE id = %s", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post.visibility == "private" and post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view this post.")

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return post
    

@router.post("/", status_code=status.HTTP_201_CREATED,  response_model=schemas.PostResponse)
def create_post(post: schemas.Post, db: Session = Depends(get_db),
            current_user:schemas.UserResponse = Depends(oauth2.get_current_user)):
    post = models.Post(title=post.title, content=post.content, visibility= post.visibility, user_id=current_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return  post

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db), current_user:schemas.UserResponse = Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published=%s WHERE id = %s RETURNING *", (post.title, post.content,post.published, str(id)))
    # updated_post = cursor.fetchone()
    # connection.commit()

    query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    
    if updated_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this post.")
    
    query.update(post.dict())
    db.commit()
    db.refresh(updated_post)
    updated_post = query.first()
    
    return updated_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                 user_id:int = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s", (str(id),))
    # connection.commit()
    # deleted_post = cursor.fetchone()
    query = db.query(models.Post).filter(models.Post.id == id)
    
    if query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    
    if query.first().user_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this post.")
    
    query.delete(synchronize_session=False)
    db.commit()
