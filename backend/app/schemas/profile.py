"""
Pydantic schemas for profile data validation
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.video import Video

class ProfileBase(BaseModel):
    """Base profile schema"""
    username: str
    followers_count: int = 0
    total_videos: int = 0
    total_views: int = 0
    total_likes: int = 0
    total_comments: int = 0
    avg_likes_rate: float = 0.0
    avg_comments_rate: float = 0.0

class ProfileCreate(ProfileBase):
    """Schema for creating a profile"""
    pass

class ProfileUpdate(BaseModel):
    """Schema for updating a profile"""
    followers_count: Optional[int] = None
    total_videos: Optional[int] = None
    total_views: Optional[int] = None
    total_likes: Optional[int] = None
    total_comments: Optional[int] = None
    avg_likes_rate: Optional[float] = None
    avg_comments_rate: Optional[float] = None

class Profile(ProfileBase):
    """Schema for profile response"""
    id: int
    created_at: datetime
    updated_at: datetime
    videos: List[Video] = []
    
    class Config:
        from_attributes = True

class ProfileList(BaseModel):
    """Schema for profile list response"""
    profiles: List[Profile]
    total: int
    page: int
    size: int
