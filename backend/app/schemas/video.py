"""
Pydantic schemas for video data validation
"""
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class VideoBase(BaseModel):
    """Base video schema"""
    url: str
    username: str
    likes: int = 0
    comments: int = 0
    views: int = 0
    likes_rate: float = 0.0
    comments_rate: float = 0.0
    transcription: Optional[str] = None
    posted_at: Optional[datetime] = None

class VideoCreate(VideoBase):
    """Schema for creating a video"""
    pass

class VideoUpdate(BaseModel):
    """Schema for updating a video"""
    likes: Optional[int] = None
    comments: Optional[int] = None
    views: Optional[int] = None
    likes_rate: Optional[float] = None
    comments_rate: Optional[float] = None
    transcription: Optional[str] = None

class Video(VideoBase):
    """Schema for video response"""
    id: int
    created_at: datetime
    updated_at: datetime
    profile_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class VideoList(BaseModel):
    """Schema for video list response"""
    videos: list[Video]
    total: int
    page: int
    size: int
