"""
Analytics router for API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.utils.database import get_db
from app.models.video import Video
from app.models.profile import Profile

router = APIRouter()

@router.get("/engagement-stats")
async def get_engagement_stats(db: Session = Depends(get_db)):
    """Get overall engagement statistics"""
    stats = db.query(
        func.avg(Video.likes_rate).label('avg_likes_rate'),
        func.avg(Video.comments_rate).label('avg_comments_rate'),
        func.max(Video.likes_rate).label('max_likes_rate'),
        func.max(Video.comments_rate).label('max_comments_rate'),
        func.min(Video.likes_rate).label('min_likes_rate'),
        func.min(Video.comments_rate).label('min_comments_rate'),
        func.count(Video.id).label('total_videos')
    ).first()
    
    return {
        "average_likes_rate": round(stats.avg_likes_rate or 0, 2),
        "average_comments_rate": round(stats.avg_comments_rate or 0, 2),
        "max_likes_rate": round(stats.max_likes_rate or 0, 2),
        "max_comments_rate": round(stats.max_comments_rate or 0, 2),
        "min_likes_rate": round(stats.min_likes_rate or 0, 2),
        "min_comments_rate": round(stats.min_comments_rate or 0, 2),
        "total_videos": stats.total_videos or 0
    }

@router.get("/top-performers")
async def get_top_performers(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get top performing videos by engagement rate"""
    videos = db.query(Video).order_by(
        (Video.likes_rate + Video.comments_rate).desc()
    ).limit(limit).all()
    
    return [
        {
            "id": video.id,
            "url": video.url,
            "username": video.username,
            "likes_rate": video.likes_rate,
            "comments_rate": video.comments_rate,
            "total_engagement_rate": round(video.likes_rate + video.comments_rate, 2)
        }
        for video in videos
    ]

@router.get("/outliers")
async def get_outliers(
    threshold: float = Query(2.0, ge=0.1, le=10.0),
    db: Session = Depends(get_db)
):
    """Get outlier videos (engagement rate significantly above/below average)"""
    # Get average engagement rates
    avg_stats = db.query(
        func.avg(Video.likes_rate).label('avg_likes_rate'),
        func.avg(Video.comments_rate).label('avg_comments_rate')
    ).first()
    
    avg_likes_rate = avg_stats.avg_likes_rate or 0
    avg_comments_rate = avg_stats.avg_comments_rate or 0
    
    # Calculate thresholds
    likes_threshold_high = avg_likes_rate * (1 + threshold)
    likes_threshold_low = avg_likes_rate * (1 - threshold)
    comments_threshold_high = avg_comments_rate * (1 + threshold)
    comments_threshold_low = avg_comments_rate * (1 - threshold)
    
    # Find outliers
    outliers = db.query(Video).filter(
        (Video.likes_rate > likes_threshold_high) |
        (Video.likes_rate < likes_threshold_low) |
        (Video.comments_rate > comments_threshold_high) |
        (Video.comments_rate < comments_threshold_low)
    ).all()
    
    return {
        "average_likes_rate": round(avg_likes_rate, 2),
        "average_comments_rate": round(avg_comments_rate, 2),
        "threshold_multiplier": threshold,
        "outliers": [
            {
                "id": video.id,
                "url": video.url,
                "username": video.username,
                "likes_rate": video.likes_rate,
                "comments_rate": video.comments_rate,
                "is_high_performer": (
                    video.likes_rate > likes_threshold_high or 
                    video.comments_rate > comments_threshold_high
                )
            }
            for video in outliers
        ]
    }

@router.get("/profile-stats/{username}")
async def get_profile_stats(username: str, db: Session = Depends(get_db)):
    """Get statistics for a specific profile"""
    profile = db.query(Profile).filter(Profile.username == username).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    videos = db.query(Video).filter(Video.username == username).all()
    
    return {
        "profile": {
            "username": profile.username,
            "followers_count": profile.followers_count,
            "total_videos": profile.total_videos,
            "total_views": profile.total_views,
            "total_likes": profile.total_likes,
            "total_comments": profile.total_comments,
            "avg_likes_rate": profile.avg_likes_rate,
            "avg_comments_rate": profile.avg_comments_rate
        },
        "recent_videos": [
            {
                "id": video.id,
                "url": video.url,
                "likes": video.likes,
                "comments": video.comments,
                "views": video.views,
                "likes_rate": video.likes_rate,
                "comments_rate": video.comments_rate,
                "posted_at": video.posted_at
            }
            for video in videos[-10:]  # Last 10 videos
        ]
    }
