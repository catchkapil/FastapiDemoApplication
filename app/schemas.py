from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:  # Convert Pydantic Data Structure to Dictionary
        orm_mode = True


class UserCreatedResponse(BaseModel):
    email: EmailStr
    created_at: datetime
    id: int

    class Config:  # Convert Pydantic Data Structure to Dictionary for response Model
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:  # Convert Pydantic Data Structure to Dictionary
        orm_mode = True


class UserToken(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class PostBase(BaseModel):  # Pydantic Model
    title: str
    content: str
    published: bool = True  # Field with default value

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    created_at: datetime
    owner_id: int
    owner: UserCreatedResponse


class PostWithVoteResponse(PostResponse):
    post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id: int
    vote_dir: conint(le=1)
