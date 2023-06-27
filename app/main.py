from fastapi import FastAPI
from app.models import models
from app.database.db import engine

from app.routers import users
from app.routers import shorten_url
from fastapi.responses import RedirectResponse
from sqlalchemy import or_


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

from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.shorten_url import ShortenUrl

from app.database.db import get_db
from sqlalchemy.orm import Session
from app.middleware import get_current_user

from app.models import models
from .routers.url_generator import generate_short_url

@app.get('/root')
def main():
    return "Hello, world"

@app.get("/{short_url}")
def redirect_url(short_url: str, db:Session=  Depends(get_db)):
    
    check_query = db.query(models.ShortenUrl).filter(
        or_(models.ShortenUrl.short_url == short_url, models.ShortenUrl.custom_url == short_url)
        ).first()
    
    if not check_query:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # return check_query
    return RedirectResponse(url=check_query.long_url)


app.include_router(users.user_router)
app.include_router(shorten_url.shorten_url_router)


