from typing import List, Optional
from .. import schemas
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from .. import models
from .. import utils
from ..database import get_db
from .. import oauth2

router = APIRouter(prefix='/vote', tags=['Votes on Post'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def user_post_vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    post = db.query(models.Post.id).filter(
        models.Post.id == vote.post_id).all()

    if post:

        vote_query = db.query(models.Vote).filter(
            models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
        found_vote = vote_query.first()
        if(vote.vote_dir == 1):
            if found_vote:
                raise HTTPException(status.HTTP_409_CONFLICT,
                                    f"You have already voted on post with vote id : {vote.post_id}")
            else:
                new_vote = models.Vote(post_id=vote.post_id,
                                       user_id=current_user.id)
                db.add(new_vote)
                db.commit()
                return{"message": "successfully added the vote"}
        else:
            if found_vote:
                vote_query.delete(synchronize_session=False)
                db.commit()
                return {"message": "successfully deleted the vote ...."}

            else:
                raise HTTPException(status.HTTP_404_NOT_FOUND,
                                    f"Vote doesnot exist... ")

    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"No post with id : {vote.id} doesn't exists ... ")
