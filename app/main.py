
# import psycopg2
# from psycopg2.extras import RealDictCursor

from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# Currently commented because we are creating table using alembic autogenerate
# models.Base.metadata.create_all(bind=engine)  # Create All DB Models

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():

    return {"message": "Hello World"}

# Getting Connection object to database using psycopg2 Database driver for postgres
# while True:

#     try:
#         # Setting up connection to database
#         conn = psycopg2.connect(host='localhost', database='FastApiDatabase',
#                                 user='postgres', password='************', cursor_factory=RealDictCursor)  # Cursor Factory to get column name
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break

#     except Exception as error:
#         print("Connection to database failed ....")
#         print("Error : ", error)
#         time.sleep(2)
