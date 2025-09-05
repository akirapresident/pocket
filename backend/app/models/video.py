"""
Video model for Instagram videos
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.database import Base

class Video(Base):
    """Instagram video model"""
    __tablename__ = "videos"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic video info
    url = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    
    # Metrics
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    views = Column(Integer, default=0)
    
    # Engagement rates
    likes_rate = Column(Float, default=0.0)  # (likes/views)*100
    comments_rate = Column(Float, default=0.0)  # (comments/views)*100
    
    # Content
    transcription = Column(Text, nullable=True)
    
    # Timestamps
    posted_at = Column(DateTime, nullable=True)  # When video was posted
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    profile = relationship("Profile", back_populates="videos")
    
    def __repr__(self):
        return f"<Video(id={self.id}, url='{self.url}', username='{self.username}')>"
