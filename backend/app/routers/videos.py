"""
Video router for API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.utils.database import get_db
from app.models.video import Video
from app.schemas.video import VideoCreate, VideoUpdate, Video as VideoSchema, VideoList
from app.services.instagram_scraper import InstagramScraper

router = APIRouter()

@router.get("/", response_model=VideoList)
async def get_videos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all videos with pagination"""
    videos = db.query(Video).offset(skip).limit(limit).all()
    total = db.query(Video).count()
    
    return VideoList(
        videos=videos,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.get("/{video_id}", response_model=VideoSchema)
async def get_video(video_id: int, db: Session = Depends(get_db)):
    """Get video by ID"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@router.post("/scrape", response_model=VideoSchema)
async def scrape_video(
    url: str,
    db: Session = Depends(get_db)
):
    """Scrape data from Instagram video URL"""
    scraper = InstagramScraper()
    data = scraper.scrape_video_data(url)
    
    if not data:
        raise HTTPException(status_code=400, detail="Failed to scrape video data")
    
    # Check if video already exists
    existing_video = db.query(Video).filter(Video.url == url).first()
    if existing_video:
        # Update existing video
        for key, value in data.items():
            if hasattr(existing_video, key):
                setattr(existing_video, key, value)
        db.commit()
        db.refresh(existing_video)
        return existing_video
    
    # Create new video
    video_data = VideoCreate(**data)
    db_video = Video(**video_data.dict())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    
    return db_video

@router.put("/{video_id}", response_model=VideoSchema)
async def update_video(
    video_id: int,
    video_update: VideoUpdate,
    db: Session = Depends(get_db)
):
    """Update video data"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    update_data = video_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(video, key, value)
    
    db.commit()
    db.refresh(video)
    return video

@router.delete("/{video_id}")
async def delete_video(video_id: int, db: Session = Depends(get_db)):
    """Delete video"""
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    db.delete(video)
    db.commit()
    return {"message": "Video deleted successfully"}
