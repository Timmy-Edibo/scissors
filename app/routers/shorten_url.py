from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.shorten_url import ShortenUrl, UpdateShortenUrl
from fastapi.responses import JSONResponse


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
    
    check_custom_url = db.query(models.ShortenUrl).filter(
        models.ShortenUrl.custom_url == request.custom_url).first()
    
    if check_query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Long URL has already been mapped")
        
    if check_custom_url:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Custom domain already exists")

    short_url = generate_short_url()
    
    query = models.ShortenUrl(
        long_url=request.long_url,
        custom_url=request.custom_url,
        user=current_user.email,
        short_url=short_url
    )
    
    db.add(query)
    db.commit()
    db.refresh(query)
    return  query


@shorten_url_router.get("/list-all")
def list_shorten_url(db:Session=  Depends(get_db), 
                    current_user:Session=Depends(get_current_user)):
    
    query = db.query(models.ShortenUrl).all()
    return query if len(query) > 0 else []



@shorten_url_router.get("/search/{short_url}")
def search_shorten_url(short_url: str, custom_url:str, db:Session=  Depends(get_db), 
                    current_user:Session=Depends(get_current_user)):
    
    check_query = db.query(models.ShortenUrl).filter(
        models.ShortenUrl.short_url == short_url).first()
    
    if not check_query.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="URL does not exist")
    
    return check_query.first()




@shorten_url_router.patch("/update-custom-domain/{short_url}")
def search_shorten_url(short_url: str, custom_url:str, db:Session=  Depends(get_db), 
                    current_user:Session=Depends(get_current_user)):
    
    check_query = db.query(models.ShortenUrl).filter(
        models.ShortenUrl.short_url == short_url)
    
    check_custom_url = db.query(models.ShortenUrl).filter(
        models.ShortenUrl.custom_url == custom_url).first()
    
    if not check_query.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="URL does not exist")
    
    if current_user.email != check_query.first().user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                    detail="Unauthorized to perform this operation")
        
    if check_custom_url:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Custom domain already exists")
        
    check_query.update({'custom_url': custom_url})
    db.commit()

    return check_query.first()


@shorten_url_router.put("/update/{short_url}")
def update_shorten_url(short_url: str, request: UpdateShortenUrl, db:Session=  Depends(get_db), 
            current_user:Session=Depends(get_current_user)):
    
    check_query = db.query(models.ShortenUrl).filter(
        models.ShortenUrl.short_url == short_url)
    
    if not check_query.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="URL does not exist")
    
    if current_user.email != check_query.first().user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Unauthorized to perform this operation")
        
    check_query.update(request.dict())
    db.commit()

    return check_query.first()


@shorten_url_router.delete("/delete/{short_url}")
def delete_content(url:str, db:Session=  Depends(get_db), 
                current_user:Session=Depends(get_current_user)):
    
    
    check_query = db.query(models.ShortenUrl).filter(
        models.ShortenUrl.short_url == url).first()
    
    if not check_query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="URL does not exist")
        
    if current_user.email != check_query.user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Unauthorized to perform this operation")
        
    db.delete(check_query)
    db.commit()
    
    return  JSONResponse(status_code=204, content="No content")
