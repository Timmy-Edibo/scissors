from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.shorten_url import ShortenUrl

from app.database.db import get_db
from sqlalchemy.orm import Session
from app.middleware import get_current_user

from app.models import models
from .url_generator import generate_short_url

shorten_url_router = APIRouter(prefix="/api/v1/url", tags=['url'])

@shorten_url_router.post("/shorten")
def shorten_shorten_url(request:ShortenUrl, db:Session=  Depends(get_db), 
                        current_user:Session=Depends(get_current_user)):
    
    check_query = db.query(models.ShortenUrl).filter(
        models.ShortenUrl.long_url == request.long_url).first()
    
    if check_query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Long URL has already been mapped")

    domain = "bluecounts.com"
    short_url = generate_short_url(domain)
    
    query = models.ShortenUrl(
        long_url=request.long_url,
        custom_url=request.custom_url,
        user=current_user.email,
        short_url=short_url
    )
    # query = models.ShortenUrl(**request.dict())
    
    db.add(query)
    db.commit()
    db.refresh(query)
    return  query

from fastapi.responses import RedirectResponse

@shorten_url_router.get("/{short_url}")
def redirect_url(short_url: str, db:Session=  Depends(get_db), 
                current_user:Session=Depends(get_current_user)):
    
    check_query = db.query(models.ShortenUrl).filter(
        models.ShortenUrl.short_url == short_url).first()
    
    if not check_query:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return check_query



@shorten_url_router.get("/get")
def get_shorten_url():
    return  "Endpoint for fetching a single shorten_url"

@shorten_url_router.get("/list-all")
def list_shorten_url():
    return  "Endpoint for fetching all shorten_url"



@shorten_url_router.get("/search")
def search_shorten_url():
    return  "Endpoint for searching for a particular shorten_url"



@shorten_url_router.put("/update")
def update_shorten_url():
    return  "Endpoint for updating a shorten_url"


@shorten_url_router.delete("/delete")
def delete_content():
    return  "Endpoint for deleting a  content"
