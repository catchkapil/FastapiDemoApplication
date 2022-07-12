from email.policy import HTTP
from os import stat
from typing import List, Optional
from .. import schemas
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from .. import models
from ..database import get_db
from .. import oauth2
from sqlalchemy import func

router = APIRouter(prefix='/posts', tags=['Users Post'])


@router.get("/", response_model=List[schemas.PostResponse])
# Query params based API Call
# ---------------------------> Limit , Optional and Search are query  params
def get_posts(db: Session = Depends(get_db), limit: Optional[int] = 10, skip: Optional[int] = 0, search: Optional[str] = ""):
    # all_posts = db.query(models.Post).limit(limit).skip(
    #     skip).filter(models.title.contains(search)).all()
    all_posts = db.query(models.Post).all()

    # Default SQLAlchemy Join is Left inner join
    # --------------------> ORM to get all the votes for specific post
    all_posts_new = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

    print(all_posts_new)

    return all_posts


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute(
    #     """SELECT * FROM posts where id = %s""", str(id))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"post with id : {id} not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    # print("User Email : ", current_user.email)

    # new_post = models.Post(title=post.title, content=post.content,
    #                        published=post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    return new_post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))

    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"post with id : {id} not found")
    if(post_query.first().owner_id != current_user.id):
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            f"Not authorized to perform requested action.")

    post_query.delete(synchronize_session=False)
    db.commit()
    return None


@router.put('/{id}')
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s,content = %s,published=%s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()

    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"post with id : {id} not found")
    if(post_query.first().owner_id != current_user.id):
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            f"Not authorized to perform requested action.")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {"response": f"post with id : {id} updated successfully ...."}
