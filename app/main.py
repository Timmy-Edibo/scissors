from fastapi import FastAPI
from app.models import models
from app.database.db import engine

from app.routers import users
from app.routers import shorten_url

app = FastAPI(title="Scissors App",
              description="A multi-functional platform where authors and readers  \
              can create and have access to their own content.",
              version="1.0.0")


from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"],
)


@app.get('/root')
def main():
    return "Hello, world"


app.include_router(users.user_router)
app.include_router(shorten_url.shorten_url_router)


